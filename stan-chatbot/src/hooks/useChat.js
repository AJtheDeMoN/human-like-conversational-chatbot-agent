import { useState, useEffect, useRef } from 'react';
import { generateSessionId, sendMessageToServer } from '../api/chatService';

export const useChat = () => {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [allMessages, setAllMessages] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const isInitialized = useRef(false);

  // Load sessions from localStorage on initial render
  useEffect(() => {
    if (isInitialized.current) return;
    isInitialized.current = true;

    try {
      const savedSessions = JSON.parse(localStorage.getItem('kai_chat_sessions'));
      const savedMessages = JSON.parse(localStorage.getItem('kai_chat_messages'));

      if (savedSessions && savedSessions.length > 0) {
        setSessions(savedSessions);
        setAllMessages(savedMessages || {});
        setActiveSessionId(savedSessions[0].id);
      } else {
        startNewChat();
      }
    } catch (error) {
      console.error("Failed to load from localStorage:", error);
      startNewChat();
    }
  }, []);

  // Save sessions and messages to localStorage whenever they change
  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('kai_chat_sessions', JSON.stringify(sessions));
    }
    if (Object.keys(allMessages).length > 0) {
      localStorage.setItem('kai_chat_messages', JSON.stringify(allMessages));
    }
  }, [sessions, allMessages]);

  const startNewChat = () => {
    const newSessionId = generateSessionId();
    const chatNumber = sessions.length + 1;
    const newSessionName = `Chat ${chatNumber}`;
    const newSession = { id: newSessionId, name: newSessionName };

    setSessions(prev => [...prev, newSession]);
    setActiveSessionId(newSessionId);
    setAllMessages(prev => ({
      ...prev,
      [newSessionId]: [{ sender: 'bot', text: "Hello! I'm Kai. What new skill can I help you explore today? 🌱" }]
    }));
  };

  const switchSession = (sessionId) => {
    if (sessionId !== activeSessionId) {
      setActiveSessionId(sessionId);
    }
  };

  const handleSendMessage = async (inputValue) => {
    if (!inputValue.trim() || isLoading || !activeSessionId) return;

    const userMessage = { sender: 'user', text: inputValue };
    
    setAllMessages(prev => ({
      ...prev,
      [activeSessionId]: [...(prev[activeSessionId] || []), userMessage]
    }));

    setIsLoading(true);

    try {
      const data = await sendMessageToServer(activeSessionId, inputValue);
      const botMessage = { sender: 'bot', text: data.response };
      
      setAllMessages(prev => ({
        ...prev,
        [activeSessionId]: [...(prev[activeSessionId] || []), botMessage]
      }));

    } catch (error) {
      console.error("Failed to send message:", error);
      const errorMessage = { sender: 'bot', text: "Sorry, I'm having trouble connecting right now." };
      setAllMessages(prev => ({
        ...prev,
        [activeSessionId]: [...(prev[activeSessionId] || []), errorMessage]
      }));
    } finally {
      setIsLoading(false);
    }
  };

  return {
    sessions,
    activeSessionId,
    messages: allMessages[activeSessionId] || [],
    isLoading,
    startNewChat,
    switchSession,
    handleSendMessage,
  };
};
