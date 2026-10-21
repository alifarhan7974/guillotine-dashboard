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
    setLoading(true); setError(""); setDashboard(null);
    try {
      const data = await fetchDashboard(leagueId.trim());
      setDashboard(data); setSelectedWeek(data.available_weeks[0] ?? null);
      if (!data.latest_week) setError("This league does not have completed weekly scores yet.");
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally { setLoading(false); }
  }

  const selectedIndex = dashboard?.available_weeks.indexOf(selectedWeek) ?? -1;
  const view = selectedIndex >= 0 ? dashboard.weeks[selectedIndex] : null;

  return <main className="dashboard">
    <header className="page-header"><p className="eyebrow">SLEEPER LEAGUE TRACKER</p><h1>Guillotine Dashboard</h1><p>See exactly who was on the chopping block each week.</p></header>
    <LeagueSearch leagueId={leagueId} loading={loading} onLeagueIdChange={setLeagueId} onSubmit={loadLeague} />
    {error && <p className="error" role="alert">{error}</p>}
    {dashboard && <>
      <section className="league-card"><div><p className="eyebrow">{dashboard.league.season} SEASON</p><h2>{dashboard.league.name}</h2></div><div className="league-meta"><span>{dashboard.league.total_rosters} teams</span><span>{dashboard.league.status}</span></div></section>
      {view && <><WeekNavigator week={selectedWeek} canGoPrevious={selectedIndex > 0} canGoNext={selectedIndex < dashboard.available_weeks.length - 1} onPrevious={() => setSelectedWeek(dashboard.available_weeks[selectedIndex - 1])} onNext={() => setSelectedWeek(dashboard.available_weeks[selectedIndex + 1])} /><WeeklyStandings view={view} /></>}
    </>}
  </main>;
}

export default App;
