import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function BoardPage() {
  const { id } = useParams<{ id: string }>();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <header className="topbar">
        <h1 className="topbar-title">
          <button className="btn-back" onClick={() => navigate('/')}>
            &larr;
          </button>{' '}
          Board {id}
        </h1>
        <div className="topbar-user">
          <span>{user?.username}</span>
          <button className="btn-secondary btn-sm" onClick={logout}>
            Logout
          </button>
        </div>
      </header>
      <main className="content">
        <p className="empty-message">Board-Inhalt folgt in Ticket #3</p>
      </main>
    </div>
  );
}
