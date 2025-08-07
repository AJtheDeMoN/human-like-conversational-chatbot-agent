import React from 'react';

const Sidebar = ({ sessions, activeSessionId, onNewChat, onSwitchSession }) => (
  <aside className="w-64 bg-gray-800 p-4 flex flex-col space-y-2">
    <button
      onClick={onNewChat}
      className="w-full text-left px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors duration-200"
    >
      + New Chat
    </button>
    <div className="flex-1 overflow-y-auto space-y-2 mt-4">
      {sessions.map((session) => (
        <button
          key={session.id}
          onClick={() => onSwitchSession(session.id)}
          className={`w-full text-left px-4 py-2 rounded-lg transition-colors duration-200 truncate ${
            activeSessionId === session.id ? 'bg-gray-600' : 'hover:bg-gray-700'
          }`}
        >
          {session.name}
        </button>
      ))}
    </div>
  </aside>
);

export default Sidebar;

