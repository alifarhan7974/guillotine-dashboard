function score(value) { return Number(value).toFixed(2); }

export default function WeeklyStandings({ view }) {
  const isWinner = view.eliminated.status === "winner";
  return <section className="standings" aria-labelledby="standings-title">
    <div className={`elimination-summary ${isWinner ? "winner-summary" : ""}`}><span>{isWinner ? "Winner" : "Eliminated"}</span><strong>{view.eliminated.owner_name}</strong><span>{score(view.eliminated.points)} pts · {score(view.eliminated.cumulative_points)} season pts</span></div>
    <h2 id="standings-title">Weekly standings</h2>
    <p className="table-note">Lowest weekly score is eliminated; ties use cumulative season points.</p>
    <div className="standings-table" role="table" aria-label={`Week ${view.week} standings`}>
      <div className="standing-row heading" role="row"><span>Rank</span><span>Team</span><span>Week</span><span>PF</span><span>Status</span></div>
      {view.standings.map((team) => <div className={`standing-row ${team.status}`} role="row" key={team.roster_id}>
        <span>#{team.rank}</span><span><strong>{team.owner_name}</strong></span><span>{score(team.points)}</span><span>{score(team.cumulative_points)}</span><span>{team.status === "winner" ? "Winner" : team.status === "eliminated" ? "Eliminated" : "Safe"}</span>
      </div>)}
    </div>
  </section>;
}
