import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function ChatPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "Hello! I'm your AI tutor for Mass Communication. I'm here to guide you through Socratic questioning to help you discover insights yourself. What topic would you like to explore today?",
      timestamp: new Date()
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const socraticResponses = [
    "That's an interesting point! What do you think might happen if we consider the opposite perspective?",
    "Great observation! Can you think of a specific example that illustrates this concept?",
    "I can see you're thinking deeply about this. What questions does this raise for you?",
    "Excellent! Now, how might this apply to modern digital communication?",
    "Fascinating! What assumptions are we making here that we should examine?",
    "Good thinking! How does this connect to what we learned about media effects?",
    "Wonderful insight! What evidence would support or challenge this idea?"
  ];

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message
    const userMsg = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setMessage('');
    setIsTyping(true);

    // Simulate AI thinking and response
    setTimeout(() => {
      const randomResponse = socraticResponses[Math.floor(Math.random() * socraticResponses.length)];
      const aiMsg = {
        id: Date.now() + 1,
        type: 'ai',
        content: randomResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="h-full flex flex-col bg-white rounded-lg shadow">
      {/* Chat Header */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-800">AI Tutor Chat</h2>
            <p className="text-sm text-gray-600">Ask questions about Mass Communication concepts</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => navigate('/dashboard')}
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Dashboard
            </button>
            <button
              onClick={() => navigate('/progress')}
              className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
            >
              View Progress
            </button>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                msg.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p>{msg.content}</p>
              <p className={`text-xs mt-1 ${
                msg.type === 'user' ? 'text-blue-100' : 'text-gray-500'
              }`}>
                {msg.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Chat Input */}
      <form onSubmit={sendMessage} className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask a question about communication theory..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isTyping}
          />
          <button
            type="submit"
            disabled={isTyping || !message.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isTyping ? '⏳' : 'Send'}
          </button>
        </div>
        <div className="mt-2 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setMessage("What are the four worlds of communication?")}
            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200"
          >
            Four Worlds?
          </button>
          <button
            type="button"
            onClick={() => setMessage("How do media effects work?")}
            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200"
          >
            Media Effects?
          </button>
          <button
            type="button"
            onClick={() => setMessage("What makes mass communication different?")}
            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200"
          >
            Mass Communication?
          </button>
        </div>
      </form>
    </div>
  );
}
