import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: Date;
}

const HelpBot: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([ // Fixed syntax error
    {
      id: '1',
      sender: 'bot',
      text: "Hi there! I'm HelpBot. I can help explain medical terms, risk percentages, or clarify any confusing health information. What would you like help with today?",
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: inputText.trim(),
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);
    
    // Simulate bot response after a delay
    setTimeout(() => {
      let botResponse = '';
      
      if (inputText.toLowerCase().includes('risk')) {
        botResponse = 'Risk can be presented in different ways. When you see a percentage like "15% risk", it means that out of 100 people, about 15 will experience that outcome. I recommend looking at both the numbers and any visual representations like icon arrays to better understand your personal risk.';
      } else if (inputText.toLowerCase().includes('side effect') || inputText.toLowerCase().includes('side-effect')) {
        botResponse = 'Side effects are unwanted symptoms caused by medical treatments. They range from minor (like a headache) to serious. Every medication has potential side effects, but not everyone experiences them. The decision aid should list how common each side effect is - look for percentages or phrases like "common" or "rare".';
      } else {
        botResponse = 'That\'s a great question! Medical information can be complex. I recommend discussing this with your healthcare provider who knows your personal health history. Is there a specific part of the information that I can try to clarify for you?';
      }
      
      const newBotMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: botResponse,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, newBotMessage]);
      setIsTyping(false);
    }, 1500);
  };
  
  // Format timestamps
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm px-4 py-4 flex items-center">
        <div className="bg-primary w-10 h-10 rounded-full flex items-center justify-center text-white mr-3">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-gray-900">HelpBot</h1>
          <p className="text-sm text-grayText">Your personal medical information assistant</p>
        </div>
      </header>
      
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map(message => (
            <motion.div 
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-sm rounded-xl2 p-4 ${
                message.sender === 'user' 
                  ? 'bg-primary text-white' 
                  : 'bg-white shadow-soft'
              }`}>
                <p className={message.sender === 'user' ? 'text-white' : 'text-gray-800'}>
                  {message.text}
                </p>
                <p className={`text-xs mt-1 text-right ${
                  message.sender === 'user' ? 'text-white/70' : 'text-gray-500'
                }`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </motion.div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white rounded-xl2 shadow-soft p-4 max-w-sm">
                <div className="flex space-x-1 items-center">
                  <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input area */}
      <div className="bg-white border-t p-4">
        <div className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask me about medical terms or risks..."
            className="flex-1 border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-primary focus:border-primary"
            aria-label="Chat message"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            className="bg-primary text-white p-3 rounded-lg"
            aria-label="Send message"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
          </motion.button>
          <button 
            className="bg-gray-100 text-gray-700 p-3 rounded-lg"
            aria-label="Voice input"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path>
            </svg>
          </button>
        </div>
        <div className="max-w-3xl mx-auto mt-2 flex justify-between text-xs text-gray-500">
          <span>Type a question or tap the microphone</span>
          <button className="underline">Need help?</button>
        </div>
      </div>
    </div>
  );
};

export default HelpBot;
