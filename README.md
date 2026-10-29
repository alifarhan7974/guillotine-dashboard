# Guillotine Dashboard

Guillotine Dashboard is a web application for viewing a Sleeper fantasy-football
guillotine league one week at a time. Enter a Sleeper league ID, review the
surviving teams in ascending weekly-score order, and see the eliminated team or
the final winner.

## Features

- Loads league metadata, owners, rosters, and matchup scores from Sleeper.
- Shows weekly standings in ascending score order for teams that are still alive.
- Eliminates the lowest weekly score; tied weekly scores use lower cumulative
  points through that week as the tiebreaker.
- Marks the final remaining team as the winner.
- Lets the user move between available weeks without another browser request.
- Serves the production frontend through Nginx and exposes FastAPI Swagger UI.

## Technology stack

| Area | Technology used in this repository |
| --- | --- |
| Frontend | React 19, Vite 8, Oxlint |
| Backend | FastAPI, HTTPX, Uvicorn, Python 3.11+ |
| Python dependencies | `uv` with `pyproject.toml` and `uv.lock` |
| Production web server | Nginx |
| Containers | Docker and Docker Compose |
| Data provider | Sleeper API |
| CI | GitHub Actions |

## Architecture at a glance

```text
Browser
  │  http://localhost/
  ▼
Nginx frontend container ── /api/* ──► FastAPI backend container
  │                                      │
  └── React static files                  └── Sleeper API
```

Docker Compose publishes the frontend on host port 80 and the backend on host
port 8000. Nginx keeps browser API calls on the same origin by proxying `/api/`
to the backend service over Docker's internal network.

Read [the architecture guide](docs/architecture.md) for request flows and
state behavior.

## Prerequisites

Choose the workflow that fits your task:

- **Container workflow:** Docker Desktop (or Docker Engine) with the Docker
  Compose plugin.
- **Backend-only local workflow:** Python 3.11 or later and `uv`.
- **Frontend-only local workflow:** Node.js and npm. The production Dockerfile
  uses Node 22; use that version when you want local parity with the container
  build.

The repository does not define environment variables or require a `.env` file.

## Local setup with Docker Compose

From the repository root:

```bash
docker compose up --build
```

`--build` creates fresh images from `backend/Dockerfile` and
`frontend/Dockerfile` before starting the services.

Open these addresses after the services start:

- Frontend: <http://localhost/>
- FastAPI Swagger UI: <http://localhost:8000/docs>
- Backend root response: <http://localhost:8000/>

Stop the services with `Ctrl+C`, or run this in a second terminal:

```bash
docker compose down
```

## Usage

1. Open the frontend in a browser.
2. Paste a Sleeper league ID into **Load league**.
3. Start on the first available completed week.
4. Use **Previous** and **Next** to inspect each weekly scoreboard.

The UI labels the eliminated team for a normal week. When only one active team
is left in the calculated view, it labels that team as the winner.

## Tests and checks

Run the backend tests from `backend/`:

```bash
uv run pytest -q
```

Run the frontend production build from `frontend/`:

```bash
npm run build
```

Run the configured frontend linter from `frontend/`:

```bash
npm run lint
```

For clean dependency installation before those commands, use `uv sync
--locked --all-groups` in `backend/` and `npm ci` in `frontend/`.

The GitHub Actions workflow runs the backend tests and frontend build on pushes
and pull requests. See `.github/workflows/ci.yml`.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `localhost` does not load | Run `docker compose ps`; the frontend container should be running and host port 80 must be free. |
| Swagger UI does not load | Confirm the backend is running with `docker compose ps` and host port 8000 is free. |
| The frontend loads but data fails | Check backend logs with `docker compose logs -f backend`. The backend depends on reaching the Sleeper API. |
| A league is reported missing | Verify that the pasted Sleeper league ID is correct. |
| No completed weeks appear | The app reports this when the response has no available completed weeks. Confirm the league has matchup scores in Sleeper. |
| Local frontend API calls fail in Vite | Start the backend locally on port 8000; Vite proxies `/api` to `http://localhost:8000`. |

## More documentation

- [Architecture](docs/architecture.md)
- [Development workflow](docs/development.md)
- [Deployment notes](docs/deployment.md)
- [Project guidance for contributors](AGENTS.md)
