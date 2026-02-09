import { useState } from 'react';

// Custom Styles for Heartbeat Animation
const styles = `
  @keyframes heartbeat {
    0% { box-shadow: 0 0 0 rgba(244, 63, 94, 0); }
    50% { box-shadow: 0 0 0 20px rgba(244, 63, 94, 0.1); }
    100% { box-shadow: 0 0 0 rgba(244, 63, 94, 0); }
  }
  .heartbeat-glow {
    animation: heartbeat 3s infinite ease-in-out;
  }
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .animate-fade-in-up {
    animation: fadeInUp 0.5s ease-out;
  }
`;

function App() {
  // 1. State for Form Data - UPDATED WITH CORRECT HIGH RISK VALUES
  const [formData, setFormData] = useState({
    Age: 65, // Higher age for risk
    Sex: '1', // Male
    'Chest pain type': 4, // Asymptomatic (highest risk)
    BP: 180, // High BP
    Cholesterol: 300, // High cholesterol
    'FBS over 120': '1', // High fasting blood sugar
    'EKG results': 2, // Left ventricular hypertrophy
    'Max HR': 120, // Low max heart rate
    'Exercise angina': '1', // Yes
    'ST depression': 4.5, // High ST depression
    'Slope of ST': 3, // Downsloping
    'Number of vessels fluro': 3, // Maximum vessels affected
    Thallium: '7' // Reversible defect (highest risk)
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHelp, setShowHelp] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (prob) => {
    if (prob > 70) return 'bg-red-600';
    if (prob > 40) return 'bg-orange-400';
    return 'bg-emerald-500';
  };

  return (
      <>
        <style>{styles}</style>

        {/* MEDICAL THEME BACKGROUND */}
        <div className="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-red-50 flex items-center justify-center p-4 font-sans text-slate-800">

          {/* Main Card with Glassmorphism & Heartbeat Glow */}
          <div className="bg-white/95 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-5xl border border-rose-200 heartbeat-glow relative">

            {/* Header - Centered */}
            <div className="text-center pt-6 pb-8">
              {/* Medical Icon */}
              <div className="inline-block p-4 rounded-full bg-rose-100 text-rose-600 mb-4 shadow-sm ring-4 ring-rose-50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 21 5.42 21 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
              </div>
              <h2 className="text-4xl font-extrabold text-rose-900 mb-2 tracking-tight">VitalThrob AI</h2>
              <p className="text-rose-700 font-medium">Deep Neural Network Analysis • Real-time Cardiovascular Assessment • Cardio Check</p>
            </div>

            {/* Guide Button - Top Right Corner */}
            <button
                onClick={() => setShowHelp(true)}
                className="absolute top-6 right-6 bg-gradient-to-r from-rose-500 to-red-600 text-white hover:from-rose-600 hover:to-red-700 shadow-lg rounded-full px-5 py-2.5 flex items-center gap-2 transition-all font-bold text-sm z-10 transform hover:scale-105"
                title="How to use this tool"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>How to Use</span>
            </button>

            {/* The Main Form */}
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

              {/* SECTION 1: PATIENT VITALS */}
              <div className="md:col-span-2">
                <h3 className="text-sm font-bold text-rose-400 uppercase tracking-wider border-b border-rose-200 pb-2 mb-4">
                  <span className="text-rose-600 mr-2">01.</span>Patient Vitals
                </h3>
              </div>

              {[
                { label: 'Age (Years)', name: 'Age', type: 'number', min: 20, max: 100, step: 1 },
                { label: 'Resting Blood Pressure (mmHg)', name: 'BP', type: 'number', min: 80, max: 250, step: 1 },
                { label: 'Serum Cholesterol (mg/dL)', name: 'Cholesterol', type: 'number', min: 100, max: 400, step: 1 },
                { label: 'Max Heart Rate Achieved (bpm)', name: 'Max HR', type: 'number', min: 60, max: 220, step: 1 },
                { label: 'ST Depression Induced by Exercise', name: 'ST depression', type: 'number', min: 0, max: 6, step: 0.1 },
              ].map(field => (
                  <div key={field.name} className="col-span-1 group">
                    <label className="block text-xs font-bold text-slate-600 mb-1 uppercase group-hover:text-rose-600 transition-colors">{field.label}</label>
                    <input
                        type={field.type}
                        name={field.name}
                        value={formData[field.name]}
                        onChange={handleChange}
                        min={field.min}
                        max={field.max}
                        step={field.step}
                        className="w-full bg-slate-50 border border-slate-200 text-slate-900 rounded-xl p-3 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition-all shadow-sm"
                    />
                  </div>
              ))}

              {/* SECTION 2: MEDICAL HISTORY */}
              <div className="md:col-span-2 mt-2">
                <h3 className="text-sm font-bold text-rose-400 uppercase tracking-wider border-b border-rose-200 pb-2 mb-4">
                  <span className="text-rose-600 mr-2">02.</span>Medical History & Symptoms
                </h3>
              </div>

              {/* Sex */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Sex</label>
                <select name="Sex" value={formData.Sex} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-rose-500">
                  <option value="1">Male</option>
                  <option value="0">Female</option>
                </select>
              </div>

              {/* Chest Pain Type */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Chest Pain Type</label>
                <select name="Chest pain type" value={formData['Chest pain type']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="1">1 - Typical angina</option>
                  <option value="2">2 - Atypical angina</option>
                  <option value="3">3 - Non-anginal pain</option>
                  <option value="4">4 - Asymptomatic (high risk)</option>
                </select>
              </div>

              {/* FBS */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Fasting Blood Sugar > 120 mg/dL</label>
                <select name="FBS over 120" value={formData['FBS over 120']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="0">No {`<=`} 120</option>
                  <option value="1">Yes (> 120)</option>
                </select>
              </div>

              {/* EKG Results */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Resting EKG Results</label>
                <select name="EKG results" value={formData['EKG results']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="0">0 - Normal</option>
                  <option value="1">1 - ST-T wave abnormality</option>
                  <option value="2">2 - Left ventricular hypertrophy</option>
                </select>
              </div>

              {/* Exercise Angina */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Exercise Induced Angina</label>
                <select name="Exercise angina" value={formData['Exercise angina']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>

              {/* Slope of ST */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Slope of ST Segment</label>
                <select name="Slope of ST" value={formData['Slope of ST']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="1">1 - Upsloping</option>
                  <option value="2">2 - Flat</option>
                  <option value="3">3 - Downsloping (high risk)</option>
                </select>
              </div>

              {/* Number of vessels fluro */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Fluoroscopy Colored Vessels</label>
                <select name="Number of vessels fluro" value={formData['Number of vessels fluro']} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="0">0 - None</option>
                  <option value="1">1 - One vessel</option>
                  <option value="2">2 - Two vessels</option>
                  <option value="3">3 - Three vessels (high risk)</option>
                </select>
              </div>

              {/* Thallium */}
              <div className="col-span-1">
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase">Thallium Stress Test</label>
                <select name="Thallium" value={formData.Thallium} onChange={handleChange} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3">
                  <option value="3">3 - Normal</option>
                  <option value="6">6 - Fixed defect</option>
                  <option value="7">7 - Reversible defect (high risk)</option>
                </select>
              </div>

              {/* Submit Button */}
              <div className="md:col-span-2 mt-4">
                <button type="submit" disabled={loading}
                        className={`w-full text-white font-bold py-4 px-6 rounded-xl text-lg transition-all duration-300 shadow-lg transform hover:-translate-y-1 
                  ${loading ? 'bg-rose-400 cursor-not-allowed' : 'bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700'}`}
                >
                  {loading ? 'Analyzing EKG Data...' : 'Predict Heart Disease Risk'}
                </button>
              </div>
            </form>

            {/* Error Box */}
            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl flex items-center justify-center gap-3" role="alert">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  <div>
                    <strong className="font-bold block">Prediction Error</strong>
                    <span className="block sm:inline">{error}</span>
                  </div>
                </div>
            )}

            {/* Result Section */}
            {result && (
                <div className="animate-fade-in-up mt-6">
                  {/* Visual Risk Meter */}
                  <div className="text-center mb-4">
                    <p className="text-rose-700 text-sm font-medium mb-2">Neural Network Confidence Score</p>
                    <div className="w-full bg-rose-100 rounded-full h-6 overflow-hidden relative">
                      <div
                          className={`h-full transition-all duration-1000 ease-out ${getRiskColor(result.probability)}`}
                          style={{ width: `${result.probability}%` }}
                      ></div>
                    </div>
                    <p className="text-3xl font-bold mt-2 text-rose-900">{result.probability}%</p>
                  </div>

                  {/* Result Badge */}
                  <div className={`p-8 rounded-2xl border text-center shadow-inner ${
                      result.prediction === 1
                          ? 'bg-gradient-to-br from-red-100 to-rose-100 border-red-300 text-red-900'
                          : 'bg-gradient-to-br from-emerald-50 to-emerald-100 border-emerald-300 text-emerald-900'
                  }`}>
                    {result.prediction === 1
                        ? (
                            <>
                              <div className="text-5xl mb-2">⚠️</div>
                              <h3 className="text-3xl font-bold mb-2">High Risk Detected</h3>
                              <p className="text-sm opacity-80">Model suggests high probability of cardiovascular anomaly. Immediate medical consultation recommended.</p>
                            </>
                        )
                        : (
                            <>
                              <div className="text-5xl mb-2">✅</div>
                              <h3 className="text-3xl font-bold mb-2">Low Risk Detected</h3>
                              <p className="text-sm opacity-80">Model indicates low probability of cardiovascular disease based on provided metrics.</p>
                            </>
                        )}
                  </div>

                  {/* Download/Print Button */}
                  <div className="text-center mt-6">
                    <button
                        onClick={() => window.print()}
                        className="text-sm text-rose-600 hover:text-rose-800 underline font-medium"
                    >
                      Print / Save Patient Report
                    </button>
                  </div>
                </div>
            )}

            {/* Ethical Footer */}
            <div className="mt-8 border-t border-rose-200 pt-6 text-center">
              <p className="text-xs text-rose-500">
                ⚠️ <strong>Disclaimer:</strong> This tool is an AI educational demonstration.
                It does not constitute professional medical advice. Always consult a qualified doctor for health decisions.
              </p>
            </div>

            {/* THE HELP MODAL POP-UP */}
            {showHelp && (
                <div
                    className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    onClick={() => setShowHelp(false)}
                >
                  <div
                      className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl p-8 relative animate-fade-in-up max-h-[90vh] overflow-y-auto"
                      onClick={(e) => e.stopPropagation()}
                  >
                    {/* Close Button */}
                    <button
                        onClick={() => setShowHelp(false)}
                        className="absolute top-4 right-4 text-rose-400 hover:text-rose-700 hover:bg-rose-50 rounded-full p-2 transition-colors"
                        aria-label="Close help"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>

                    <h2 className="text-2xl font-bold text-rose-900 mb-6 flex items-center gap-3">
                      <div className="bg-rose-100 text-rose-600 rounded-full w-10 h-10 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      How VitalThrob AI Works
                    </h2>

                    <div className="space-y-6">
                      {/* Section 1: How to Use */}
                      <div className="bg-rose-50/50 rounded-xl p-5 border border-rose-100">
                        <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center">
                          <span className="bg-rose-500 text-white rounded-full w-7 h-7 flex items-center justify-center mr-3 text-sm">1</span>
                          How to Use This Tool
                        </h3>
                        <ul className="space-y-3 text-slate-700">
                          <li className="flex items-start">
                            <span className="text-rose-500 mr-2 font-bold">•</span>
                            <span>Fill in the <strong className="text-rose-700">Patient Vitals</strong> (Age, BP, Cholesterol) from your recent medical checkup.</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-rose-500 mr-2 font-bold">•</span>
                            <span>Fill in the <strong className="text-rose-700">Medical History</strong> (Pain type, Stress test results).
                                            <br /><span className="text-xs text-rose-400 italic ml-6">Tip: Check your "Thallium" value (usually 3, 6, or 7).</span>
                                        </span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-rose-500 mr-2 font-bold">•</span>
                            <span>Click the <strong className="text-rose-700">"Predict Heart Disease Risk"</strong> button.</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-rose-500 mr-2 font-bold">•</span>
                            <span>The AI will calculate a percentage score (0-100%) and a Risk Badge (High/Low).</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-rose-500 mr-2 font-bold">•</span>
                            <span>Click the <strong className="text-rose-700">"Print / Save Patient Report"</strong> button to save the result for your doctor.</span>
                          </li>
                        </ul>
                      </div>

                      <hr className="border-rose-200" />

                      {/* Section 2: How the AI Works */}
                      <div className="bg-blue-50/50 rounded-xl p-5 border border-blue-100">
                        <h3 className="text-lg font-bold text-slate-800 mb-3 flex items-center">
                          <span className="bg-blue-500 text-white rounded-full w-7 h-7 flex items-center justify-center mr-3 text-sm">2</span>
                          The Neural Network Logic
                        </h3>
                        <p className="text-slate-700 mb-4 leading-relaxed">
                          <strong className="text-blue-700">Think of it as a Digital Cardiologist.</strong><br /><br />
                          Behind the scenes, we trained a <strong className="text-blue-700">Deep Neural Network</strong> on over 300 patient records.
                          When you enter your data, the model compares your BP, Heart Rate, and Stress Test results to the patterns it "learned."
                        </p>
                        <div className="bg-white/80 p-4 rounded-lg border-l-4 border-blue-500">
                          <p className="text-sm font-mono text-slate-800">
                            <span className="text-blue-600">Input Data</span> ➔ <span className="text-purple-600">Mathematical Model</span> ➔ <span className="text-green-600">Probability Output</span> (e.g., 85%)
                          </p>
                        </div>
                      </div>

                      {/* Input Map */}
                      <div className="bg-emerald-50/50 rounded-xl p-5 border border-emerald-100">
                        <h4 className="text-md font-bold text-slate-800 mb-3 flex items-center">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                          </svg>
                          Quick Field Reference Map
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-slate-700">
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">BP</div>
                            <span className="font-medium">Resting Blood Pressure</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">Chest pain type</div>
                            <span className="font-medium">Chest Pain (1-4)</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">Cholesterol</div>
                            <span className="font-medium">Serum Cholesterol</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">Max HR</div>
                            <span className="font-medium">Max Heart Rate</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">Slope of ST</div>
                            <span className="font-medium">ST Segment Slope (1-3)</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="bg-rose-100 text-rose-700 text-xs font-bold px-2 py-1 rounded">Number of vessels fluro</div>
                            <span className="font-medium">Fluoroscopy Vessels (0-3)</span>
                          </div>
                        </div>
                      </div>

                      {/* Field Range Guide */}
                      <div className="bg-purple-50/50 rounded-xl p-5 border border-purple-100">
                        <h4 className="text-md font-bold text-slate-800 mb-3 flex items-center">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          </svg>
                          Medical Value Ranges
                        </h4>
                        <div className="text-sm text-slate-700 space-y-2">
                          <p><strong>Chest Pain Type:</strong> 1-4 (4 = Asymptomatic = Highest Risk)</p>
                          <p><strong>EKG Results:</strong> 0-2 (2 = Left Ventricular Hypertrophy)</p>
                          <p><strong>Slope of ST:</strong> 1-3 (3 = Downsloping = Highest Risk)</p>
                          <p><strong>Fluoroscopy Vessels:</strong> 0-3 (3 = All Vessels = Highest Risk)</p>
                          <p><strong>Thallium Stress Test:</strong> 3, 6, or 7 (7 = Reversible Defect = Highest Risk)</p>
                          <p><strong>ST Depression:</strong> 0-6mm (Higher = More Risk)</p>
                        </div>
                      </div>

                      {/* Important Note */}
                      <div className="bg-amber-50/70 rounded-xl p-5 border border-amber-200">
                        <h4 className="text-md font-bold text-amber-800 mb-2 flex items-center">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                          </svg>
                          Important Note
                        </h4>
                        <p className="text-amber-700 text-sm">
                          This AI tool provides <strong>predictive analysis only</strong> and is not a substitute for professional medical diagnosis.
                          Always consult with a qualified healthcare provider for medical decisions.
                        </p>
                      </div>
                    </div>

                    {/* Close Button at Bottom */}
                    <div className="mt-8 pt-6 border-t border-rose-200">
                      <button
                          onClick={() => setShowHelp(false)}
                          className="w-full bg-gradient-to-r from-rose-500 to-red-600 text-white font-bold py-3 rounded-xl hover:from-rose-600 hover:to-red-700 transition-all"
                      >
                        Got It, Close Guide
                      </button>
                    </div>
                  </div>
                </div>
            )}
          </div>
        </div>
      </>
  );
}

export default App;