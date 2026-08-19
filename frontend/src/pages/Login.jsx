import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append("username", username.trim());
    formData.append("password", password.trim());

    try {
      const response = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.detail || "Login Failed");
    }
  };

  return (
    <section className="hero-card">
      <div className="hero-copy">
        <p className="eyebrow">Fast railway reservations</p>
        <h1>Book Tatkal tickets with confidence.</h1>
        <p>
          Search trains, save passenger profiles, monitor PNR status, and manage
          tickets from one polished dashboard built for phones, tablets, and desktops.
        </p>
        <div className="hero-actions">
          <Link className="btn secondary" to="/register">Create account</Link>
        </div>
      </div>
      <form className="panel form-stack" onSubmit={handleLogin}>
        <h2>Welcome back</h2>
        <input type="text" placeholder="Username or Email" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login securely</button>
      </form>
    </section>
  );
}

export default Login;
