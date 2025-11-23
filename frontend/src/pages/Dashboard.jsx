import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [budgets, setBudgets] = useState([]);
    const [newBudgetName, setNewBudgetName] = useState('');
    const [newBudgetLimit, setNewBudgetLimit] = useState('');
    const [loading, setLoading] = useState(true);

    const token = localStorage.getItem('token');
    const authHeader = { headers: { Authorization: `Bearer ${token}` } };

    useEffect(() => {
        fetchBudgets();
    }, []);

    const fetchBudgets = async () => {
        try {
            const response = await axios.get('http://localhost:8001/budgets/', authHeader);
            setBudgets(response.data);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching budgets", error);
            setLoading(false);
        }
    };

    const handleCreateBudget = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8001/budgets/', {
                name: newBudgetName,
                limit: parseFloat(newBudgetLimit)
            }, authHeader);
            setNewBudgetName('');
            setNewBudgetLimit('');
            fetchBudgets();
        } catch (error) {
            console.error("Error creating budget", error);
        }
    };

    const handleAddExpense = async (budgetId, description, amount, category) => {
        try {
            await axios.post(`http://localhost:8001/budgets/${budgetId}/expenses/`, {
                description,
                amount: parseFloat(amount),
                category
            }, authHeader);
            fetchBudgets();
        } catch (error) {
            console.error("Error adding expense", error);
        }
    };

    const handleUpdateExpense = async (budgetId, expenseId, description, amount, category) => {
        try {
            await axios.put(`http://localhost:8001/budgets/${budgetId}/expenses/${expenseId}`, {
                description,
                amount: parseFloat(amount),
                category
            }, authHeader);
            fetchBudgets();
        } catch (error) {
            console.error("Error updating expense", error);
        }
    };

    const handleDeleteExpense = async (budgetId, expenseId) => {
        try {
            await axios.delete(`http://localhost:8001/budgets/${budgetId}/expenses/${expenseId}`, authHeader);
            fetchBudgets();
        } catch (error) {
            console.error("Error deleting expense", error);
        }
    };

    const handleUpdateBudget = async (budgetId, name, limit) => {
        try {
            await axios.put(`http://localhost:8001/budgets/${budgetId}`, {
                name,
                limit: parseFloat(limit)
            }, authHeader);
            fetchBudgets();
        } catch (error) {
            console.error("Error updating budget", error);
        }
    };

    const handleDeleteBudget = async (budgetId) => {
        if (window.confirm('Are you sure you want to delete this budget? This will also delete all expenses.')) {
            try {
                await axios.delete(`http://localhost:8001/budgets/${budgetId}`, authHeader);
                fetchBudgets();
            } catch (error) {
                console.error("Error deleting budget", error);
            }
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-gray-900"></div>
        </div>
    );

    // Calculate statistics
    const totalBudgets = budgets.length;
    const totalBudgetLimit = budgets.reduce((sum, budget) => sum + budget.limit, 0);
    const totalSpending = budgets.reduce((sum, budget) => {
        const budgetSpending = budget.expenses.reduce((expSum, exp) => expSum + exp.amount, 0);
        return sum + budgetSpending;
    }, 0);
    const totalRemaining = totalBudgetLimit - totalSpending;
    const avgBudgetUsage = totalBudgetLimit > 0 ? ((totalSpending / totalBudgetLimit) * 100).toFixed(1) : 0;

    return (
        <div className="max-w-7xl mx-auto px-4">
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-black mb-1">My Budgets</h1>
                <p className="text-gray-500 text-sm">Track and manage your spending</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                {/* Total Budgets Card */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium mb-1">Total Budgets</p>
                            <p className="text-3xl font-bold text-black">{totalBudgets}</p>
                        </div>
                    </div>
                </div>

                {/* Total Spending Card */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium mb-1">Total Spending</p>
                            <p className="text-3xl font-bold text-red-600">${totalSpending.toLocaleString()}</p>
                        </div>
                    </div>
                </div>

                {/* Remaining Budget Card */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium mb-1">Remaining Budget</p>
                            <p className={`text-3xl font-bold ${totalRemaining < 0 ? 'text-red-600' : 'text-green-600'}`}>
                                ${Math.abs(totalRemaining).toLocaleString()}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Monthly Overview Card */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium mb-1">Budget Usage</p>
                            <p className={`text-3xl font-bold ${avgBudgetUsage >= 100 ? 'text-red-600' :
                                avgBudgetUsage >= 75 ? 'text-orange-500' :
                                    'text-green-600'
                                }`}>
                                {avgBudgetUsage}%
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm mb-6 border border-gray-200">
                <h2 className="text-lg font-bold mb-4 text-black">Create New Budget</h2>
                <form onSubmit={handleCreateBudget} className="flex flex-col md:flex-row gap-3">
                    <input
                        type="text"
                        placeholder="Budget Name (e.g., Groceries)"
                        value={newBudgetName}
                        onChange={(e) => setNewBudgetName(e.target.value)}
                        className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 transition-all bg-white text-sm"
                        required
                    />
                    <input
                        type="number"
                        placeholder="Limit"
                        value={newBudgetLimit}
                        onChange={(e) => setNewBudgetLimit(e.target.value)}
                        className="w-full md:w-32 px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 transition-all bg-white text-sm"
                        required
                    />
                    <button
                        type="submit"
                        className="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-black transition-all text-sm"
                    >
                        Create Budget
                    </button>
                </form>
            </div>

            <div className="grid gap-4">
                {budgets.map((budget) => (
                    <BudgetCard
                        key={budget.id}
                        budget={budget}
                        onAddExpense={handleAddExpense}
                        onUpdateExpense={handleUpdateExpense}
                        onDeleteExpense={handleDeleteExpense}
                        onUpdateBudget={handleUpdateBudget}
                        onDeleteBudget={handleDeleteBudget}
                    />
                ))}
            </div>
        </div>
    );
};

const BudgetCard = ({ budget, onAddExpense, onUpdateExpense, onDeleteExpense, onUpdateBudget, onDeleteBudget }) => {
    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [category, setCategory] = useState('General');
    const [isExpanded, setIsExpanded] = useState(false);
    const [showExpenses, setShowExpenses] = useState(false);
    const [editingExpense, setEditingExpense] = useState(null);
    const [editingBudget, setEditingBudget] = useState(false);
    const [editBudgetName, setEditBudgetName] = useState(budget.name);
    const [editBudgetLimit, setEditBudgetLimit] = useState(budget.limit);

    const totalExpenses = budget.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const remaining = budget.limit - totalExpenses;
    const percentUsed = Math.min((totalExpenses / budget.limit) * 100, 100);

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddExpense(budget.id, description, amount, category);
        setDescription('');
        setAmount('');
        setCategory('General');
    };

    const handleEditExpense = (expense) => {
        setEditingExpense({
            id: expense.id,
            description: expense.description,
            amount: expense.amount,
            category: expense.category
        });
    };

    const handleSaveEdit = () => {
        if (editingExpense) {
            onUpdateExpense(
                budget.id,
                editingExpense.id,
                editingExpense.description,
                editingExpense.amount,
                editingExpense.category
            );
            setEditingExpense(null);
        }
    };

    const handleCancelEdit = () => {
        setEditingExpense(null);
    };

    const handleSaveBudgetEdit = () => {
        onUpdateBudget(budget.id, editBudgetName, editBudgetLimit);
        setEditingBudget(false);
    };

    const handleCancelBudgetEdit = () => {
        setEditBudgetName(budget.name);
        setEditBudgetLimit(budget.limit);
        setEditingBudget(false);
    };

    return (
        <div className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden border border-gray-200">
            {/* Compact Header - Always Visible */}
            <div
                className="p-5 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => !editingBudget && setIsExpanded(!isExpanded)}
            >
                <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3 flex-1">
                        <span className={`transform transition-transform duration-200 text-gray-400 ${isExpanded ? 'rotate-90' : ''}`}>
                            ▶
                        </span>
                        {editingBudget ? (
                            <div className="flex gap-2 flex-1" onClick={(e) => e.stopPropagation()}>
                                <input
                                    type="text"
                                    value={editBudgetName}
                                    onChange={(e) => setEditBudgetName(e.target.value)}
                                    className="px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 text-sm"
                                />
                                <input
                                    type="number"
                                    value={editBudgetLimit}
                                    onChange={(e) => setEditBudgetLimit(e.target.value)}
                                    className="w-32 px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 text-sm"
                                />
                                <button onClick={handleSaveBudgetEdit} className="px-3 py-1.5 bg-gray-900 text-white rounded-lg hover:bg-black text-sm">Save</button>
                                <button onClick={handleCancelBudgetEdit} className="px-3 py-1.5 bg-gray-400 text-white rounded-lg hover:bg-gray-500 text-sm">Cancel</button>
                            </div>
                        ) : (
                            <div>
                                <h3 className="text-lg font-bold text-black">{budget.name}</h3>
                                <p className="text-xs text-gray-500">Budget Limit: ${budget.limit.toLocaleString()}</p>
                            </div>
                        )}
                    </div>
                    <div className="flex items-center gap-3">
                        <div className="text-right">
                            <p className={`text-2xl font-bold ${remaining < 0 ? 'text-red-600' : 'text-green-600'}`}>
                                ${Math.abs(remaining).toLocaleString()}
                            </p>
                            <p className="text-xs text-gray-500">{remaining < 0 ? 'Over Budget' : 'Remaining'}</p>
                        </div>
                        {!editingBudget && (
                            <div className="flex gap-1" onClick={(e) => e.stopPropagation()}>
                                <button
                                    onClick={() => setEditingBudget(true)}
                                    className="p-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all"
                                    title="Edit Budget"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                </button>
                                <button
                                    onClick={() => onDeleteBudget(budget.id)}
                                    className="p-1.5 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-all"
                                    title="Delete Budget"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* Compact Progress Bar */}
                <div className="mt-3">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>${totalExpenses.toLocaleString()} spent</span>
                        <span>{percentUsed.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div
                            className={`h-2 rounded-full transition-all duration-500 ${percentUsed >= 100 ? 'bg-red-500' :
                                percentUsed >= 75 ? 'bg-orange-400' :
                                    'bg-gray-900'
                                }`}
                            style={{ width: `${percentUsed}%` }}
                        ></div>
                    </div>
                </div>
            </div>

            {/* Expanded Content */}
            {isExpanded && (
                <div className="px-5 pb-5 border-t border-gray-100">
                    {/* Add Expense Form */}
                    <form onSubmit={handleSubmit} className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <h4 className="font-bold text-black mb-3 text-sm">Add Expense</h4>
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                            <input
                                type="text"
                                placeholder="Description"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 transition-all bg-white text-sm"
                                required
                            />
                            <input
                                type="number"
                                step="0.01"
                                placeholder="Amount"
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 transition-all bg-white text-sm"
                                required
                            />
                            <select
                                value={category}
                                onChange={(e) => setCategory(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 transition-all bg-white text-sm"
                            >
                                <option>General</option>
                                <option>Food</option>
                                <option>Transport</option>
                                <option>Utilities</option>
                                <option>Entertainment</option>
                            </select>
                            <button
                                type="submit"
                                className="bg-gray-900 text-white px-4 py-2 rounded-lg font-medium hover:bg-black transition-all text-sm"
                            >
                                Add
                            </button>
                        </div>
                    </form>

                    {/* Expenses List */}
                    <div className="mt-4">
                        <button
                            onClick={() => setShowExpenses(!showExpenses)}
                            className="flex items-center gap-2 text-gray-900 hover:text-black font-semibold mb-2 transition-colors text-sm"
                        >
                            <span className={`transform transition-transform ${showExpenses ? 'rotate-90' : ''}`}>▶</span>
                            {budget.expenses.length} Expenses
                        </button>

                        {showExpenses && (
                            <div className="space-y-2 mt-3">
                                {budget.expenses.length === 0 ? (
                                    <p className="text-gray-400 text-center py-6 bg-gray-50 rounded-lg text-sm">No expenses yet</p>
                                ) : (
                                    budget.expenses.map((expense) => (
                                        <div key={expense.id}>
                                            {editingExpense && editingExpense.id === expense.id ? (
                                                <div className="p-4 bg-gray-50 rounded-lg border border-gray-300">
                                                    <div className="grid grid-cols-1 md:grid-cols-4 gap-2 mb-2">
                                                        <input
                                                            type="text"
                                                            value={editingExpense.description}
                                                            onChange={(e) => setEditingExpense({ ...editingExpense, description: e.target.value })}
                                                            className="px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 text-sm"
                                                        />
                                                        <input
                                                            type="number"
                                                            step="0.01"
                                                            value={editingExpense.amount}
                                                            onChange={(e) => setEditingExpense({ ...editingExpense, amount: e.target.value })}
                                                            className="px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 text-sm"
                                                        />
                                                        <select
                                                            value={editingExpense.category}
                                                            onChange={(e) => setEditingExpense({ ...editingExpense, category: e.target.value })}
                                                            className="px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-900 text-sm"
                                                        >
                                                            <option>General</option>
                                                            <option>Food</option>
                                                            <option>Transport</option>
                                                            <option>Utilities</option>
                                                            <option>Entertainment</option>
                                                        </select>
                                                        <div className="flex gap-2">
                                                            <button
                                                                onClick={handleSaveEdit}
                                                                className="flex-1 bg-gray-900 text-white px-3 py-1.5 rounded-lg hover:bg-black transition-all text-sm font-medium"
                                                            >
                                                                Save
                                                            </button>
                                                            <button
                                                                onClick={handleCancelEdit}
                                                                className="flex-1 bg-gray-400 text-white px-3 py-1.5 rounded-lg hover:bg-gray-500 transition-all text-sm font-medium"
                                                            >
                                                                Cancel
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="flex justify-between items-center p-3 bg-white rounded-lg hover:bg-gray-50 transition-all border border-gray-200">
                                                    <div className="flex-1">
                                                        <p className="font-medium text-gray-900 text-sm">{expense.description}</p>
                                                        <span className="inline-block px-2 py-0.5 bg-gray-100 rounded-full text-xs text-gray-600 mt-1">
                                                            {expense.category}
                                                        </span>
                                                    </div>
                                                    <div className="flex items-center gap-3">
                                                        <p className="font-semibold text-gray-900 text-base">-${expense.amount.toLocaleString()}</p>
                                                        <div className="flex gap-1">
                                                            <button
                                                                onClick={() => handleEditExpense(expense)}
                                                                className="p-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all"
                                                                title="Edit"
                                                            >
                                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                                                </svg>
                                                            </button>
                                                            <button
                                                                onClick={() => onDeleteExpense(budget.id, expense.id)}
                                                                className="p-1.5 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-all"
                                                                title="Delete"
                                                            >
                                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                                </svg>
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    ))
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
