import { useState, useEffect, useRef } from 'react';
import { Camera, StopCircle, PlayCircle } from 'lucide-react';

const Prediction = () => {
    const [isStreaming, setIsStreaming] = useState(false);
    const [prediction, setPrediction] = useState('...');
    const [confidence, setConfidence] = useState('0%');
    const intervalRef = useRef(null);

    const startStream = () => {
        setIsStreaming(true);
        intervalRef.current = setInterval(fetchPrediction, 500);
    };

    const stopStream = () => {
        setIsStreaming(false);
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
        setPrediction('...');
        setConfidence('0%');
    };

    const fetchPrediction = async () => {
        try {
            const res = await fetch('/get_prediction');
            const data = await res.json();
            setPrediction(data.sentence);
            setConfidence(data.accuracy);
        } catch (err) {
            console.error('Fetch error:', err);
        }
    };

    useEffect(() => {
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, []);

    return (
        <div className="flex flex-col items-center justify-center min-h-[90vh] py-16 px-4">
            <h2 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500 mb-2">
                Real-time Prediction
            </h2>
            <p className="text-slate-400 mb-8">Face the camera and perform signs to see instant translation.</p>

            <div className="flex flex-col lg:flex-row gap-8 w-full max-w-[95vw]">
                {/* Video Feed Area */}
                <div className="relative flex-1 bg-black rounded-3xl overflow-hidden shadow-2xl border-2 border-cyan-500/30 aspect-video">
                    {isStreaming ? (
                        <img
                            src="/video_feed"
                            alt="Live Feed"
                            className="w-full h-full object-cover"
                        />
                    ) : (
                        <div className="flex flex-col items-center justify-center w-full h-full text-slate-600 bg-slate-900">
                            <Camera size={64} className="mb-4 opacity-50" />
                            <p>Camera is off</p>
                        </div>
                    )}

                    {/* Overlay */}
                    <div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-md rounded-xl p-4 flex justify-between items-center border border-white/10">
                        <div>
                            <span className="text-sm text-slate-400 block">Output</span>
                            <span className="text-xl font-bold text-cyan-400">{prediction}</span>
                        </div>
                        <div className="text-right">
                            <span className="text-sm text-slate-400 block">Confidence</span>
                            <span className="text-lg font-semibold text-white">{confidence}</span>
                        </div>
                    </div>
                </div>

                {/* Controls & Instructions */}
                <div className="w-full lg:w-96 flex flex-col gap-6">
                    <div className="bg-slate-800/50 p-6 rounded-2xl border border-white/5 backdrop-blur-sm">
                        <h3 className="text-xl font-semibold text-white mb-4">Instructions</h3>
                        <ul className="space-y-3 text-slate-300 text-sm">
                            <li className="flex gap-2">
                                <span className="text-cyan-400">•</span> Place your hand within the frame.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-cyan-400">•</span> Hold the sign steady for 1-2 seconds.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-cyan-400">•</span> Ensure good lighting for accuracy.
                            </li>
                        </ul>
                    </div>

                    <button
                        onClick={startStream}
                        disabled={isStreaming}
                        className={`flex items-center justify-center gap-2 py-4 rounded-full font-bold transition-all ${isStreaming
                            ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                            : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:shadow-[0_0_20px_rgba(6,182,212,0.5)] transform hover:-translate-y-1'
                            }`}
                    >
                        <PlayCircle size={20} />
                        Start Prediction
                    </button>

                    <button
                        onClick={stopStream}
                        disabled={!isStreaming}
                        className={`flex items-center justify-center gap-2 py-4 rounded-full font-bold transition-all border border-white/10 ${!isStreaming
                            ? 'bg-slate-800 text-slate-600 cursor-not-allowed'
                            : 'bg-red-500/20 text-red-400 hover:bg-red-500/30 hover:border-red-500/50'
                            }`}
                    >
                        <StopCircle size={20} />
                        Stop Prediction
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Prediction;
