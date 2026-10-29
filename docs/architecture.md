# Architecture

## Overview

The repository is a two-service application managed by Docker Compose:

```text
                         Docker Compose network
┌─────────────┐      ┌───────────────────┐      ┌───────────────────┐
│ Browser tab │─────►│ frontend (Nginx)  │─────►│ backend (FastAPI) │
└─────────────┘      │ port 80           │      │ port 8000         │
       │             └───────────────────┘      └─────────┬─────────┘
       │                                                   │ HTTPS
       │                                                   ▼
       │                                          Sleeper public API
       │                                           api.sleeper.app
       ▼
Host ports: 80 (frontend), 8000 (backend)
```

The frontend is a React application built by Vite. The production frontend
image builds the static site and serves it with Nginx. The backend is a FastAPI
application started by Uvicorn.

## Components and responsibilities

### React frontend

The frontend source lives in `frontend/src/`.

- `App.jsx` owns the entered league ID, loaded dashboard response, selected
  week, loading flag, and error message.
- `api/league.js` requests
  `/api/league/{leagueId}/dashboard`.
- `components/LeagueSearch.jsx`, `WeekNavigator.jsx`, and
  `WeeklyStandings.jsx` render the form, week controls, and standings.

After one dashboard response arrives, changing weeks only changes React state;
it does not make another API request.

### Nginx

`frontend/nginx.conf` has two relevant routes:

| Browser path | Nginx behavior |
| --- | --- |
| `/` and static-file paths | Serves the built React files from `/usr/share/nginx/html`; `try_files` falls back to `index.html` for client-side routes. |
| `/api/` | Proxies to `http://backend:8000`, where `backend` is the Docker Compose service name. |

This means a production browser requests `/api/...` from the same origin as the
frontend. It does not need to know the backend container hostname.

### FastAPI backend

`backend/main.py` defines:

- `GET /` — returns an API-running message.
- `GET /api/league/{league_id}/dashboard` — returns the dashboard data used by
  the frontend.

The FastAPI lifespan creates one reusable `SleeperClient` when the application
starts and closes it when the application stops. The client is a connection
helper; it is not a per-league data store.

### League service and rules

`backend/league_service.py` gathers a league, its users, rosters, NFL state,
and matchup lists from Sleeper. It obtains matchup lists concurrently for the
weeks it needs. It then maps owner names to rosters and passes weekly scores to
`calculate_weekly_views` in `backend/guillotine.py`.

The calculation code:

1. Starts with all roster IDs active.
2. Adds each roster's weekly score to its cumulative points.
3. Sorts active teams by weekly points ascending, then cumulative points
   ascending, then roster ID only as a deterministic fallback.
4. Marks the lowest ranked team as eliminated and removes it from later weeks.
5. Marks a one-team final view as `winner` and stops processing later weeks.

The included tests cover basic eliminations, the cumulative-points tiebreaker,
and the winner state.

### Sleeper API client

`backend/sleeper_client.py` uses HTTPX with base URL
`https://api.sleeper.app/v1`. The code requests league, user, roster, matchup,
and NFL-state resources. HTTP failures are translated by the FastAPI route into
404 for a missing league or 502 for upstream/connectivity problems.

## Request flows

### Production Compose flow

```text
1. Browser GET /api/league/123/dashboard
2. Nginx sees /api/ and proxies the request to backend:8000
3. FastAPI calls the Sleeper API and calculates weekly views
4. FastAPI returns JSON to Nginx
5. Nginx returns JSON to the browser
6. React stores the response and renders week 1
```

### Local Vite development flow

`frontend/vite.config.js` configures the Vite development server to proxy
`/api` to `http://localhost:8000`. The browser request is still `/api/...`,
but Vite forwards it to a backend running on the developer's machine.

## Separate browser tabs and league state

Each browser tab creates its own React application instance. The app stores the
league ID, dashboard data, and selected week with React `useState` inside that
tab. The frontend code does not use shared browser storage, URL parameters,
cookies, or a client-side global cache for league data.

As a result, loading league A in one tab and league B in another tab keeps the
two displayed dashboards separate. Each tab sends its own API request whose
path contains its league ID and stores its own response.

On the server, the reusable HTTPX client is shared for connections, but the
route passes the requested `league_id` directly into the service for every
request. The repository has no configured server-side cache or mutable
per-league session state. Therefore, the application code does not mix data
between tabs.

This describes the code in this repository. It does not guarantee behavior of
any browser extension, reverse proxy, or external cache added outside this
repository.

## Docker Compose networking and ports

`compose.yaml` defines `frontend` and `backend` on Compose's default network.

| Service | Container port | Published host port | Purpose |
| --- | --- | --- | --- |
| `frontend` | 80 | 80 | Nginx serves the React app and proxies `/api/`. |
| `backend` | 8000 | 8000 | Uvicorn serves FastAPI and Swagger UI at `/docs`. |

`depends_on` makes Compose start `backend` before `frontend`, but the current
file does not define a health check. It is start ordering, not a readiness
guarantee.
