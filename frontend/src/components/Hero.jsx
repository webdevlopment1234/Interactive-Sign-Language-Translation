import React from "react";
import { Hand } from "lucide-react";

const Hero = ({ setActiveSection }) => {
    return (
        <div className="flex flex-col md:flex-row items-center justify-between min-h-[90vh] px-8 md:px-20 py-24 gap-12 bg-transparent">
            {/* Left Content */}
            <div className="flex-1 space-y-8 animate-fade-in">
                <h1 className="text-5xl md:text-7xl font-extrabold leading-tight text-white">
                    Bridging the Gap <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#00d2ff] to-[#3a7bd5]">
                        with Technology
                    </span>
                </h1>
                <p className="text-lg md:text-xl text-[rgba(248,250,252,0.8)] max-w-lg leading-relaxed font-light">
                    SignSpeak uses advanced Machine Learning to translate Indian Sign Language into text in real-time. Empowering communication for everyone.
                </p>
                <div className="flex gap-4 pt-4">
                    <button
                        onClick={() => setActiveSection("prediction")}
                        className="px-8 py-3 rounded-full text-white font-semibold bg-gradient-to-r from-[#00d2ff] to-[#3a7bd5] shadow-[0_10px_20px_rgba(0,210,255,0.3)] hover:translate-y-[-2px] hover:shadow-[0_15px_30px_rgba(0,210,255,0.4)] transition-all duration-300"
                    >
                        Try Prediction
                    </button>
                    <button
                        onClick={() => setActiveSection("learning")}
                        className="px-8 py-3 rounded-full text-white font-semibold bg-white/10 border border-white/20 hover:bg-white/20 transition-all duration-300 backdrop-blur-sm"
                    >
                        Start Learning
                    </button>
                </div>
            </div>

            {/* Right Visual - Glass Card */}
            <div className="flex-1 flex justify-center items-center animate-fade-in delay-100">
                <div className="relative w-[400px] h-[400px] bg-white/5 border border-white/10 rounded-3xl backdrop-blur-xl flex flex-col items-center justify-center p-8 shadow-2xl skew-y-[-2deg] hover:skew-y-0 transition-transform duration-500">
                    <div className="absolute inset-0 bg-gradient-to-br from-[#00d2ff]/10 to-transparent rounded-3xl pointer-events-none" />
                    <Hand size={120} className="text-[#00d2ff] mb-6 drop-shadow-[0_0_15px_rgba(0,210,255,0.5)]" />
                    <h2 className="text-3xl font-bold text-white mb-2">Sign Language</h2>
                    <p className="text-[#f8fafc]/70 text-lg">AI-Powered Recognition</p>
                </div>
            </div>
        </div>
    );
};

export default Hero;
