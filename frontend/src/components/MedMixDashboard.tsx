import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface MedicationCard {
  id: string;
  name: string;
  purpose: string;
  riskLevel: 'green' | 'amber' | 'red';
}

const MedMixDashboard: React.FC = () => {
  // Sample data - would be replaced with API data
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [medications, setMedications] = useState<MedicationCard[]>([
    { id: '1', name: 'Lisinopril', purpose: 'Lowers blood pressure by relaxing blood vessels', riskLevel: 'green' },
    { id: '2', name: 'Metformin', purpose: 'Controls blood sugar levels for type 2 diabetes', riskLevel: 'amber' },
    { id: '3', name: 'Atorvastatin', purpose: 'Lowers cholesterol by reducing production in the liver', riskLevel: 'green' },
    { id: '4', name: 'Amlodipine', purpose: 'Relaxes blood vessels to lower blood pressure', riskLevel: 'red' },
  ]);

  const [selectedCondition, setSelectedCondition] = useState<string | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [duplicatesFound, setDuplicatesFound] = useState(2);
  const [selectedMed, setSelectedMed] = useState<MedicationCard | null>(null);

  const conditions = ['Diabetes', 'Hypertension', 'High Cholesterol', 'Anxiety'];

  const filterByCondition = (condition: string | null) => {
    setSelectedCondition(condition === selectedCondition ? null : condition);
  };

  // Badge colors based on risk level
  const getBadgeColor = (riskLevel: string) => {
    switch(riskLevel) {
      case 'green': return 'bg-success text-white';
      case 'amber': return 'bg-accent text-white';
      case 'red': return 'bg-danger text-white';
      default: return 'bg-gray-200 text-gray-700';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with condition filter pills */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">MedMix Dashboard</h1>
          
          <div className="flex flex-wrap gap-2">
            {conditions.map((condition) => (
              <button
                key={condition}
                onClick={() => filterByCondition(condition)}
                className={`px-4 py-2 rounded-full text-sm font-medium ${
                  selectedCondition === condition 
                    ? 'bg-primary text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {condition}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Duplicate Detector Banner */}
      {duplicatesFound > 0 && (
        <div className="bg-accent/10 sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex justify-between items-center">
            <p className="text-accent font-medium">
              <span className="font-bold">{duplicatesFound} duplicates</span> found
            </p>
            <button className="text-sm text-primary font-medium hover:underline">
              Resolve
            </button>
          </div>
        </div>
      )}

      {/* Medication Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {medications.map((med) => (
            <motion.div
              key={med.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-xl2 shadow-soft h-[120px] p-4 flex flex-col relative cursor-pointer"
              onClick={() => setSelectedMed(med)}
            >
              <div className="flex items-center gap-3">
                <div className="bg-gray-100 w-10 h-10 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-grayText" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-900">{med.name}</h3>
              </div>
              <p className="text-sm text-grayText mt-2 line-clamp-2">{med.purpose}</p>
              
              {/* Risk Badge */}
              <div className={`absolute bottom-4 left-4 px-2 py-1 rounded-md text-xs font-medium ${getBadgeColor(med.riskLevel)}`}>
                {med.riskLevel === 'green' ? 'Low Risk' : med.riskLevel === 'amber' ? 'Medium Risk' : 'High Risk'}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Side Panel (Explain mode) */}
      {selectedMed && (
        <motion.div
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-lg z-20 overflow-y-auto"
        >
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">{selectedMed.name}</h2>
              <button 
                onClick={() => setSelectedMed(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold mb-2">Purpose</h3>
              <p className="text-grayText">{selectedMed.purpose}</p>
            </div>

            <div className="mb-6">
              <h3 className="font-semibold mb-2">Dosage & Side Effects</h3>
              <ul className="list-disc pl-5 text-grayText">
                <li>Take 1 tablet daily with food</li>
                <li>May cause dizziness or lightheadedness</li>
                <li>May cause dry cough in some people</li>
              </ul>
            </div>

            <div className="flex border-t pt-4">
              <button className="bg-primary text-white px-4 py-2 rounded-md mr-2 flex-grow">English</button>
              <button className="bg-gray-100 text-grayText px-4 py-2 rounded-md flex-grow">Español</button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default MedMixDashboard;
