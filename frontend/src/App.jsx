
import { useState } from "react";
import "./App.css";

const API_URL = "";

function App() {
  const [leagueId, setLeagueId] = useState("");
  const [league, setLeague] = useState(null);
  const [eliminations, setEliminations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadLeague(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setLeague(null);
    setEliminations([]);

    try {
      const id = leagueId.trim();

      const response = await fetch(
        `${API_URL}/api/league/${encodeURIComponent(id)}`
      );

      if (!response.ok) {
        throw new Error("Could not load league. Check the league ID.");
      }

      const leagueData = await response.json();

      const eliminationResponse = await fetch(
        `${API_URL}/api/league/${encodeURIComponent(id)}/eliminations`
      );

      if (!eliminationResponse.ok) {
        throw new Error("League loaded, but eliminations could not be fetched.");
      }

      const eliminationData = await eliminationResponse.json();

      setLeague(leagueData);
      setEliminations(eliminationData.eliminations);
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="dashboard">
      <header className="page-header">
        <h1>Guillotine Dashboard</h1>
        <p>Track every elimination in your Sleeper league.</p>
      </header>

      <form className="league-form" onSubmit={loadLeague}>
        <input
          value={leagueId}
          onChange={(event) => setLeagueId(event.target.value)}
          placeholder="Paste your Sleeper league ID"
          aria-label="Sleeper league ID"
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Load League"}
        </button>
      </form>

      {error && <p className="error" role="alert">{error}</p>}

      {league && (
        <>
          <section className="league-card">
            <h2>{league.name}</h2>
            <p>Season: {league.season}</p>
            <p>Teams: {league.total_rosters}</p>
            <p>Status: {league.status}</p>
          </section>

          <section className="timeline">
            <h2>Elimination History</h2>

            {eliminations.length === 0 ? (
              <p>No eliminations to display yet.</p>
            ) : (
              <ol className="timeline-list">
                {eliminations.map((item) => (
                  <li key={`${item.week}-${item.roster_id}`}>
                    <div className="week-label">WEEK {item.week}</div>
                    <div className="elimination-card">
                      <div>
                        <h3>{item.owner_name}</h3>
                        <p>Roster #{item.roster_id}</p>
                      </div>
                      <div className="score">
                        {Number(item.points).toFixed(2)} pts
                      </div>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </section>
        </>
      )}
    </main>
  );
}

export default App;
