import { useState } from "react";
import { api, getToken } from "./api.js";
import Auth from "./Auth.jsx";
import Dashboard from "./Dashboard.jsx";

export default function App() {
  const [authed, setAuthed] = useState(Boolean(getToken()));
  const [user, setUser] = useState(localStorage.getItem("username") || "");

  const onAuth = ({ token, username }) => {
    localStorage.setItem("token", token);
    localStorage.setItem("username", username);
    setUser(username);
    setAuthed(true);
  };
  const logout = () => {
    localStorage.clear();
    setAuthed(false);
  };

  return authed ? <Dashboard user={user} onLogout={logout} /> : <Auth onAuth={onAuth} api={api} />;
}
