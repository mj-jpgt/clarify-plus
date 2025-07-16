import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface AnalysisResult {
  readability: {
    score: number;
    grade: string;
    level: 'Good' | 'Moderate' | 'Poor';
  };
  risks: {
    id: string;
    statement: string;
    percent: number;
    iconArray: string; // URL to icon array image
    explanation: string;
  }[];
  ctsPhrases: string[];
}

const DecisionAidViewer: React.FC = () => {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState<'readability' | 'risks' | 'equity'>('readability');
  
  // Sample data - would be replaced with API data
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!url) return;
    
    setIsAnalyzing(true);
    
    // Simulate API call
    setTimeout(() => {
      // Sample data
      setAnalysisResult({
        readability: {
          score: 14.7,
          grade: '9th Grade',
          level: 'Moderate'
        },
        risks: [
          {
            id: '1',
            statement: 'Treatment A has a 15% chance of causing headaches',
            percent: 15,
            iconArray: '/placeholder-icon-array.png',
            explanation: 'This means that out of 100 people who take this treatment, about 15 will experience headaches.'
          },
          {
            id: '2',
            statement: 'Treatment B reduces pain in 3 out of 4 patients',
            percent: 75,
            iconArray: '/placeholder-icon-array.png',
            explanation: 'This means that out of 100 people who take this treatment, about 75 will experience less pain.'
          }
        ],
        ctsPhrases: [
          'many patients find relief',
          'studies suggest',
          'may be effective'
        ]
      });
      
      setIsAnalyzing(false);
    }, 2000);
  };

  // Get color for readability level
  const getReadabilityColor = (level: string) => {
    switch(level) {
      case 'Good': return 'text-success';
      case 'Moderate': return 'text-accent';
      case 'Poor': return 'text-danger';
      default: return 'text-grayText';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-10">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Decision Aid Analyzer</h1>
          <p className="text-grayText mt-1">
            Analyze patient decision aids for readability, risk presentation, and equity
          </p>
        </div>
      </header>
      
      {/* Input form */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-xl2 shadow-soft p-6">
          <label htmlFor="url-input" className="block text-sm font-medium text-gray-700 mb-2">
            Enter URL or upload a PDF
          </label>
          <div className="flex gap-2">
            <input
              id="url-input"
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/decision-aid.pdf"
              className="flex-1 border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-primary focus:border-primary"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className={`px-6 py-3 rounded-lg font-semibold ${
                isAnalyzing ? 'bg-gray-300 text-gray-500' : 'bg-primary text-white'
              }`}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze'}
            </motion.button>
          </div>
          <div className="mt-2 text-sm text-gray-500">Or drag and drop a PDF file here</div>
        </div>
      </div>
      
      {/* Results */}
      {analysisResult && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
          <div className="bg-white rounded-xl2 shadow-soft overflow-hidden">
            {/* Tabs */}
            <div className="border-b">
              <div className="flex space-x-1 p-1">
                {['readability', 'risks', 'equity'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab as any)}
                    className={`py-3 px-6 font-medium rounded-t-lg ${
                      activeTab === tab 
                        ? 'text-primary border-b-2 border-primary' 
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Tab Content */}
            <div className="p-6">
              {activeTab === 'readability' && (
                <div>
                  <div className="mb-4">
                    <div className="flex items-baseline">
                      <h2 className="text-xl font-semibold">Readability Score:</h2>
                      <span className={`ml-2 text-2xl font-bold ${getReadabilityColor(analysisResult.readability.level)}`}>
                        {analysisResult.readability.score}
                      </span>
                    </div>
                    <p className="text-grayText">
                      Reading Level: {analysisResult.readability.grade} ({analysisResult.readability.level})
                    </p>
                  </div>
                  
                  <div className="mt-6">
                    <h3 className="font-semibold mb-2">Recommendations:</h3>
                    <ul className="list-disc pl-5 text-grayText">
                      <li>Use shorter sentences with simpler words</li>
                      <li>Break complex concepts into bullet points</li>
                      <li>Aim for a 6th-8th grade reading level</li>
                    </ul>
                  </div>
                </div>
              )}
              
              {activeTab === 'risks' && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">Risk Statements Found</h2>
                  
                  <div className="space-y-6">
                    {analysisResult.risks.map(risk => (
                      <div key={risk.id} className="bg-gray-50 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900">{risk.statement}</h3>
                        
                        {/* Placeholder for Icon Array */}
                        <div className="my-4 bg-white border rounded-lg p-3 flex items-center justify-center h-32">
                          <p className="text-gray-400 text-center">Icon Array will be shown here</p>
                        </div>
                        
                        <div className="text-grayText">
                          <p>{risk.explanation}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {activeTab === 'equity' && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">Equity & Language Analysis</h2>
                  
                  <div className="mb-6">
                    <h3 className="font-semibold mb-2">CTS Phrases Found:</h3>
                    <div className="bg-gray-50 rounded-lg p-4">
                      {analysisResult.ctsPhrases.length > 0 ? (
                        <ul className="list-disc pl-5 text-grayText">
                          {analysisResult.ctsPhrases.map((phrase, index) => (
                            <li key={index}>{phrase}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-grayText">No problematic phrases found.</p>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Recommendations:</h3>
                    <ul className="list-disc pl-5 text-grayText">
                      <li>Replace vague terms with specific numbers</li>
                      <li>Use both numeric and visual representations of risk</li>
                      <li>Provide absolute risk, not just relative risk</li>
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DecisionAidViewer;
