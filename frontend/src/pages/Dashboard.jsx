import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

const actions = [
  ["🚆", "Search Train", "Find real-time routes and availability.", "/search-train"],
  ["👤", "Passenger Details", "Store traveler information once.", "/passenger-details"],
  ["📄", "My Bookings", "Review or cancel reservations.", "/my-bookings"],
  ["💳", "Payment", "Complete pending payments quickly.", "/payment"],
  ["🎟", "My Tickets", "Download confirmed ticket PDFs.", "/tickets"],
  ["🔍", "PNR Status", "Track booking status instantly.", "/pnr-status"],
];

function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ total_bookings: 0, total_tickets: 0, total_payments: 0 });

  useEffect(() => {
    if (!localStorage.getItem("token")) {
      navigate("/");
      return;
    }
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await api.get("/dashboard/stats", { headers: { Authorization: `Bearer ${token}` } });
        setStats(res.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchStats();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <>
      <section className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">Control center</p>
          <h1>Your journey dashboard.</h1>
          <p>Plan faster with a responsive workspace for searches, passenger profiles, payments, PNR checks, bookings, and tickets.</p>
          <div className="hero-actions"><Link className="btn" to="/search-train">Start booking</Link><button className="btn secondary" onClick={handleLogout}>Logout</button></div>
        </div>
        <div className="visual-card"><h3>Next trip, simplified</h3><p>Everything you need before the chart is prepared.</p><div className="train">🚆</div><div className="train-line" /></div>
      </section>

      <section className="panel">
        <div className="metric-grid">
          <div className="stat-card"><span>📄 Bookings</span><strong>{stats.total_bookings}</strong></div>
          <div className="stat-card"><span>🎟 Tickets</span><strong>{stats.total_tickets}</strong></div>
          <div className="stat-card"><span>💳 Payments</span><strong>{stats.total_payments}</strong></div>
        </div>
      </section>

      <section className="panel">
        <h2>Quick actions</h2>
        <div className="card-grid">
          {actions.map(([icon, title, description, to]) => <Link className="quick-card" key={title} to={to}><h3>{icon} {title}</h3><p>{description}</p></Link>)}
        </div>
      </section>
    </>
  );
}

export default Dashboard;
