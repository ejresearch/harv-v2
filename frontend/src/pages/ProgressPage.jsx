import React from 'react';

const ProgressPage = () => {
  return (
    <div className="text-center py-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-6xl mb-6">📊</div>
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Learning Progress</h1>
        <p className="text-gray-600 mb-8">
          Track your journey through the Mass Communication course with detailed analytics and insights.
        </p>
        
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
          <h3 className="font-semibold text-green-800 mb-2">📈 Coming in Phase 3!</h3>
          <p className="text-green-700 text-sm">
            The progress dashboard will show detailed learning analytics, mastery levels, 
            time spent per module, and cross-module knowledge connections.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold text-gray-800 mb-3">📚 Module Progress</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Completion percentages</li>
              <li>• Time spent per module</li>
              <li>• Mastery level tracking</li>
              <li>• Learning streak counter</li>
            </ul>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold text-gray-800 mb-3">🔗 Knowledge Connections</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Cross-module insights</li>
              <li>• Concept relationship maps</li>
              <li>• Learning pathway visualization</li>
              <li>• Knowledge gap identification</li>
            </ul>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold text-gray-800 mb-3">💡 AI Insights</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Learning style analysis</li>
              <li>• Personalized recommendations</li>
              <li>• Difficulty adjustment suggestions</li>
              <li>• Next steps guidance</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;
