import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

export default function Login() {
  const nav = useNavigate();

  // ✅ FIX: empty fields (no auto-fill)
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async () => {
    try {
      const res = await API.post("/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.token);
      nav("/billing");
    } catch (err) {
      setError("Invalid Login");
    }
  };

  return (
    <div style={{
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "#111827"
    }}>
      <div style={{
        width: "350px",
        background: "#1f2937",
        padding: "30px",
        borderRadius: "15px",
        color: "white"
      }}>
        <h1>🛒 POS LOGIN</h1>

        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          autoComplete="off"
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "15px"
          }}
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          autoComplete="off"
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "10px"
          }}
        />

        <button
          onClick={submit}
          style={{
            width: "100%",
            padding: "12px",
            marginTop: "15px",
            background: "green",
            color: "white",
            border: "none",
            borderRadius: "6px"
          }}
        >
          LOGIN
        </button>

        {error && (
          <p style={{ color: "red", marginTop: "10px" }}>
            {error}
          </p>
        )}
      </div>
    </div>
  );
}
