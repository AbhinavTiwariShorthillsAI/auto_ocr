import React from 'react';
import OCRLabeler from './components/OCRLabeler';
import { Toaster } from './components/ui/toaster';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <OCRLabeler />
      <Toaster />
    </div>
  );
}

export default App; 