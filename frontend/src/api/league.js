export async function fetchDashboard(leagueId) {
  const response = await fetch(`/api/league/${encodeURIComponent(leagueId)}/dashboard`);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Could not load league. Check the league ID.");
  return data;
}
