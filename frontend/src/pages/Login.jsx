import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    const email = username.trim();
    const pwd = password.trim();

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", pwd);

    console.log("EMAIL:", "[" + email + "]");
    console.log("PASSWORD:", "[" + pwd + "]");

    try {
      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

      console.log(
        "LOGIN RESPONSE:",
        response.data
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      console.log(
        "TOKEN STORED:",
        localStorage.getItem("token")
      );

      alert("Login Successful");

      navigate("/dashboard");

    } catch (error) {
      console.error(
        "LOGIN ERROR:",
        error
      );

      console.error(
        "ERROR RESPONSE:",
        error.response?.data
      );

      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username or Email"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
          required
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          required
        />

        <br />
        <br />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;