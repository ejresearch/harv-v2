import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

const ModulePage = () => {
  const { moduleId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [module, setModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadModuleData();
  }, [moduleId]);

  const loadModuleData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [moduleData, progressData] = await Promise.all([
        api.getModule(parseInt(moduleId)),
        api.getUserProgress(user.id, parseInt(moduleId))
      ]);
      
      setModule(moduleData);
      setProgress(progressData);
    } catch (error) {
      console.error('Failed to load module:', error);
      // Set demo data if API fails
      const demoModule = {
        id: parseInt(moduleId),
        title: getModuleTitle(parseInt(moduleId)),
        description: getModuleDescription(parseInt(moduleId)),
        estimated_duration: 45
      };
      const demoProgress = {
        completion_percentage: moduleId === '1' ? 100 : moduleId === '2' ? 75 : 30,
        total_conversations: 3,
        insights_gained: 5,
        time_spent: 120,
        mastery_level: 'intermediate'
      };
      setModule(demoModule);
      setProgress(demoProgress);
    } finally {
      setLoading(false);
    }
  };

  const handleStartChat = () => {
    navigate(`/chat?module=${moduleId}`);
  };

  const handleNextModule = () => {
    const nextModuleId = parseInt(moduleId) + 1;
    if (nextModuleId <= 15) {
      navigate(`/modules/${nextModuleId}`);
    }
  };

  const handlePreviousModule = () => {
    const prevModuleId = parseInt(moduleId) - 1;
    if (prevModuleId >= 1) {
      navigate(`/modules/${prevModuleId}`);
    }
  };

  if (loading) {
    return <ModuleLoading />;
  }

  if (error) {
    return <ModuleError error={error} onRetry={loadModuleData} />;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Module Header */}
      <ModuleHeader 
        module={module}
        progress={progress}
        onStartChat={handleStartChat}
      />

      {/* Module Navigation */}
      <ModuleNavigation
        currentModuleId={parseInt(moduleId)}
        onPrevious={handlePreviousModule}
        onNext={handleNextModule}
      />

      {/* Module Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <ModuleContent module={module} />
          <LearningObjectives module={module} />
          <KeyConcepts module={module} />
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <ProgressTracker progress={progress} />
          <QuickActions 
            moduleId={moduleId}
            onStartChat={handleStartChat}
            progress={progress}
          />
          <RelatedModules currentModuleId={parseInt(moduleId)} />
        </div>
      </div>

      {/* Module Footer */}
      <ModuleFooter
        currentModuleId={parseInt(moduleId)}
        progress={progress}
        onNext={handleNextModule}
      />
    </div>
  );
};

// Supporting Components for ModulePage
const ModuleHeader = ({ module, progress, onStartChat }) => (
  <div className="bg-white rounded-xl shadow-sm overflow-hidden">
    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-8">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-4">
            <span className="text-4xl">{getModuleIcon(module.id)}</span>
            <div>
              <div className="text-indigo-200 text-sm font-medium">Module {module.id}</div>
              <h1 className="text-3xl font-bold">{module.title}</h1>
            </div>
          </div>
          
          <p className="text-indigo-100 text-lg mb-6 max-w-2xl">
            {module.description}
          </p>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={onStartChat}
              className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-indigo-50 transition-colors flex items-center space-x-2"
            >
              <span>🤖</span>
              <span>Start Learning with AI</span>
            </button>
            
            <div className="text-indigo-200 text-sm">
              ⏱️ Estimated time: {module.estimated_duration || 45} minutes
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="text-indigo-200 text-sm mb-2">Progress</div>
          <div className="text-2xl font-bold">
            {Math.round(progress?.completion_percentage || 0)}%
          </div>
          <div className="bg-indigo-400 bg-opacity-30 rounded-full h-2 w-24 mt-2">
            <div 
              className="bg-white rounded-full h-2 transition-all duration-300"
              style={{ width: `${progress?.completion_percentage || 0}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  </div>
);

const ModuleNavigation = ({ currentModuleId, onPrevious, onNext }) => (
  <div className="flex justify-between items-center bg-white rounded-lg shadow-sm p-4">
    <button
      onClick={onPrevious}
      disabled={currentModuleId <= 1}
      className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span>←</span>
      <span>Previous Module</span>
    </button>
    
    <div className="text-sm text-gray-600">
      Module {currentModuleId} of 15
    </div>
    
    <button
      onClick={onNext}
      disabled={currentModuleId >= 15}
      className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span>Next Module</span>
      <span>→</span>
    </button>
  </div>
);

const ModuleContent = ({ module }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h2 className="text-xl font-bold text-gray-800 mb-6">Module Overview</h2>
    
    <div className="prose max-w-none">
      <div className="text-gray-700 leading-relaxed space-y-4">
        {getModuleOverview(module.id)}
      </div>
    </div>
    
    <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
      <div className="flex items-start space-x-3">
        <span className="text-blue-600 text-xl">💡</span>
        <div>
          <h3 className="font-semibold text-blue-800 mb-2">Socratic Learning Approach</h3>
          <p className="text-blue-700 text-sm">
            Instead of reading through content, engage with our AI tutor to discover key concepts through 
            guided questioning. This active learning approach helps you build deeper understanding.
          </p>
        </div>
      </div>
    </div>
  </div>
);

const LearningObjectives = ({ module }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h2 className="text-xl font-bold text-gray-800 mb-6">Learning Objectives</h2>
    
    <div className="space-y-3">
      {getModuleObjectives(module.id).map((objective, index) => (
        <div key={index} className="flex items-start space-x-3">
          <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
            <span className="text-green-600 text-sm">✓</span>
          </div>
          <p className="text-gray-700">{objective}</p>
        </div>
      ))}
    </div>
  </div>
);

const KeyConcepts = ({ module }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h2 className="text-xl font-bold text-gray-800 mb-6">Key Concepts to Explore</h2>
    
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {getModuleConcepts(module.id).map((concept, index) => (
        <div key={index} className="p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-2">{concept.title}</h3>
          <p className="text-gray-600 text-sm">{concept.description}</p>
        </div>
      ))}
    </div>
  </div>
);

const ProgressTracker = ({ progress }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Progress</h3>
    
    <div className="space-y-4">
      <div>
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-600">Completion</span>
          <span className="font-medium">{Math.round(progress?.completion_percentage || 0)}%</span>
        </div>
        <div className="bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-full h-2 transition-all duration-300"
            style={{ width: `${progress?.completion_percentage || 0}%` }}
          />
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-center">
        <div className="p-3 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">
            {progress?.total_conversations || 0}
          </div>
          <div className="text-xs text-blue-600">AI Chats</div>
        </div>
        
        <div className="p-3 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">
            {progress?.insights_gained || 0}
          </div>
          <div className="text-xs text-green-600">Insights</div>
        </div>
      </div>
      
      <div className="text-sm text-gray-600">
        <div>Time spent: {formatDuration(progress?.time_spent || 0)}</div>
        <div>Mastery level: <span className="capitalize font-medium">{progress?.mastery_level || 'beginner'}</span></div>
      </div>
    </div>
  </div>
);

const QuickActions = ({ moduleId, onStartChat, progress }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
    
    <div className="space-y-3">
      <button
        onClick={onStartChat}
        className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-colors flex items-center justify-center space-x-2"
      >
        <span>🤖</span>
        <span>Chat with AI Tutor</span>
      </button>
      
      <button className="w-full bg-gray-100 text-gray-700 px-4 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors flex items-center justify-center space-x-2">
        <span>📚</span>
        <span>Review Key Points</span>
      </button>
      
      <button className="w-full bg-gray-100 text-gray-700 px-4 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors flex items-center justify-center space-x-2">
        <span>📊</span>
        <span>View Progress</span>
      </button>
    </div>
  </div>
);

const RelatedModules = ({ currentModuleId }) => {
  const getRelatedModules = (moduleId) => {
    const related = [];
    if (moduleId > 1) related.push(moduleId - 1);
    if (moduleId < 15) related.push(moduleId + 1);
    return related;
  };

  const relatedIds = getRelatedModules(currentModuleId);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Related Modules</h3>
      
      <div className="space-y-3">
        {relatedIds.map(moduleId => (
          <div key={moduleId} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors">
            <span className="text-xl">{getModuleIcon(moduleId)}</span>
            <div>
              <div className="font-medium text-gray-800">Module {moduleId}</div>
              <div className="text-sm text-gray-600">{getModuleTitle(moduleId)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const ModuleFooter = ({ currentModuleId, progress, onNext }) => {
  const isCompleted = (progress?.completion_percentage || 0) >= 80;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Ready for the next module?</h3>
          <p className="text-gray-600">
            {isCompleted 
              ? "Great progress! You're ready to move forward."
              : "Complete more of this module to unlock the next one."
            }
          </p>
        </div>
        
        <button
          onClick={onNext}
          disabled={!isCompleted || currentModuleId >= 15}
          className="bg-gradient-to-r from-green-500 to-teal-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-green-600 hover:to-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <span>Continue to Module {currentModuleId + 1}</span>
          <span>→</span>
        </button>
      </div>
    </div>
  );
};

// Loading and Error States
const ModuleLoading = () => (
  <div className="max-w-4xl mx-auto space-y-6">
    <div className="bg-white rounded-xl shadow-sm p-8">
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3 mb-6"></div>
        <div className="h-12 bg-gray-200 rounded w-48"></div>
      </div>
    </div>
  </div>
);

const ModuleError = ({ error, onRetry }) => (
  <div className="max-w-4xl mx-auto">
    <div className="bg-white rounded-xl shadow-sm p-8 text-center">
      <div className="text-6xl mb-4">😕</div>
      <h2 className="text-xl font-semibold text-gray-800 mb-2">Oops! Something went wrong</h2>
      <p className="text-gray-600 mb-6">{error}</p>
      <button
        onClick={onRetry}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Try Again
      </button>
    </div>
  </div>
);

// Helper Functions
const getModuleIcon = (moduleId) => {
  const icons = {
    1: '🌍', 2: '📺', 3: '🔗', 4: '📡', 5: '📚',
    6: '📰', 7: '📖', 8: '💭', 9: '📷', 10: '🎵',
    11: '🎬', 12: '📻', 13: '📺', 14: '🎮', 15: '💰'
  };
  return icons[moduleId] || '📚';
};

const getModuleTitle = (moduleId) => {
  const titles = {
    1: 'Your Four Worlds', 2: 'Media Uses & Effects', 3: 'Shared Characteristics',
    4: 'Communication Infrastructure', 5: 'Books', 6: 'Newspapers', 7: 'Magazines',
    8: 'Comic Books', 9: 'Photography', 10: 'Recordings', 11: 'Motion Pictures',
    12: 'Radio', 13: 'Television', 14: 'Video Games', 15: 'Economic Influencers'
  };
  return titles[moduleId] || 'Module';
};

const getModuleDescription = (moduleId) => {
  const descriptions = {
    1: 'Communication models, perception, and the four worlds we live in',
    2: 'How media functions in society and affects our daily lives',
    3: 'Common elements and characteristics across all media types',
    4: 'The evolution of communication technology and infrastructure',
    5: 'The birth of mass communication through printed books',
    6: 'News values, gatekeeping, and the newspaper industry',
    7: 'Special interest targeting and magazine publishing',
    8: 'Visual storytelling and the impact of comic books',
    9: 'Capturing reality and the art of photography',
    10: 'From Bach to rap - recordings as cultural mirrors',
    11: 'The beginning of mass entertainment through motion pictures',
    12: 'Radio as the household utility that changed society',
    13: 'Television as the center of attention and dominant medium',
    14: 'Video games as the newest form of mass media',
    15: 'Advertising, media ownership, and economic influences'
  };
  return descriptions[moduleId] || 'Explore this important communication topic';
};

const getModuleOverview = (moduleId) => {
  const overviews = {
    1: (
      <>
        <p>Communication is the bridge between minds, yet we often overlook how profoundly our perception shapes every interaction. In this foundational module, you'll explore the four interconnected worlds that influence all human communication.</p>
        <p>Through Socratic dialogue with our AI tutor, you'll discover how your personal experiences, cultural background, and the media you consume create unique lenses through which you interpret messages. This isn't just theory—it's the key to understanding why the same message can be received so differently by different people.</p>
      </>
    ),
    5: (
      <>
        <p>Books represent humanity's first true mass medium, fundamentally changing how knowledge is preserved and shared across generations. Before the printing press, information was scarce, expensive, and controlled by a select few.</p>
        <p>In this module, you'll explore how Johannes Gutenberg's innovation democratized knowledge, sparked religious reformation, and laid the foundation for all mass communication that followed. Discover why books remain powerful even in our digital age.</p>
      </>
    )
  };
  
  return overviews[moduleId] || (
    <>
      <p>Explore the fundamental concepts and historical development of this important communication medium.</p>
      <p>Through guided discovery with our AI tutor, you'll understand how this medium shaped society and continues to influence our world today.</p>
    </>
  );
};

const getModuleObjectives = (moduleId) => {
  const objectives = {
    1: [
      "Identify and analyze the four worlds that shape human communication",
      "Understand how personal perception affects message interpretation",
      "Recognize the role of media in shaping our worldview",
      "Apply communication theory to real-world examples"
    ],
    5: [
      "Trace the evolution from manuscript to mass-produced books",
      "Analyze the social impact of the printing press",
      "Understand how books democratized knowledge and literacy",
      "Evaluate the continuing relevance of books in digital media"
    ]
  };
  
  return objectives[moduleId] || [
    "Understand the historical development of this communication medium",
    "Analyze its impact on society and culture",  
    "Explore current applications and future trends",
    "Apply theoretical concepts to contemporary examples"
  ];
};

const getModuleConcepts = (moduleId) => {
  const concepts = {
    1: [
      { title: "The Self World", description: "Your personal experiences and identity" },
      { title: "The Social World", description: "Cultural and interpersonal influences" },
      { title: "The Physical World", description: "Material reality and environment" },
      { title: "The Media World", description: "Information from mass communication" }
    ],
    5: [
      { title: "Manuscript Culture", description: "Pre-printing book production and literacy" },
      { title: "Movable Type", description: "Gutenberg's revolutionary printing technology" },
      { title: "Mass Literacy", description: "How books spread reading skills" },
      { title: "Knowledge Democratization", description: "Information accessibility transformation" }
    ]
  };
  
  return concepts[moduleId] || [
    { title: "Historical Context", description: "Origins and development" },
    { title: "Technical Innovation", description: "Key technological advances" },
    { title: "Social Impact", description: "Effects on society and culture" },
    { title: "Modern Relevance", description: "Contemporary applications" }
  ];
};

const formatDuration = (minutes) => {
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours}h ${remainingMinutes}m`;
};

export default ModulePage;
