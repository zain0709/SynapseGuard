import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Receipt, FileText, Wallet, Settings, LogOut } from 'lucide-react';

const Sidebar = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const isActive = (path) => location.pathname === path;

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
        { icon: Receipt, label: 'Transactions', path: '/transactions' }, // Placeholder
        { icon: FileText, label: 'Reports', path: '/reports' }, // Placeholder
        { icon: Wallet, label: 'Budgets', path: '/budgets' }, // Placeholder
        { icon: Settings, label: 'Settings', path: '/settings' }, // Placeholder
    ];

    return (
        <div className="w-64 bg-white border-r border-gray-100 h-screen fixed left-0 top-0 flex flex-col">
            <div className="p-8">
                <Link to="/" className="text-2xl font-bold text-primary tracking-tight flex items-center gap-2">
                    <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
                        S
                    </div>
                    Synapse
                </Link>
            </div>

            <nav className="flex-1 px-4 space-y-2">
                {navItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive(item.path)
                                ? 'bg-primary/10 text-primary font-semibold'
                                : 'text-gray-500 hover:bg-gray-50 hover:text-dark'
                            }`}
                    >
                        <item.icon size={20} />
                        {item.label}
                    </Link>
                ))}
            </nav>

            <div className="p-4 border-t border-gray-100">
                <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-3 w-full text-gray-500 hover:bg-red-50 hover:text-red-500 rounded-xl transition-all duration-200"
                >
                    <LogOut size={20} />
                    Logout
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
