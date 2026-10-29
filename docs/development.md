# Development workflow

## Before you edit

Read [AGENTS.md](../AGENTS.md). It requires contributors to inspect existing
code, preserve functionality and API contracts unless asked to change them, run
relevant checks, avoid exposing secrets, and avoid production changes without
approval.

This repository has no configured environment variables. Do not add secrets to
the repository, even if a future feature needs configuration.

## Repository layout

```text
backend/                 FastAPI application, tests, Python dependency files
frontend/                React/Vite application, Nginx production configuration
compose.yaml             Starts the two containers together
.github/workflows/ci.yml Backend-test and frontend-build CI workflow
docs/                    Project documentation
```

## Start the full stack with Docker Compose

From the repository root:

```bash
docker compose up --build
```

Use this when you want the production-style Nginx frontend and FastAPI backend
to run together. Visit <http://localhost/> for the UI and
<http://localhost:8000/docs> for Swagger UI.

Stop the foreground process with `Ctrl+C`. If it was started in the background,
stop it with:

```bash
docker compose down
```

## Run the backend locally

Open one terminal:

```bash
cd backend
uv sync --locked --all-groups
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

The first command installs the dependency versions recorded in `uv.lock`,
including the development group containing pytest. The second command starts
the same FastAPI application and port used by the backend Dockerfile.

Then use <http://localhost:8000/docs> to inspect the API.

## Run the frontend locally

With the backend running on port 8000, open a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

`npm ci` installs exactly the versions in `package-lock.json`. `npm run dev`
starts Vite. Its configuration proxies `/api` requests to
`http://localhost:8000`, so the local frontend can call the local FastAPI
backend.

The Vite command prints the local browser URL when it starts. That URL depends
on Vite's runtime output; this repository does not hard-code it in a script.

## Checks to run before review

### Backend tests

```bash
cd backend
uv run pytest -q
```

The current test file is `backend/test_guillotine.py`. It exercises the
elimination calculation, the cumulative-points tiebreaker, and the winner
state. It does not test live Sleeper API requests or container startup.

### Frontend checks

```bash
cd frontend
npm run lint
npm run build
```

The linter command runs Oxlint. The build command runs Vite and produces a
`frontend/dist/` directory, which is ignored by Git.

For a frontend change, also test the affected interaction in a browser. The
project's guidance specifically calls for responsive layout and interaction
verification when possible.

### Compose configuration check

```bash
docker compose config
```

This prints Docker Compose's resolved configuration and catches basic Compose
syntax/configuration problems. It does not build or start containers.

## Git branches and pull requests

The repository does not define a branch naming convention, a default branch,
or pull-request protection rules. The following is a recommended personal
workflow, not a repository-enforced rule:

```bash
git switch -c docs/improve-documentation
# make and test one focused change
git status
git diff
git add <files-you-reviewed>
git commit -m "Document local development workflow"
git push -u origin docs/improve-documentation
```

Open a pull request from that branch in GitHub. In the PR description, state
what changed, what you tested, and anything you could not verify. The existing
GitHub Actions workflow runs backend tests and the frontend production build on
pushes and pull requests.

Before merging, review the diff and CI result. Do not assume that a green CI
run tests Docker Compose, live Sleeper connectivity, or the visual layout; it
currently does not.
