# Deployment notes

## Scope and verified configuration

The project owner reports deployment on an AWS EC2 instance. This repository
contains Dockerfiles and `compose.yaml`, but it does **not** contain EC2
provisioning, an AWS security-group configuration, a domain name, TLS
configuration, a system service, or a deployment script. Those details must be
verified directly on the instance or in AWS before changing a live deployment.

The deployment information below is limited to the configuration committed in
this repository.

## Services and ports

`compose.yaml` builds and starts two services:

| Service | Host mapping | Container role |
| --- | --- | --- |
| `frontend` | `80:80` | Nginx serving the compiled React files and proxying `/api/`. |
| `backend` | `8000:8000` | Uvicorn serving FastAPI and Swagger UI. |

The frontend is available at `http://<server>/`. The backend Swagger UI is
available at `http://<server>:8000/docs` when the server's network rules permit
access to port 8000.

Both services use `restart: unless-stopped`, so Docker restarts them unless
they were explicitly stopped. No Docker volumes are configured; the application
does not persist its own data through Compose.

## Reverse-proxy behavior

The frontend image uses Nginx.

```text
Client GET /          → Nginx serves static React files
Client GET /api/...   → Nginx proxies to http://backend:8000
```

Nginx passes the standard `Host`, real-IP, forwarded-for, and forwarded-proto
headers to the backend. This is an internal Docker-network proxy, not a
documented public TLS/reverse-proxy configuration.

The backend is also separately published on host port 8000. That is useful for
local Swagger access, but on an EC2 instance it means you should decide whether
port 8000 should be publicly reachable. The repository does not choose that
policy for you.

## Build and start on a host

On a host with Docker and the Compose plugin installed, from a checked-out copy
of this repository:

```bash
docker compose up --build -d
```

- `--build` rebuilds the backend and frontend images from the checked-out code.
- `-d` starts the containers in the background.

Confirm that Compose sees both containers:

```bash
docker compose ps
```

Inspect the published configuration without starting anything:

```bash
docker compose config
```

## Logs and diagnosis

Follow logs from both services:

```bash
docker compose logs -f
```

Follow a single service when diagnosing a frontend proxy or backend API issue:

```bash
docker compose logs -f frontend
docker compose logs -f backend
```

The frontend logs come from Nginx. Backend logs come from the Uvicorn process.
If a dashboard request fails, inspect the backend logs because it calls the
external Sleeper API.

## Safe update process

The following is a cautious process based on the files in this repository. It
does not assume a particular Git branch or EC2 setup:

1. Review the intended revision and run the relevant local tests before it
   reaches the server.
2. On the server, ensure the desired reviewed code is present in the project
   directory. How it arrives is outside this repository's configuration.
3. Inspect the Compose configuration:

   ```bash
   docker compose config
   ```

4. Rebuild and replace the services:

   ```bash
   docker compose up --build -d
   ```

5. Check status and logs:

   ```bash
   docker compose ps
   docker compose logs -f
   ```

6. Verify the frontend and, if intentionally exposed, Swagger UI from an
   allowed network.

Do not run deployment commands without approval. `AGENTS.md` requires explicit
approval before production changes.

## Manual verification checklist for EC2

These items are not represented in the repository and need manual confirmation:

- Docker and Docker Compose are installed on the EC2 instance.
- The instance firewall and AWS security group allow only the ports you intend
  to expose. At minimum, the configured frontend uses port 80.
- Whether port 8000 should be public, restricted, or reachable only through an
  external reverse proxy.
- Whether a domain name, HTTPS certificate, and an external reverse proxy
  exist. The committed Nginx configuration listens only on HTTP port 80.
- How the service should start after a host reboot beyond Docker's container
  restart policy.
- How a failed update should be rolled back to a previously reviewed revision.
