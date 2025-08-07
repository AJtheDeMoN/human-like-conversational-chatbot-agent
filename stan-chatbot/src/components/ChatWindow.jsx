import React, { useEffect, useRef } from 'react';
import FormattedMessage from './FormattedMessage';
import LoadingSpinner from './LoadingSpinner';

const ChatWindow = ({ messages, isLoading }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-10">
      <div className="max-w-3xl mx-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`py-4 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xl px-5 py-3 rounded-2xl ${msg.sender === 'user' ? 'bg-blue-600 rounded-br-none' : 'bg-gray-700 rounded-bl-none'}`}>
              <FormattedMessage text={msg.text} />
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="py-4 flex justify-start">
            <div className="max-w-xl px-5 py-3 rounded-2xl bg-gray-700 rounded-bl-none">
              <LoadingSpinner />
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;