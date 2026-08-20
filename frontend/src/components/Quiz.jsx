import React, { useState, useEffect } from 'react';

const Quiz = () => {
    const [actions, setActions] = useState(['A', 'B', 'C', '0', '1', '2']);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(false);
    const [score, setScore] = useState(0);

    useEffect(() => {
        fetch('/api/actions')
            .then((res) => res.json())
            .then((data) => {
                setActions(data);
                generateQuestion(data);
            })
            .catch((err) => {
                console.error('Failed to fetch actions', err);
                generateQuestion(actions); // Fallback
            });
    }, []);

    const generateQuestion = (list) => {
        if (!list || list.length < 2) return;
        const correct = list[Math.floor(Math.random() * list.length)];
        let options = [correct];
        while (options.length < 4) {
            const distractor = list[Math.floor(Math.random() * list.length)];
            if (!options.includes(distractor)) options.push(distractor);
        }
        // Shuffle options
        options = options.sort(() => Math.random() - 0.5);
        setCurrentQuestion({ correct, options });
        setSelectedOption(null);
        setIsCorrect(false);
    };

    const handleAnswer = (option) => {
        if (selectedOption) return; // Prevent multiple clicks
        setSelectedOption(option);
        if (option === currentQuestion.correct) {
            setIsCorrect(true);
            setScore(score + 1);
        } else {
            setIsCorrect(false);
        }
    };

    const handleNext = () => {
        generateQuestion(actions);
    };

    if (!currentQuestion) return <div className="text-center text-white p-20">Loading Quiz...</div>;

    return (
        <div className="flex flex-col items-center justify-center min-h-[90vh] py-16 px-4">
            <div className="text-center mb-8">
                <h2 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500">
                    Challenge Quiz
                </h2>
                <p className="text-slate-400">Can you identify the sign correctly?</p>
                <div className="mt-4 text-sm text-slate-500 font-mono">
                    Score: <span className="text-cyan-400 text-lg">{score}</span>
                </div>
            </div>

            <div className="w-full max-w-md bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl flex flex-col items-center gap-8">
                {/* Question Image */}
                <div className="w-64 h-64 bg-black/40 rounded-2xl overflow-hidden border-2 border-slate-700/50 relative group">
                    <img
                        src={`/static/images/${currentQuestion.correct}/0.png`}
                        alt="Identify this sign"
                        className="w-full h-full object-contain p-4 transition-transform duration-500 group-hover:scale-105"
                        onError={(e) => { e.target.src = 'https://via.placeholder.com/300x300?text=Sign'; }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none" />
                </div>

                {/* Options Grid */}
                <div className="grid grid-cols-2 gap-4 w-full">
                    {currentQuestion.options.map((option) => {
                        let btnClass = "py-4 rounded-xl font-bold transition-all duration-300 transform hover:scale-[1.02] active:scale-95 border border-white/5 bg-slate-700/50 hover:bg-slate-600/50 text-slate-200";

                        if (selectedOption) {
                            if (option === currentQuestion.correct) {
                                btnClass = "py-4 rounded-xl font-bold bg-green-500/20 border-green-500 text-green-400 shadow-[0_0_15px_rgba(34,197,94,0.3)]";
                            } else if (option === selectedOption && option !== currentQuestion.correct) {
                                btnClass = "py-4 rounded-xl font-bold bg-red-500/20 border-red-500 text-red-400";
                            } else {
                                btnClass = "py-4 rounded-xl font-bold bg-slate-800/30 text-slate-500 opacity-50 cursor-not-allowed";
                            }
                        }

                        return (
                            <button
                                key={option}
                                onClick={() => handleAnswer(option)}
                                disabled={!!selectedOption}
                                className={btnClass}
                            >
                                {option}
                            </button>
                        );
                    })}
                </div>

                {/* Feedback & Next Button */}
                {selectedOption && (
                    <div className="w-full flex flex-col items-center animate-fade-in gap-4 mt-2">
                        <div className={`text-xl font-bold ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                            {isCorrect ? 'Correct! Well done.' : `Incorrect. It was ${currentQuestion.correct}.`}
                        </div>

                        <button
                            onClick={handleNext}
                            className="px-8 py-3 w-full rounded-full font-bold text-white bg-gradient-to-r from-cyan-500 to-blue-600 shadow-lg hover:shadow-cyan-500/25 transition-all transform hover:-translate-y-1"
                        >
                            Next Question
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Quiz;
