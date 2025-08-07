import React from 'react';
import { useChat } from './hooks/useChat';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';

export default function App() {
  const {
    sessions,
    activeSessionId,
    messages,
    isLoading,
    startNewChat,
    switchSession,
    handleSendMessage,
  } = useChat();

  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onNewChat={startNewChat}
        onSwitchSession={switchSession}
      />
      <main className="flex-1 flex flex-col">
        <ChatWindow messages={messages} isLoading={isLoading} />
        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </main>
    </div>
  );
}