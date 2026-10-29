import { useState } from "react";
import { fetchDashboard } from "./api/league";
import LeagueSearch from "./components/LeagueSearch";
import WeekNavigator from "./components/WeekNavigator";
import WeeklyStandings from "./components/WeeklyStandings";
import "./App.css";

function App() {
  const [leagueId, setLeagueId] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [selectedWeek, setSelectedWeek] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadLeague(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setDashboard(null);

    try {
      const data = await fetchDashboard(leagueId.trim());
      setDashboard(data);
      setSelectedWeek(data.available_weeks[0] ?? null);
      if (!data.latest_week) {
        setError("This league does not have completed weekly scores yet.");
      }
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  const selectedIndex = dashboard?.available_weeks.indexOf(selectedWeek) ?? -1;
  const view = selectedIndex >= 0 ? dashboard.weeks[selectedIndex] : null;

  return (
    <main className="dashboard">
      <header className="scoreboard-header">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">G</span>
          <div>
            <p className="kicker">SLEEPER · GUILLOTINE LEAGUE</p>
            <h1>Monday Night<br />Scorecard</h1>
          </div>
        </div>
        <p className="header-copy">Weekly survival standings, settled one score at a time.</p>
      </header>

      <section className="load-panel" aria-label="Load a Sleeper league">
        <div>
          <p className="panel-label">League control</p>
          <h2>Load the board</h2>
        </div>
        <LeagueSearch
          leagueId={leagueId}
          loading={loading}
          onLeagueIdChange={setLeagueId}
          onSubmit={loadLeague}
        />
      </section>

      {error && <p className="error" role="alert">{error}</p>}

      {dashboard && (
        <>
          <section className="league-card" aria-label="League summary">
            <div className="league-identity">
              <p className="kicker">{dashboard.league.season} SEASON</p>
              <h2>{dashboard.league.name}</h2>
            </div>
            <div className="league-meta">
              <span><b>{dashboard.league.total_rosters}</b> teams</span>
              <span className="status-live"><i aria-hidden="true" />{dashboard.league.status}</span>
            </div>
          </section>

          {view && (
            <>
              <WeekNavigator
                week={selectedWeek}
                canGoPrevious={selectedIndex > 0}
                canGoNext={selectedIndex < dashboard.available_weeks.length - 1}
                onPrevious={() => setSelectedWeek(dashboard.available_weeks[selectedIndex - 1])}
                onNext={() => setSelectedWeek(dashboard.available_weeks[selectedIndex + 1])}
              />
              <WeeklyStandings view={view} />
            </>
          )}
        </>
      )}
    </main>
  );
}

export default App;
