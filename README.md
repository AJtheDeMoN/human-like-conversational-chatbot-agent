# Kai - A Human-Like Conversational AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to Kai, a sophisticated, human-like conversational AI designed to be an empathetic and context-aware companion. This project goes beyond a simple Q&A bot, implementing a multi-layered memory system, emotional tone adaptation, and a scalable, modular architecture ready for real-world integration.

**[Live Demo Link](https://[your-render-frontend-url].onrender.com)** 👈

---

## ✨ Key Features

* **Human-Like Interaction:** Delivers natural, emotionally engaging conversations by adapting its tone to be supportive, playful, or neutral based on the user's detected emotional state.
* **Persistent Multi-Session Memory:** Utilizes a **ChromaDB** vector store to remember distinct conversations. Users can create multiple chats, switch between them, and the history is saved permanently, even after restarting the server or refreshing the browser.
* **Advanced Context Awareness:** Employs a multi-step **RAG (Retrieval-Augmented Generation)** pipeline. This includes an LLM-based relevance filter that intelligently determines which past memories are relevant to the current topic, preventing context confusion when users switch subjects.
* **User-Level Emotion:** Tracks a user's emotional state across different chat sessions via a persistent user profile. If a user expresses sadness in one chat, Kai will maintain a supportive tone even if the user switches to a new chat.
* **Modular Full-Stack Architecture:** The backend is a stateless **FastAPI** service with separated logic for the API, chatbot core, and memory. The frontend is a clean, modular **React** application, ensuring the entire system is scalable and maintainable.

---

## 🛠️ Tech Stack

| Area      | Technology                                                                                             |
| :-------- | :----------------------------------------------------------------------------------------------------- |
| **Backend** | **Python**, **FastAPI** |
| **Frontend** | **React**, **Tailwind CSS** |
| **AI Model** | **Google Gemini API** (`gemini-1.5-flash`) for chat, context filtering, and emotion detection.         |
| **Database** | **ChromaDB** (Persistent Vector Store), **JSON** (for User Emotion Profiles)                             |
| **Hosting** | **Render** (Backend API & Persistent Disk), **Vercel / Netlify / Render** (Frontend)                     |

---

## 🚀 Getting Started

You can interact with the live demo linked above or run the project locally by following these steps.

### Prerequisites

* Node.js (v18 or later)
* Python (v3.9 or later)
* A Google Gemini API Key

### 1. Backend Setup (`kai_backend`)

1.  **Clone the repository:**
    ```bash
    git clone https://[your-github-repo-url]
    cd kai_backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` does not exist, create it with `pip freeze > requirements.txt`)*

3.  **Set up environment variables:**
    Create a file named `.env` in the `kai_backend` directory and add your API key:
    ```
    GOOGLE_API_KEY="your_actual_gemini_api_key"
    ```

4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup (`kai_frontend`)

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../kai_frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Set up environment variables:**
    Create a file named `.env` in the `kai_frontend` directory. For local development, add the following line:
    ```
    REACT_APP_API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```
    *(For a deployed version, replace the URL with your Render backend URL.)*

4.  **Run the development server:**
    ```bash
    npm start
    ```
    The application will be available at `http://localhost:3000`.

---

## 🏛️ Architecture Explained

Kai's architecture is designed for robustness and scalability.

1.  **UI (React):** The user interacts with the React frontend. It manages chat sessions in `localStorage` for persistence on the client-side and makes API calls to the backend.
2.  **API (FastAPI):** The backend receives requests. For a new message, it triggers the `Chatbot` service.
3.  **Emotion Detection:** The user's message is first analyzed to detect their current emotional state, which is then saved to a persistent `user_profiles.json` file.
4.  **Memory Retrieval (RAG):** The system queries the **ChromaDB** vector store to find past conversation snippets from the current `session_id` that are semantically similar to the recent conversation.
5.  **Relevance Filtering:** To avoid topic confusion, the retrieved memories and the recent conversation are passed to a Gemini model instance that acts as a filter, returning only the memories relevant to the *current* topic.
6.  **Prompt Augmentation:** A final, detailed prompt is constructed. It includes the user's latest message, the filtered memories, and a special instruction about the user's overall emotional state.
7.  **Response Generation:** This augmented prompt is sent to the main Gemini chat model, which generates Kai's final, context-aware, and emotionally-attuned response.
8.  **Memorization:** The new user message and Kai's response are converted to embeddings and saved back into ChromaDB for future recall.
