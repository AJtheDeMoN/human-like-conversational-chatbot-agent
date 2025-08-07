import React, { useState } from 'react';

const SendIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
      <path d="m22 2-7 20-4-9-9-4Z"/><path d="m22 2-11 11"/>
    </svg>
);

const MessageInput = ({ onSendMessage, isLoading }) => {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = () => {
        if (inputValue.trim()) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    return (
        <div className="px-6 md:px-10 pb-6">
            <div className="max-w-3xl mx-auto">
                <div className="flex items-center w-full bg-gray-700 rounded-full px-2 focus-within:ring-2 focus-within:ring-blue-500 transition-shadow duration-200">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
                        placeholder="Message Kai..."
                        className="flex-grow bg-transparent border-none py-3 pl-3 focus:outline-none"
                        disabled={isLoading}
                    />
                    <button
                        onClick={handleSubmit}
                        disabled={isLoading || !inputValue.trim()}
                        className="p-2 rounded-full hover:bg-gray-600 disabled:hover:bg-transparent disabled:opacity-50 transition-colors duration-200"
                    >
                        <SendIcon />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default MessageInput;