import React, { useState, useEffect, useRef } from 'react';
import { Send, Mic, MicOff, Settings, Brain, Zap, Clock, User, BookOpen } from 'lucide-react';
import MemoryVisualization from './MemoryVisualization';

const EnhancedChatInterface = ({ moduleId = 1, userId }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [showMemory, setShowMemory] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [wsConnection, setWsConnection] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Sample initial messages
  useEffect(() => {
    const initialMessages = [
      {
        id: 1,
        type: 'assistant',
        content: "Welcome to Module 1: Your Four Worlds! I'm here to guide you through understanding communication models. Let's start with a question - when you send a text message to a friend, what do you think happens between your idea and their understanding?",
        timestamp: new Date(Date.now() - 300000),
        memoryContext: {
          layer: 'module_intro',
          relevance: 'high'
        }
      }
    ];
    setMessages(initialMessages);
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // WebSocket connection simulation
  useEffect(() => {
    // Simulate WebSocket connection
    setConnectionStatus('connecting');
    setTimeout(() => {
      setConnectionStatus('connected');
    }, 1000);

    return () => {
      if (wsConnection) {
        wsConnection.close();
      }
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI processing with memory context
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Simulate Socratic AI response
      const aiResponse = generateSocraticResponse(inputMessage.trim());
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: aiResponse,
        timestamp: new Date(),
        memoryContext: {
          layer: 'conversation_active',
          relevance: 'high',
          connections: ['module_1_concepts', 'user_progress']
        }
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: "I apologize, but I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const generateSocraticResponse = (userInput) => {
    // Simple Socratic response generator (replace with actual AI)
    const responses = [
      "That's an interesting perspective! What do you think might influence how your friend interprets your message differently than you intended?",
      "I can see you're thinking about this. Can you help me understand what you mean by that? What examples come to mind?",
      "Good observation! Now, what do you think happens to a message between the moment you create it and when someone else receives it?",
      "You're on the right track. What role do you think the medium (like text vs. phone call) plays in how your message is understood?",
      "That's a thoughtful answer. How might this concept apply to mass media like television or newspapers?"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // Implement voice recording logic here
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">Module 1: Your Four Worlds</h1>
                <p className="text-sm text-gray-600">Communication Models & Perception</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {/* Connection Status */}
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-green-500 animate-pulse' : 
                  connectionStatus === 'connecting' ? 'bg-yellow-500 animate-pulse' : 'bg-red-500'
                }`}></div>
                <span className="text-sm text-gray-600 capitalize">{connectionStatus}</span>
              </div>

              {/* Controls */}
              <button
                onClick={() => setShowMemory(!showMemory)}
                className={`p-2 rounded-lg transition-colors ${
                  showMemory ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'
                }`}
                title="Toggle Memory Visualization"
              >
                <Brain className="w-5 h-5" />
              </button>
              <button className="p-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors">
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-lg ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                {/* Message Bubble */}
                <div
                  className={`px-4 py-3 rounded-2xl ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                      : message.isError
                      ? 'bg-red-50 border border-red-200 text-red-800'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                </div>

                {/* Message Meta */}
                <div className={`flex items-center gap-2 mt-1 px-2 ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}>
                  <span className="text-xs text-gray-500">{formatTime(message.timestamp)}</span>
                  {message.memoryContext && (
                    <div className="flex items-center gap-1">
                      <Zap className="w-3 h-3 text-purple-500" />
                      <span className="text-xs text-purple-600">Memory Active</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Avatar */}
              <div className={`w-8 h-8 rounded-full flex-shrink-0 ${
                message.type === 'user' ? 'order-1 ml-3' : 'order-2 mr-3'
              }`}>
                {message.type === 'user' ? (
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                ) : (
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">AI</span>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex justify-start">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-bold">AI</span>
                </div>
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 px-6 py-4">
          <div className="flex items-end gap-3">
            <div className="flex-1">
              <div className="relative">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage(e)}
                  placeholder="Share your thoughts about communication..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  disabled={isTyping}
                />
              </div>
            </div>
            
            <button
              type="button"
              onClick={toggleRecording}
              className={`p-3 rounded-2xl transition-colors ${
                isRecording 
                  ? 'bg-red-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
            
            <button
              type="button"
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isTyping}
              className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>

          {/* Quick Suggestions */}
          <div className="flex flex-wrap gap-2 mt-3">
            {[
              "What's a communication model?",
              "How do perceptions differ?",
              "Give me an example",
              "I don't understand"
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setInputMessage(suggestion)}
                className="text-xs px-3 py-1 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Memory Visualization Panel */}
      {showMemory && (
        <div className="w-80 border-l border-gray-200 bg-gray-50">
          <MemoryVisualization 
            moduleId={moduleId}
            currentMessage={inputMessage}
            isVisible={showMemory}
          />
        </div>
      )}
    </div>
  );
};

export default EnhancedChatInterface;
