function score(value) {
  return Number(value).toFixed(2);
}

export default function WeeklyStandings({ view }) {
  const isWinner = view.eliminated.status === "winner";
  const headline = isWinner ? "Champion crowned" : "On the chopping block";

  return (
    <section className="standings" aria-labelledby="standings-title">
      <div className={`elimination-summary ${isWinner ? "winner-summary" : ""}`}>
        <div className="summary-signal" aria-hidden="true">{isWinner ? "★" : "↓"}</div>
        <div>
          <span>{headline}</span>
          <strong>{view.eliminated.owner_name}</strong>
        </div>
        <p><b>{score(view.eliminated.points)}</b> weekly pts <em>·</em> {score(view.eliminated.cumulative_points)} PF</p>
      </div>

      <div className="standings-heading">
        <div>
          <p className="panel-label">Week {view.week} results</p>
          <h2 id="standings-title">Survival standings</h2>
        </div>
        <p className="table-note">Lowest score goes home. Ties break on PF.</p>
      </div>

      <div className="standings-table" role="table" aria-label={`Week ${view.week} standings`}>
        <div className="standing-row heading" role="row">
          <span>Rank</span><span>Owner</span><span>Week</span><span>PF</span><span>Result</span>
        </div>
        {view.standings.map((team) => (
          <div className={`standing-row ${team.status}`} role="row" key={team.roster_id}>
            <span className="rank">{String(team.rank).padStart(2, "0")}</span>
            <span className="owner"><strong>{team.owner_name}</strong></span>
            <span className="points">{score(team.points)}</span>
            <span className="pf">{score(team.cumulative_points)}</span>
            <span className="result">{team.status === "winner" ? "Winner" : team.status === "eliminated" ? "Eliminated" : "Safe"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
