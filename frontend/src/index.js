import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

const API_URL = ''; // your backend URL if needed

export default function App() {
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState('');
    const [health, setHealth] = useState('checking...');
    const [editingId, setEditingId] = useState(null);
    const [editingText, setEditingText] = useState('');

    useEffect(() => {
        fetch(`${API_URL}/`)
            .then(res => setHealth(res.ok ? 'healthy' : 'unhealthy'))
            .catch(() => setHealth('unreachable'));
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        try {
            const res = await fetch(`${API_URL}/twi/`);
            if (!res.ok) {
                console.error('fetchTwi: bad response', res.status);
                setTodos([]);
                return;
            }
            const data = await res.json();
            setTodos(Array.isArray(data) ? data : []);
        } catch (e) {
            console.error('Error fetching twi', e);
            setTodos([]);
        }
    };

    const addTodo = async () => {
        if (!newTodo.trim()) return;
        await fetch(`${API_URL}/twi/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_text: newTodo }),
        });
        setNewTodo('');
        fetchTodos();
    };

    const deleteTodo = async (id) => {
        await fetch(`${API_URL}/twi/${id}/`, { method: 'DELETE' });
        fetchTodos();
    };

    const startEditing = (id, post_text) => {
        setEditingId(id);
        setEditingText(post_text);
    };

    const cancelEditing = () => {
        setEditingId(null);
        setEditingText('');
    };

    const saveEdit = async (id) => {
        await fetch(`${API_URL}/twi/${id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_text: editingText }),
        });
        setEditingId(null);
        setEditingText('');
        fetchTodos();
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
            <div className="w-full max-w-md bg-white rounded-2xl shadow p-6">
                <h1 className="text-2xl font-bold mb-2">Twi Posts</h1>
                <p className="text-sm text-gray-500 mb-4">
                    Backend health:{' '}
                    <span className={health === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                        {health}
                    </span>
                </p>

                <div className="flex mb-4">
                    <input
                        value={newTodo}
                        onChange={(e) => setNewTodo(e.target.value)}
                        placeholder="Add new twi..."
                        className="flex-grow border border-gray-300 rounded-l-lg px-3 py-2 focus:outline-none"
                    />
                    <button
                        onClick={addTodo}
                        className="bg-blue-600 text-white px-4 rounded-r-lg hover:bg-blue-700"
                    >
                        Add
                    </button>
                </div>

                <ul>
                    {(Array.isArray(todos) ? todos : []).map((t) => (
                        <li
                            key={t.id}
                            className="flex justify-between items-center py-2 border-b border-gray-200"
                        >
                            {editingId === t.id ? (
                                <div className="flex flex-grow items-center">
                                    <input
                                        value={editingText}
                                        onChange={(e) => setEditingText(e.target.value)}
                                        className="flex-grow border border-gray-300 rounded px-2 py-1 focus:outline-none"
                                        autoFocus
                                    />
                                    <button
                                        onClick={() => saveEdit(t.id)}
                                        className="ml-2 text-green-600 hover:text-green-800"
                                    >
                                        ✓
                                    </button>
                                    <button
                                        onClick={cancelEditing}
                                        className="ml-1 text-gray-500 hover:text-gray-700"
                                    >
                                        ✕
                                    </button>
                                </div>
                            ) : (
                                <>
                                    <span
                                        className={`flex-grow cursor-pointer ${t.done ? 'line-through text-gray-400' : ''
                                            }`}
                                    >
                                        {t.post_text}
                                    </span>
                                    <button
                                        onClick={() => startEditing(t.id, t.post_text)}
                                        className="text-blue-500 hover:text-blue-700 mr-2"
                                    >
                                        ✎
                                    </button>
                                    <button
                                        onClick={() => deleteTodo(t.id)}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        ×
                                    </button>
                                </>
                            )}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

if (typeof document !== 'undefined') {
    const el = document.getElementById('root');
    if (el) {
        const root = ReactDOM.createRoot(el);
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );
    }
}
