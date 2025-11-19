import { useState } from 'react';
import './Login.css';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validação básica
    if (!formData.username || !formData.password) {
      setError('Todos os campos são obrigatórios');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('Login realizado com sucesso!');

        // Armazenar o token no localStorage
        if (data.token) {
          localStorage.setItem('token', data.token);
        }

        // Limpar o formulário
        setFormData({
          username: 'Deu certo!!!',
          password: ''
        });

        // Aqui você pode redirecionar o usuário ou atualizar o estado global
        console.log('Login successful:', data);
      } else {
        const errorData = await response.json();
        setError(errorData.mensagem || errorData.message || 'Credenciais inválidas');
      }
    } catch (err) {
      console.error('Erro completo:', err);
      setError('Erro de conexão com o servidor: ' + err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Nome de Usuário:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}

export default Login;
