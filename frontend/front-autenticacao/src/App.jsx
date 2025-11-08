import { useState } from 'react'
import './App.css'
import Login from './Login'
import Registro from './Registro'

function App() {
  const [showLogin, setShowLogin] = useState(true)

  return (
    <div className="App">
      <div className="toggle-container">
        <button
          className={showLogin ? 'active' : ''}
          onClick={() => setShowLogin(true)}
        >
          Login
        </button>
        <button
          className={!showLogin ? 'active' : ''}
          onClick={() => setShowLogin(false)}
        >
          Registro
        </button>
      </div>

      {showLogin ? <Login /> : <Registro />}
    </div>
  )
}

export default App
