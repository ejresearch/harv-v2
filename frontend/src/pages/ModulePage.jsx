import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function ModulePage() {
  const { moduleId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);

  const modules = {
    1: { title: 'Your Four Worlds', icon: '🌍', description: 'Understanding the four different worlds we live in and how they shape communication.', content: 'This module explores how communication exists in four distinct worlds: the physical world, the world of ideas, the social world, and the inner world of consciousness. Each world has its own rules, constraints, and possibilities for communication.' },
    2: { title: 'Media Uses & Effects', icon: '📺', description: 'How media influences society and individual behavior.', content: 'Examine theories of media effects and how different media channels influence public opinion and individual behavior patterns. We\'ll explore agenda-setting, framing, and cultivation theory.' },
    3: { title: 'Shared Characteristics', icon: '🔗', description: 'Common elements across all forms of mass communication.', content: 'Discover the fundamental characteristics that all mass communication media share, from books to digital platforms. These include mass production, rapid distribution, and the ability to reach diverse audiences.' },
    4: { title: 'Communication Infrastructure', icon: '📡', description: 'The systems and structures that enable mass communication.', content: 'Learn about the technological, economic, and social infrastructure that makes mass communication possible. From printing presses to internet servers, infrastructure shapes what messages can be sent and received.' },
    5: { title: 'Books', icon: '📚', description: 'The first mass medium and its lasting impact.', content: 'Explore how books revolutionized communication and continue to shape culture and knowledge distribution. Books created the first truly portable, mass-produced communication medium.' },
    6: { title: 'Newspapers', icon: '📰', description: 'Daily news and the democratic process.', content: 'Understand the role of newspapers in democracy, journalism, and public discourse. Newspapers created the concept of daily news and informed citizenship.' },
    7: { title: 'Magazines', icon: '📖', description: 'Specialized content for targeted audiences.', content: 'Examine how magazines serve niche audiences and specialized interests. Unlike newspapers, magazines could focus on specific topics and communities.' },
    8: { title: 'Comic Books', icon: '💭', description: 'Visual storytelling and cultural impact.', content: 'Analyze comics as a unique medium combining visual and textual communication. Comics demonstrate how images and words work together to create meaning.' },
    9: { title: 'Photography', icon: '📷', description: 'The power of visual communication.', content: 'Study how photography changed documentation, art, and mass communication. Photography brought visual evidence and artistic expression to mass media.' },
    10: { title: 'Recordings', icon: '🎵', description: 'Audio media and musical culture.', content: 'Explore how recorded audio transformed music, entertainment, and communication. Sound recording allowed mass distribution of audio content for the first time.' },
    11: { title: 'Motion Pictures', icon: '🎬', description: 'Cinema as art and mass entertainment.', content: 'Learn about film as both artistic expression and mass entertainment medium. Movies combined multiple media forms into powerful storytelling experiences.' },
    12: { title: 'Radio', icon: '📻', description: 'The theater of the mind.', content: 'Understand radio\'s unique position in mass communication and its enduring relevance. Radio created intimate, immediate connections with audiences through sound alone.' },
    13: { title: 'Television', icon: '📺', description: 'The dominant medium of the 20th century.', content: 'Examine television\'s massive cultural and social impact on society. TV brought visual and audio content directly into homes, reshaping family life and social habits.' },
    14: { title: 'Video Games', icon: '🎮', description: 'Interactive media and digital culture.', content: 'Analyze video games as an emerging form of interactive mass communication. Games represent the first truly interactive mass medium, where audiences become participants.' },
    15: { title: 'Economic Influencers', icon: '💰', description: 'Money, power, and media control.', content: 'Study how economic factors shape media content and distribution. Understanding who pays for media helps explain what messages get distributed and how.' }
  };

  useEffect(() => {
    setTimeout(() => {
      setModule(modules[parseInt(moduleId)] || modules[1]);
      setLoading(false);
    }, 500);
  }, [moduleId]);

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  const currentModuleId = parseInt(moduleId);
  const prevModule = currentModuleId > 1 ? currentModuleId - 1 : null;
  const nextModule = currentModuleId < 15 ? currentModuleId + 1 : null;

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-3xl">{module.icon}</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">{module.title}</h1>
              <p className="text-gray-600">{module.description}</p>
            </div>
          </div>
          <div className="text-sm text-gray-500">
            Module {moduleId} of 15
          </div>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={() => navigate('/chat')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            💬 Ask AI Tutor
          </button>
          <button
            onClick={() => navigate('/progress')}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
          >
            📊 View Progress
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
          >
            🏠 Dashboard
          </button>
        </div>
      </div>

      {/* Module Content */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Module Content</h2>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed text-lg mb-6">{module.content}</p>
          
          <div className="mt-8 p-6 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <h3 className="text-lg font-semibold text-blue-800 mb-3">🤔 Think About This</h3>
            <p className="text-blue-700 mb-4">
              Instead of just reading about {module.title.toLowerCase()}, let's explore together. 
              What questions do you have about this topic?
            </p>
            <button
              onClick={() => navigate('/chat')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Socratic Dialogue →
            </button>
          </div>

          {/* Learning Objectives */}
          <div className="mt-6 p-4 bg-green-50 rounded-lg">
            <h3 className="text-lg font-semibold text-green-800 mb-2">🎯 Learning Objectives</h3>
            <ul className="text-green-700 space-y-1">
              <li>• Understand the key concepts of {module.title.toLowerCase()}</li>
              <li>• Analyze how this relates to modern communication</li>
              <li>• Apply these concepts to real-world examples</li>
              <li>• Connect this module to previous learning</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        {prevModule ? (
          <button
            onClick={() => navigate(`/modules/${prevModule}`)}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium"
          >
            <span>←</span>
            <span>Previous: {modules[prevModule]?.title}</span>
          </button>
        ) : (
          <div></div>
        )}
        
        <div className="flex space-x-2">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            All Modules
          </button>
        </div>
        
        {nextModule ? (
          <button
            onClick={() => navigate(`/modules/${nextModule}`)}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium"
          >
            <span>Next: {modules[nextModule]?.title}</span>
            <span>→</span>
          </button>
        ) : (
          <div></div>
        )}
      </div>
    </div>
  );
}
