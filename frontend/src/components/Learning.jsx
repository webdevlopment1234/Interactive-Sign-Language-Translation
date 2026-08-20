import React, { useEffect, useState } from 'react';

const Learning = () => {
    const [actions, setActions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/actions')
            .then((res) => res.json())
            .then((data) => {
                setActions(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Failed to fetch actions', err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="min-h-screen py-24 px-8 md:px-20 text-white">
            <div className="text-center mb-16 animate-fade-in">
                <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500">
                    Learning Center
                </h2>
                <p className="text-slate-400 text-lg max-w-2xl mx-auto">
                    Master the basics by exploring the sign library. Each card shows the gesture for a specific letter or number.
                </p>
            </div>

            {loading ? (
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
                    {[...Array(10)].map((_, i) => (
                        <div key={i} className="h-48 bg-slate-800/50 rounded-2xl animate-pulse" />
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8">
                    {actions.map((action, index) => (
                        <div
                            key={action}
                            className="group relative bg-slate-800/30 backdrop-blur-sm border border-white/5 rounded-2xl p-4 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-[0_0_20px_rgba(6,182,212,0.3)] hover:bg-slate-800/50"
                            style={{ animationDelay: `${index * 50}ms` }}
                        >
                            <div className="aspect-square bg-black/40 rounded-xl overflow-hidden mb-4 border border-white/5 flex items-center justify-center">
                                <img
                                    src={`/static/images/${action}/0.png`}
                                    alt={`Sign for ${action}`}
                                    className="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500"
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = 'https://via.placeholder.com/150/0f172a/ffffff?text=?'; // Fallback
                                    }}
                                />
                            </div>
                            <h3 className="text-2xl font-bold text-center text-cyan-400 group-hover:text-cyan-300">
                                {action}
                            </h3>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Learning;
