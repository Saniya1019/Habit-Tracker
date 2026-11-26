import { useState } from "react";

export default function Auth({ onAuth, api }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      onAuth(await api(mode === "login" ? "login/" : "register/", { method: "POST", body: form }));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="auth">
      <h1>Habit Tracker</h1>
      <p className="muted">Small things, done daily, add up.</p>
      <form onSubmit={submit} className="card">
        <h2>{mode === "login" ? "Log in" : "Create account"}</h2>
        <input placeholder="Username" value={form.username} autoFocus
          onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <input type="password" placeholder="Password (6+ characters)" value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })} />
        {error && <p className="error">{error}</p>}
        <button className="primary">{mode === "login" ? "Log in" : "Sign up"}</button>
        <button type="button" className="link" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>
          {mode === "login" ? "New here? Create an account" : "Have an account? Log in"}
        </button>
      </form>
    </main>
  );
}
