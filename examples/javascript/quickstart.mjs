// PrizePicks API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs NBA

const HOST = 'prizepicks-api.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`PrizePicks API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const league = process.argv[2] ?? 'NBA';

// The board, most picked first. odds_type says standard, goblin (easier) or demon (harder).
const { projections, pagination } = await get('/projections', {
  league,
  sort: 'trending_count',
  sort_direction: 'desc',
  per_page: 25,
});
console.log(`${pagination.total} ${league} lines on the board`);
for (const p of projections.slice(0, 10)) {
  console.log(`${String(p.trending_count ?? 0).padStart(6)}  ${p.player.name} ${p.stat_type} ${p.line_score} [${p.odds_type}] vs ${p.description}`);
}
