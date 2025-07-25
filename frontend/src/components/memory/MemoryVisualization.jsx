import React, { useState, useEffect } from 'react';
import { Brain, User, BookOpen, MessageCircle, Zap, Activity, Clock, TrendingUp } from 'lucide-react';

const MemoryVisualization = ({ moduleId, currentMessage, isVisible = true }) => {
  const [memoryContext, setMemoryContext] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeLayer, setActiveLayer] = useState(null);

  // Simulate API call to get memory context
  useEffect(() => {
    if (moduleId && isVisible) {
      fetchMemoryContext();
    }
  }, [moduleId, currentMessage, isVisible]);

  const fetchMemoryContext = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Simulate API call - replace with actual harvAPI call
      const mockContext = {
        layer1_profile: {
          content: `User: Sarah Chen | Learning Style: Visual-Kinesthetic | Pace: Moderate | Goals: Master communication theory for marketing career | Challenges: Understanding abstract concepts`,
          size: 156,
          status: 'active'
        },
        layer2_module: {
          content: `Module 1: Your Four Worlds | Focus: Communication models & perception | Key Concepts: Sender-receiver model, perceptual worlds, meaning construction | Socratic Mode: Guide discovery through questions`,
          size: 189,
          status: 'active'
        },
        layer3_conversation: {
          content: `Recent Discussion: Exploring how different people interpret the same message differently. Student showed understanding of basic sender-receiver model. Next: Guide toward perception differences.`,
          size: 134,
          status: 'active'
        },
        layer4_connections: {
          content: `Cross-Module Links: Module 2 (Media Effects) - perception shapes media interpretation | Module 6 (Newspapers) - gatekeeping as perception filter | Prior Knowledge: Marketing background relevant`,
          size: 167,
          status: 'active'
        },
        context_size: 646,
        layers_active: 4,
        success: true,
        assembly_time: 45
      };
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 800));
      setMemoryContext(mockContext);
    } catch (err) {
      setError('Failed to load memory context');
    } finally {
      setLoading(false);
    }
  };

  const layers = [
    {
      id: 'layer1',
      title: 'User Profile',
      icon: User,
      color: 'bg-blue-500',
      data: memoryContext?.layer1_profile,
      description: 'Learning style, preferences, and goals'
    },
    {
      id: 'layer2', 
      title: 'Module Context',
      icon: BookOpen,
      color: 'bg-green-500',
      data: memoryContext?.layer2_module,
      description: 'Current module objectives and focus'
    },
    {
      id: 'layer3',
      title: 'Conversation State',
      icon: MessageCircle,
      color: 'bg-purple-500', 
      data: memoryContext?.layer3_conversation,
      description: 'Real-time conversation history'
    },
    {
      id: 'layer4',
      title: 'Knowledge Connections',
      icon: Zap,
      color: 'bg-orange-500',
      data: memoryContext?.layer4_connections,
      description: 'Cross-module learning links'
    }
  ];

  if (!isVisible) return null;

  return (
    <div className="bg-slate-900 text-white p-6 rounded-lg max-w-md">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Brain className="w-6 h-6 text-blue-400" />
          <h3 className="text-lg font-semibold">Enhanced Memory</h3>
        </div>
        <button 
          onClick={fetchMemoryContext}
          disabled={loading}
          className="text-blue-400 hover:text-blue-300 transition-colors"
        >
          <Activity className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin w-8 h-8 border-2 border-blue-400 border-t-transparent rounded-full mx-auto mb-3"></div>
          <p className="text-sm text-gray-400">Assembling memory context...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 mb-4">
          <p className="text-sm text-red-300">{error}</p>
          <button 
            onClick={fetchMemoryContext}
            className="text-xs text-red-400 hover:text-red-300 mt-2"
          >
            Retry
          </button>
        </div>
      )}

      {/* Memory Context Display */}
      {memoryContext && !loading && (
        <>
          {/* Context Stats */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-blue-400">{memoryContext.context_size}</div>
              <div className="text-xs text-gray-400">Context Size</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-green-400">{memoryContext.layers_active}/4</div>
              <div className="text-xs text-gray-400">Layers Active</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-purple-400">{memoryContext.assembly_time}ms</div>
              <div className="text-xs text-gray-400">Assembly Time</div>
            </div>
          </div>

          {/* Memory Layers */}
          <div className="space-y-3">
            {layers.map((layer) => {
              const Icon = layer.icon;
              const isActive = activeLayer === layer.id;
              
              return (
                <div key={layer.id} className="space-y-2">
                  <button
                    onClick={() => setActiveLayer(isActive ? null : layer.id)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${
                      isActive ? 'bg-slate-700' : 'bg-slate-800 hover:bg-slate-750'
                    }`}
                  >
                    <div className={`w-3 h-3 rounded-full ${layer.color} flex-shrink-0`}></div>
                    <Icon className="w-4 h-4 text-gray-300 flex-shrink-0" />
                    <div className="flex-1 text-left">
                      <div className="text-sm font-medium">{layer.title}</div>
                      <div className="text-xs text-gray-400">{layer.description}</div>
                    </div>
                    <div className="text-xs text-gray-500">
                      {layer.data?.size || 0} chars
                    </div>
                    <div className={`w-2 h-2 rounded-full ${
                      layer.data?.status === 'active' ? 'bg-green-400' : 'bg-gray-600'
                    }`}></div>
                  </button>
                  
                  {/* Layer Content Expansion */}
                  {isActive && layer.data && (
                    <div className="ml-6 pl-4 border-l-2 border-slate-700">
                      <div className="bg-slate-800 rounded-lg p-3">
                        <div className="text-xs text-gray-300 leading-relaxed">
                          {layer.data.content}
                        </div>
                        <div className="flex items-center gap-4 mt-3 pt-3 border-t border-slate-700">
                          <div className="flex items-center gap-1 text-xs text-gray-500">
                            <Clock className="w-3 h-3" />
                            Updated now
                          </div>
                          <div className="flex items-center gap-1 text-xs text-gray-500">
                            <TrendingUp className="w-3 h-3" />
                            High relevance
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Assembly Status */}
          <div className="mt-6 pt-4 border-t border-slate-700">
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-400">Memory Assembly</span>
              <span className="text-green-400 font-medium">
                ✓ Successful ({memoryContext.assembly_time}ms)
              </span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5 mt-2">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-1.5 rounded-full transition-all duration-500"
                style={{ width: '100%' }}
              ></div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default MemoryVisualization;
