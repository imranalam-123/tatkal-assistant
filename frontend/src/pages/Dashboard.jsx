import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const navigate = useNavigate();

  const [stats, setStats] = useState({
    total_bookings: 0,
    total_tickets: 0,
    total_payments: 0,
  });

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetchStats();
  }, [navigate]);

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:8000/dashboard/stats",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setStats(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div
      style={{
        textAlign: "center",
        color: "white",
        marginTop: "40px",
      }}
    >
      <h1>Tatkal Assistant Dashboard</h1>

      {/* Statistics Cards */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "20px",
          marginTop: "30px",
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            border: "1px solid white",
            padding: "20px",
            width: "180px",
          }}
        >
          <h3>📄 Bookings</h3>
          <h2>{stats.total_bookings}</h2>
        </div>

        <div
          style={{
            border: "1px solid white",
            padding: "20px",
            width: "180px",
          }}
        >
          <h3>🎟 Tickets</h3>
          <h2>{stats.total_tickets}</h2>
        </div>

        <div
          style={{
            border: "1px solid white",
            padding: "20px",
            width: "180px",
          }}
        >
          <h3>💳 Payments</h3>
          <h2>{stats.total_payments}</h2>
        </div>
      </div>

      {/* Navigation */}
      <div style={{ marginTop: "40px" }}>
        <Link
          to="/search-train"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>🚆 Search Train</h3>
        </Link>

        <Link
          to="/passenger-details"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>👤 Passenger Details</h3>
        </Link>

        <Link
          to="/my-bookings"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>📄 My Bookings</h3>
        </Link>

        <Link
          to="/payment"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>💳 Payment</h3>
        </Link>

        <Link
          to="/tickets"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>🎟 My Tickets</h3>
        </Link>

        <Link
          to="/pnr-status"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          <h3>🔍 PNR Status</h3>
        </Link>

        <button
          onClick={handleLogout}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          🚪 Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;