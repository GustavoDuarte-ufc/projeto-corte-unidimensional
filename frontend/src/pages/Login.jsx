import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import "../components/CutOptimizer.css";

export default function Login() {
  const navigate = useNavigate();
  const { signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await signIn({ email, password });
      navigate("/cut-optimizer");
    } catch {
      alert("Login inválido");
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-badge">Corte Unidimensional</div>
        <h1>Entrar na plataforma</h1>
        <p>Gmail: <strong>teste@gmail.com</strong> e Senha: <strong>12345678</strong></p>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Entrar</button>
        </form>
      </div>
    </div>
  );
}