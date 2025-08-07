import google.generativeai as genai
from memory import MemoryManager
from collections import deque
import re
import json
import os

# Define the path for our simple user profile database
USER_PROFILES_DB = 'user_profiles.json'

class Chatbot:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.memory = MemoryManager()
        self.chat_model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=self._get_persona())
        self.filter_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        self.emotion_model = genai.GenerativeModel(model_name="gemini-1.5-flash") # Model for emotion detection
        self.embedding_model = genai.GenerativeModel(model_name='models/embedding-001')
        self.recent_history = {}
        self.user_profiles = self._load_user_profiles()

    def _load_user_profiles(self):
        """Loads user profiles from a JSON file."""
        if os.path.exists(USER_PROFILES_DB):
            with open(USER_PROFILES_DB, 'r') as f:
                return json.load(f)
        return {}

    def _save_user_profiles(self):
        """Saves the current user profiles to a JSON file."""
        with open(USER_PROFILES_DB, 'w') as f:
            json.dump(self.user_profiles, f, indent=2)

    def _get_user_emotion(self, user_id: str) -> str:
        """Gets the last known emotion for a user."""
        return self.user_profiles.get(user_id, {}).get('last_emotion', 'neutral')

    def _detect_and_save_emotion(self, user_id: str, user_input: str):
        """Detects emotion from user input and saves it only if it's a significant change."""
        prompt = f"""
        Analyze the user's message and classify their primary emotion.
        Choose from: 'sad', 'happy', 'playful', 'frustrated', 'curious', 'neutral'.
        Respond with only the single chosen word.

        User Message: "{user_input}"
        """
        try:
            response = self.emotion_model.generate_content(prompt)
            detected_emotion = response.text.strip().lower()

            current_emotion = self._get_user_emotion(user_id)
            significant_emotions = {'sad', 'happy', 'playful', 'frustrated'}
            
            if detected_emotion in significant_emotions or current_emotion not in significant_emotions:
                if user_id not in self.user_profiles:
                    self.user_profiles[user_id] = {}
                self.user_profiles[user_id]['last_emotion'] = detected_emotion
                self._save_user_profiles()
                print(f"   [Emotion] Detected and SAVED new state '{detected_emotion}' for user {user_id}.")
            else:
                print(f"   [Emotion] Detected transient emotion '{detected_emotion}', maintaining existing state '{current_emotion}'.")

        except Exception as e:
            print(f"   [Emotion] Error detecting emotion: {e}")


    def _get_persona(self):
        return """
        You are Kai, a personal guide for a learning platform called 'Evolve'. You are fundamentally kind, supportive, and encouraging.
        You will receive an instruction about the user's current emotional state. You MUST adapt your tone to match it.
        For example, if the user is 'sad', be gentle and maintain that supportive tone until their mood clearly changes. If they are 'playful', be witty but kind. If they are 'frustrated', be extra patient.
        You will also receive context from the specific chat session. Use it to make relevant callbacks, but prioritize the user's overall emotional state in your tone.
        """

    def _filter_context_for_relevance(self, context: str, recent_conversation: str) -> str:
        """Uses an LLM to filter retrieved context for relevance to the recent conversation."""
        if not context:
            return ""

        # --- UPDATED PROMPT FOR BETTER CONTEXT FILTERING ---
        filtering_prompt = f"""
        You are a context filtering assistant. Your job is to determine which parts of the provided "Long-Term Conversation History" are relevant to the "Most Recent Conversation Snippet".

        The user may have switched topics. Focus ONLY on the topic in the "Most Recent Conversation Snippet".
        If none of the long-term history is relevant to the most recent topic, return an empty string.

        Most Recent Conversation Snippet:
        ---
        {recent_conversation}
        ---

        Long-Term Conversation History:
        ---
        {context}
        ---

        Relevant History (only about the most recent topic):
        """
        
        try:
            response = self.filter_model.generate_content(filtering_prompt)
            print(f"   [Filter] Relevant context identified:\n   ---\n   {response.text}\n   ---")
            return response.text
        except Exception as e:
            print(f"   [Filter] Error during context filtering: {e}")
            return context # Fallback to unfiltered context on error

    def get_response(self, user_id: str, user_input: str) -> str:
        # 1. DETECT & SAVE EMOTION
        self._detect_and_save_emotion(user_id, user_input)

        # 2. LOAD USER STATE
        current_emotion = self._get_user_emotion(user_id)
        emotional_instruction = f"IMPORTANT: The user's current emotional state is '{current_emotion}'. Your tone MUST reflect this."

        # 3. RETRIEVE & FILTER SESSION-SPECIFIC CONTEXT
        if user_id not in self.recent_history:
            self.recent_history[user_id] = deque(maxlen=4)
        self.recent_history[user_id].append(f"User: {user_input}")
        
        # This immediate context is now used for both searching and filtering
        search_query = "\n".join(self.recent_history[user_id])
        
        query_embedding = genai.embed_content(model=self.embedding_model.model_name, content=search_query)['embedding']
        retrieved_context = self.memory.search_memory(user_id, query_embedding)
        
        # --- UPDATED CALL TO THE FILTER ---
        # The filter now receives the recent conversation history for better accuracy.
        filtered_context = self._filter_context_for_relevance(retrieved_context, search_query)

        # 4. BUILD THE FINAL, FULLY-CONTEXTUALIZED PROMPT
        prompt = f"""
        {emotional_instruction}

        Context from this specific chat session:
        ---
        {filtered_context}
        ---
        Based on all of the above, answer my newest message: '{user_input}'
        """
        
        # 5. GENERATE RESPONSE & SAVE TO MEMORY
        chat = self.chat_model.start_chat(history=[])
        response = chat.send_message(prompt)
        bot_response = response.text

        user_embedding = genai.embed_content(model=self.embedding_model.model_name, content=f"User said: '{user_input}'")['embedding']
        bot_embedding = genai.embed_content(model=self.embedding_model.model_name, content=f"Kai responded: '{bot_response}'")['embedding']
        self.memory.add_to_memory(user_id, f"User said: '{user_input}'", user_embedding)
        self.memory.add_to_memory(user_id, f"Kai responded: '{bot_response}'", bot_embedding)
        self.recent_history[user_id].append(f"Kai: {bot_response}")

        return bot_response
