import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "./api.js";

const COLORS = ["#2f7d5b", "#d9822b", "#3b6fb6", "#b84a62", "#7a5ab5", "#2b8a97"];

export default function Dashboard({ user, onLogout }) {
  const [habits, setHabits] = useState([]);
  const [stats, setStats] = useState([]);
  const [name, setName] = useState("");
  const [color, setColor] = useState(COLORS[0]);
  const [days, setDays] = useState(14);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const [h, s] = await Promise.all([api("habits/"), api(`stats/?days=${days}`)]);
      setHabits(h);
      setStats(s);
    } catch (err) {
      if (err.status === 401) onLogout();
      else setError(err.message);
    }
  };
  useEffect(() => { load(); }, [days]);

  const add = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    await api("habits/", { method: "POST", body: { name: name.trim(), color } });
    setName("");
    load();
  };
  const toggle = async (id, date) => {
    await api(`habits/${id}/toggle/`, { method: "POST", body: date ? { date } : {} });
    load();
  };
  const remove = async (h) => {
    if (!confirm(`Delete "${h.name}" and its history?`)) return;
    await api(`habits/${h.id}/`, { method: "DELETE" });
    load();
  };

  const doneToday = habits.filter((h) => h.checked_today).length;
  const best = Math.max(0, ...habits.map((h) => h.current_streak));

  return (
    <main className="dash">
      <header>
        <h1>Habit Tracker</h1>
        <span className="muted">{user}</span>
        <button className="link" onClick={onLogout}>Log out</button>
      </header>
      {error && <p className="error">{error}</p>}

      <section className="today">
        <p className="big">{doneToday}<span>/{habits.length}</span></p>
        <p>habits done today{best > 0 && <> &middot; best running streak: <b>{best} {best === 1 ? "day" : "days"}</b></>}</p>
      </section>

      <form className="add" onSubmit={add}>
        <input placeholder="New habit, e.g. Read 20 pages" value={name} onChange={(e) => setName(e.target.value)} />
        <div className="swatches">
          {COLORS.map((c) => (
            <button type="button" key={c} aria-label={`Colour ${c}`} className={c === color ? "sw on" : "sw"}
              style={{ background: c }} onClick={() => setColor(c)} />
          ))}
        </div>
        <button className="primary">Add habit</button>
      </form>

      <section className="list">
        {habits.length === 0 && <p className="muted empty">No habits yet. Add your first one above.</p>}
        {habits.map((h) => (
          <article className="habit card" key={h.id} style={{ "--c": h.color }}>
            <button className={h.checked_today ? "check done" : "check"} onClick={() => toggle(h.id)}
              aria-label={h.checked_today ? "Undo today's check-in" : "Check in for today"}>
              {h.checked_today ? "✓" : ""}
            </button>
            <div className="info">
              <h3>{h.name}</h3>
              <p className="muted">
                {h.current_streak}-day streak &middot; best {h.longest_streak} &middot; {h.total_checkins} total
              </p>
            </div>
            <div className="week" title="Last 7 days (click a day to toggle)">
              {h.last_7_days.map((d) => (
                <button key={d.date} className={d.done ? "dot on" : "dot"} title={d.date} onClick={() => toggle(h.id, d.date)} />
              ))}
            </div>
            <button className="link del" onClick={() => remove(h)} aria-label={`Delete ${h.name}`}>Delete</button>
          </article>
        ))}
      </section>

      <section className="card chart">
        <div className="chart-head">
          <h2>Completion rate</h2>
          <select value={days} onChange={(e) => setDays(Number(e.target.value))}>
            <option value={7}>Last 7 days</option>
            <option value={14}>Last 14 days</option>
            <option value={30}>Last 30 days</option>
          </select>
        </div>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={stats}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="label" tick={{ fontSize: 12 }} interval="preserveStartEnd" />
            <YAxis domain={[0, 100]} unit="%" tick={{ fontSize: 12 }} width={44} />
            <Tooltip formatter={(v, _n, p) => [`${v}% (${p.payload.completed} done)`, "Completed"]} />
            <Bar dataKey="percent" fill="#2f7d5b" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </section>
    </main>
  );
}
