import { useState } from 'react';
import './Registro.css';

function Registro() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    perfil: 'admin',
    password: ''
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const perfis = [
    { value: 'admin', label: 'Administrador' },
    { value: 'professor', label: 'Professor' },
    { value: 'aluno', label: 'Aluno' },
    { value: 'coordenador', label: 'Coordenador' },
    { value: 'diretor', label: 'Diretor' }
  ];

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
    if (!formData.username || !formData.email || !formData.password) {
      setError('Todos os campos são obrigatórios');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/auth/registro/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('Usuário registrado com sucesso!');
        setFormData({
          username: '',
          email: '',
          perfil: 'admin',
          password: ''
        });
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Erro ao registrar usuário');
      }
    } catch (err) {
      setError('Erro de conexão com o servidor');
    }
  };

  return (
    <div className="registro-container">
      <h2>Registro de Usuário</h2>
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
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="perfil">Perfil:</label>
          <select
            id="perfil"
            name="perfil"
            value={formData.perfil}
            onChange={handleChange}
            required
          >
            {perfis.map((perfil) => (
              <option key={perfil.value} value={perfil.value}>
                {perfil.label}
              </option>
            ))}
          </select>
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

        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default Registro;
