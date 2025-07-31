// src/App.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import './index.css';

// !!! あなたのRenderのAPI URLに書き換えてください !!!
const API_BASE_URL = 'https://todo-api-0f44.onrender.com';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [newSubtaskName, setNewSubtaskName] = useState({});

  // 起動時と検索時にTODOリストを読み込む
  useEffect(() => {
    fetchTodos();
  }, [searchTerm]);

  const fetchTodos = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/todos/`, {
        params: { search: searchTerm }
      });
      setTodos(response.data);
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;
    try {
      await axios.post(`${API_BASE_URL}/todos/`, { title: newTodoTitle });
      setNewTodoTitle('');
      fetchTodos();
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/todos/${id}/`);
      fetchTodos();
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  const handleToggleComplete = async (todo) => {
    try {
      await axios.patch(`${API_BASE_URL}/todos/${todo.id}/`, { completed: !todo.completed });
      fetchTodos();
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  };

  const handleAddSubtask = async (e, todoId) => {
    e.preventDefault();
    const subtaskName = newSubtaskName[todoId];
    if (!subtaskName || !subtaskName.trim()) return;
    try {
      await axios.post(`${API_BASE_URL}/todos/${todoId}/subtasks/`, { name: subtaskName });
      setNewSubtaskName({ ...newSubtaskName, [todoId]: '' });
      fetchTodos();
    } catch (error) {
      console.error("Error adding subtask:", error);
    }
  };

  return (
    <div className="App">
      <h1>FastAPI & React TODO App</h1>

      <div className="search-form">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="TODOを検索..."
        />
      </div>

      <form onSubmit={handleAddTodo} className="add-form">
        <input
          type="text"
          value={newTodoTitle}
          onChange={(e) => setNewTodoTitle(e.target.value)}
          placeholder="新しいTODOを入力"
        />
        <button type="submit">追加</button>
      </form>

      <ul className="todo-list">
        {todos.map(todo => (
          <div key={todo.id}>
            <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
              <span onClick={() => handleToggleComplete(todo)}>
                {todo.title}
              </span>
              <button onClick={() => handleDeleteTodo(todo.id)} className="delete-btn">削除</button>
            </li>
            {todo.subtasks && todo.subtasks.length > 0 && (
              <ul className="subtask-list">
                {todo.subtasks.map(subtask => (
                  <li key={subtask.id}>{subtask.name}</li>
                ))}
              </ul>
            )}
            <form onSubmit={(e) => handleAddSubtask(e, todo.id)} className="subtask-form">
              <input
                type="text"
                value={newSubtaskName[todo.id] || ''}
                onChange={(e) => setNewSubtaskName({ ...newSubtaskName, [todo.id]: e.target.value })}
                placeholder="子タスクを追加"
              />
              <button type="submit">ステップ追加</button>
            </form>
          </div>
        ))}
      </ul>
    </div>
  );
}

export default App;