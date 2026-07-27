import { useAuth } from '../contexts/AuthContext';

export default function BoardListPage() {
  const { user, logout } = useAuth();

  return (
    <div className="dashboard">
      <header className="topbar">
        <h1 className="topbar-title">Boards</h1>
        <div className="topbar-user">
          <span>{user?.username}</span>
          <button className="btn-secondary btn-sm" onClick={logout}>
            Logout
          </button>
        </div>
      </header>
      <main className="content">
        <p className="empty-message">Keine Boards vorhanden</p>
      </main>
    </div>
  );
}
