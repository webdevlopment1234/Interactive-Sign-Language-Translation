import React from 'react';

const Navbar = ({ activeSection, setActiveSection }) => {
    const sections = [
        { id: 'intro', label: 'Intro' },
        { id: 'prediction', label: 'Prediction' },
        { id: 'learning', label: 'Learning' },
        { id: 'quiz', label: 'Quiz' },
    ];

    return (
        <nav className="fixed top-0 w-full z-50 px-8 py-4 flex justify-between items-center text-white backdrop-blur-md bg-[rgba(15,23,42,0.8)] border-b border-[rgba(255,255,255,0.1)]">
            <div className="text-2xl font-extrabold cursor-pointer" onClick={() => setActiveSection('intro')}>
                Sign<span className="text-[#00d2ff]">Speak</span>
            </div>
            <ul className="flex gap-8">
                {sections.map(({ id, label }) => (
                    <li
                        key={id}
                        onClick={() => setActiveSection(id)}
                        className={`cursor-pointer transition duration-300 font-medium ${activeSection === id ? 'text-[#00d2ff]' : 'text-[rgba(248,250,252,0.7)] hover:text-white'
                            }`}
                    >
                        {label}
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default Navbar;
