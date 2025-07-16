import React from 'react';
import { motion } from 'framer-motion';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="flex flex-col space-y-6"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900">Say goodbye to confusing health info</h1>
            <p className="text-xl text-grayText">
              Clear, accessible explanations that help you understand your health choices without the jargon.
            </p>
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-primary text-white font-semibold py-3 px-8 rounded-xl2 shadow-soft w-fit"
            >
              Get My Personal Guide
            </motion.button>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-gray-100 rounded-xl2 aspect-video flex items-center justify-center"
          >
            {/* Placeholder for Lottie animation */}
            <div className="text-center p-8">
              <p className="text-grayText font-semibold">60-sec Animation</p>
              <p className="text-sm text-gray-500 mt-2">(Lottie animation will go here)</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Impact Stats Strip */}
      <section className="bg-gray-50 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <motion.div 
              whileInView={{ scale: [0.9, 1] }}
              transition={{ duration: 0.5 }}
              className="bg-white p-6 rounded-xl shadow-soft"
            >
              <h3 className="text-3xl font-bold text-primary mb-2">95%</h3>
              <p className="text-grayText">users understood meds in first try</p>
            </motion.div>
            
            <motion.div 
              whileInView={{ scale: [0.9, 1] }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-white p-6 rounded-xl shadow-soft"
            >
              <h3 className="text-3xl font-bold text-primary mb-2">30%</h3>
              <p className="text-grayText">faster decisions</p>
            </motion.div>
            
            <motion.div 
              whileInView={{ scale: [0.9, 1] }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-white p-6 rounded-xl shadow-soft"
            >
              <h3 className="text-3xl font-bold text-primary mb-2">100%</h3>
              <p className="text-grayText">WCAG accessible</p>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
