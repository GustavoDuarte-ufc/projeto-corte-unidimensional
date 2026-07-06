import { useAuth } from "../hooks/useAuth";
import { Link } from "react-router-dom";
import "../components/CutOptimizer.css";

export default function Dashboard() {
  const { user, signOut } = useAuth();

  return (
    <div className="dashboard-page">
      <div className="dashboard-card">
        <div className="auth-badge">Painel</div>
        <h1>Bem-vindo, {user?.name || "usuário"}</h1>
        <p className="dashboard-subtitle">{user?.email}</p>

        <div className="dashboard-actions">
          <Link to="/cut-optimizer" className="dashboard-link optimizer">
            Acessar Solver
          </Link>
        </div>

        <button onClick={signOut} className="btn-logout">
          Sair
        </button>
      </div>
    </div>
  );
}