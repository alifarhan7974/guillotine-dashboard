export default function LeagueSearch({ leagueId, loading, onLeagueIdChange, onSubmit }) {
  return <form className="league-form" onSubmit={onSubmit}>
    <input value={leagueId} onChange={(event) => onLeagueIdChange(event.target.value)} placeholder="Paste your Sleeper league ID" aria-label="Sleeper league ID" required />
    <button type="submit" disabled={loading}>{loading ? "Loading..." : "Load League"}</button>
  </form>;
}
