import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Types for API response data
interface ReadabilityScore {
  smog: number;
  gunningFog: number;
  grade: string;
  level: 'Good' | 'Moderate' | 'Poor';
}

interface RiskStatement {
  id: string;
  statement: string;
  percent: number;
  iconArray: string; // URL to icon array image
  explanation: string;
}

interface EquityScore {
  ctsPhrases: string[];
  equityScore: number;
}

interface AnalysisResult {
  readability: ReadabilityScore;
  risks: RiskStatement[];
  equity: EquityScore;
  pdfText?: string;
  htmlContent?: string;
  url?: string;
}

interface ClarifyWidgetProps {
  initialUrl?: string;
  onAnalysisComplete?: (result: AnalysisResult) => void;
}

const ClarifyWidget: React.FC<ClarifyWidgetProps> = ({ initialUrl = '', onAnalysisComplete }) => {
  const [url, setUrl] = useState(initialUrl);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState<'readability' | 'risks' | 'equity'>('readability');
  const [error, setError] = useState<string | null>(null);

  // Handle URL analysis
  const analyzeUrl = async () => {
    if (!url) {
      setError('Please enter a URL or upload a file');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Make a real API call to our backend
      const response = await fetchAnalysis(url);
      setResult(response);
      if (onAnalysisComplete) {
        onAnalysisComplete(response);
      }
    } catch (err) {
      setError('Failed to analyze the URL. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Real API call to our Flask backend
  const fetchAnalysis = async (targetUrl: string): Promise<AnalysisResult> => {
    try {
      // Use Flask backend API endpoint - adjust URL as needed for development/production
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';
      const apiUrl = `${apiBaseUrl}/process?url=${encodeURIComponent(targetUrl)}`;
      
      console.log(`Calling API: ${apiUrl}`);
      const response = await fetch(apiUrl);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('API Response:', data);
      
      // Transform API response to match our frontend data structure
      return {
        readability: {
          smog: data.equicheck_analysis?.readability?.smog_score || 0,
          gunningFog: data.equicheck_analysis?.readability?.gunning_fog_score || 0,
          grade: data.equicheck_analysis?.readability?.grade_level || 'Unknown',
          level: determineLevelFromScore(
            (data.equicheck_analysis?.readability?.smog_score + 
             data.equicheck_analysis?.readability?.gunning_fog_score) / 2
          )
        },
        risks: (data.riskify_analysis?.risk_statements || []).map((risk: any, index: number) => ({
          id: String(index),
          statement: risk.statement || '',
          percent: risk.percentage || 0,
          iconArray: risk.icon_array_path || '/placeholder-icon-array.png',
          explanation: risk.explanation || ''
        })),
        equity: {
          ctsPhrases: data.equicheck_analysis?.cts_phrases || [],
          equityScore: data.equicheck_analysis?.equity_score || 0
        },
        url: targetUrl,
        pdfText: data.scraped_content?.text || '',
        htmlContent: data.scraped_content?.html || ''
      };
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  };
  
  // Helper function to determine readability level from score
  const determineLevelFromScore = (score: number): 'Good' | 'Moderate' | 'Poor' => {
    if (score <= 8) return 'Good';
    if (score <= 12) return 'Moderate';
    return 'Poor';
  };

  // Function to get color based on score level
  const getLevelColor = (level: string) => {
    switch(level) {
      case 'Good': return 'text-success';
      case 'Moderate': return 'text-accent';
      case 'Poor': return 'text-danger';
      default: return 'text-grayText';
    }
  };

  return (
    <div className="bg-white rounded-xl2 shadow-soft overflow-hidden">
      {/* Input Section */}
      <div className="p-6 border-b">
        <h2 className="text-xl font-bold mb-4">Clarify+ Analysis Tool</h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL of patient decision aid"
            className="flex-1 border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-primary focus:border-primary"
            aria-label="URL input"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={analyzeUrl}
            disabled={isAnalyzing}
            className={`px-6 py-3 rounded-lg font-semibold min-w-[120px] ${
              isAnalyzing ? 'bg-gray-300 text-gray-500' : 'bg-primary text-white'
            }`}
          >
            {isAnalyzing ? (
              <div className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing
              </div>
            ) : 'Analyze'}
          </motion.button>
        </div>
        <div className="mt-2 text-sm">
          <button className="text-primary hover:underline">Upload PDF</button>
          <span className="mx-2 text-gray-400">or</span>
          <button className="text-primary hover:underline">Paste text</button>
        </div>
        
        {/* Error message */}
        {error && (
          <div className="mt-3 text-danger text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Results Section */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
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
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="mb-4">
                    <div className="flex flex-wrap items-baseline gap-2">
                      <h3 className="text-xl font-semibold">Readability:</h3>
                      <span className={`text-2xl font-bold ${getLevelColor(result.readability.level)}`}>
                        {result.readability.grade}
                      </span>
                      <span className="text-grayText">(SMOG: {result.readability.smog.toFixed(1)}, Gunning-Fog: {result.readability.gunningFog.toFixed(1)})</span>
                    </div>
                    
                    {/* Progress bar */}
                    <div className="mt-3 bg-gray-200 rounded-full h-2.5">
                      <div 
                        className={`h-2.5 rounded-full ${
                          result.readability.level === 'Good' 
                            ? 'bg-success' 
                            : result.readability.level === 'Moderate' 
                              ? 'bg-accent' 
                              : 'bg-danger'
                        }`} 
                        style={{ width: `${Math.min(100, (result.readability.smog / 20) * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between mt-1 text-xs text-gray-500">
                      <span>Grade 6 (Good)</span>
                      <span>Grade 12 (Poor)</span>
                    </div>
                  </div>
                  
                  <div className="mt-6">
                    <h3 className="font-semibold mb-2">Recommendations:</h3>
                    <ul className="list-disc pl-5 text-grayText">
                      <li>Use shorter sentences with simpler words</li>
                      <li>Break complex concepts into bullet points</li>
                      <li>Aim for a 6th-8th grade reading level</li>
                      <li>Use active voice instead of passive voice</li>
                    </ul>
                    <div className="mt-4">
                      <button className="text-primary hover:underline text-sm flex items-center">
                        <span>View simplified text</span>
                        <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
              
              {activeTab === 'risks' && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <h3 className="text-xl font-semibold mb-4">Risk Statements Found ({result.risks.length})</h3>
                  
                  <div className="space-y-6">
                    {result.risks.map(risk => (
                      <div key={risk.id} className="bg-gray-50 rounded-lg p-4">
                        <h4 className="font-semibold text-gray-900">{risk.statement}</h4>
                        
                        {/* Icon Array Visualization */}
                        <div className="my-4 bg-white border rounded-lg p-3">
                          <div className="flex flex-col md:flex-row gap-3">
                            <div className="flex-1">
                              {/* Placeholder for icon array visualization */}
                              <div className="grid grid-cols-10 gap-1 max-w-[300px]">
                                {[...Array(100)].map((_, i) => (
                                  <div 
                                    key={i} 
                                    className={`w-full aspect-square rounded-sm ${
                                      i < risk.percent ? 'bg-primary' : 'bg-gray-200'
                                    }`}
                                  />
                                ))}
                              </div>
                              <p className="mt-2 text-sm text-center text-gray-500">
                                {risk.percent} out of 100 people
                              </p>
                            </div>
                            <div className="flex-1">
                              <p className="text-grayText">{risk.explanation}</p>
                              <div className="mt-3">
                                <button className="text-primary hover:underline text-sm">
                                  Get personalized risk estimate
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    {result.risks.length === 0 && (
                      <p className="text-grayText">No risk statements were found in this document.</p>
                    )}
                  </div>
                </motion.div>
              )}
              
              {activeTab === 'equity' && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="flex items-baseline gap-2 mb-4">
                    <h3 className="text-xl font-semibold">Equity Score:</h3>
                    <span className={`text-2xl font-bold ${
                      result.equity.equityScore >= 80 ? 'text-success' :
                      result.equity.equityScore >= 60 ? 'text-accent' : 'text-danger'
                    }`}>
                      {result.equity.equityScore}/100
                    </span>
                  </div>
                  
                  <div className="mb-6">
                    <h4 className="font-semibold mb-2">CTS Phrases Found:</h4>
                    <div className="bg-gray-50 rounded-lg p-4">
                      {result.equity.ctsPhrases.length > 0 ? (
                        <ul className="list-disc pl-5 text-grayText">
                          {result.equity.ctsPhrases.map((phrase, index) => (
                            <li key={index}>"{phrase}" <span className="text-danger text-sm">Vague language</span></li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-success">No problematic phrases found.</p>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold mb-2">Recommendations:</h4>
                    <ul className="list-disc pl-5 text-grayText">
                      <li>Replace vague terms with specific numbers</li>
                      <li>Use both numeric and visual representations of risk</li>
                      <li>Provide absolute risk, not just relative risk</li>
                      <li>Consider cultural context when describing treatments</li>
                    </ul>
                  </div>
                </motion.div>
              )}
            </div>
            
            {/* Footer */}
            <div className="border-t p-4 flex justify-between items-center">
              <div className="text-sm text-grayText">
                Analyzed URL: <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline truncate max-w-xs inline-block">{result.url}</a>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="text-white bg-primary px-4 py-2 rounded-lg text-sm font-medium flex items-center"
              >
                <span>Generate Report</span>
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ClarifyWidget;
