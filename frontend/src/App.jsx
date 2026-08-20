import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Prediction from './components/Prediction';
import Learning from './components/Learning';
import Quiz from './components/Quiz';

function App() {
  const [activeSection, setActiveSection] = useState('intro');

  const renderSection = () => {
    switch (activeSection) {
      case 'intro':
        return <Hero setActiveSection={setActiveSection} />;
      case 'prediction':
        return <Prediction />;
      case 'learning':
        return <Learning />;
      case 'quiz':
        return <Quiz />;
      default:
        return <Hero setActiveSection={setActiveSection} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white selection:bg-cyan-500/30">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-500/10 rounded-full blur-[120px]" />
      </div>

      <Navbar activeSection={activeSection} setActiveSection={setActiveSection} />

      <main className="pt-20 relative z-10 container mx-auto px-4 md:px-8">
        {renderSection()}
      </main>
    </div>
  );
}

export default App;
