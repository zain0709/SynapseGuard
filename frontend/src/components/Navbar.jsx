import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <nav className="bg-card shadow-sm border-b border-gray-100">
            <div className="container mx-auto px-6">
                <div className="flex justify-between items-center h-20">
                    <Link to="/" className="text-2xl font-bold text-black tracking-tight">
                        SynapseGuard
                    </Link>
                    <div className="flex items-center space-x-6">
                        {token ? (
                            <>
                                <Link to="/dashboard" className="text-gray-600 hover:text-black font-medium transition-colors">
                                    Dashboard
                                </Link>
                                <button
                                    onClick={handleLogout}
                                    className="text-gray-600 hover:text-black font-medium transition-colors"
                                >
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="text-gray-600 hover:text-primary font-medium transition-colors">
                                    Login
                                </Link>
                                <Link to="/register" className="bg-gray-900 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-black transition-all">
                                    Register
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
