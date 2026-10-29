export default function LeagueSearch({ leagueId, loading, onLeagueIdChange, onSubmit }) {
  return (
    <form className="league-form" onSubmit={onSubmit}>
      <label className="sr-only" htmlFor="league-id">Sleeper league ID</label>
      <input
        id="league-id"
        value={leagueId}
        onChange={(event) => onLeagueIdChange(event.target.value)}
        placeholder="Paste Sleeper league ID"
        required
      />
      <button type="submit" disabled={loading}>
        <span>{loading ? "Loading board" : "Load league"}</span>
        <span aria-hidden="true">→</span>
      </button>
    </form>
  );
}
