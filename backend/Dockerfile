
FROM python:3.11-slim

# Install uv, which manages our Python dependencies.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency definitions first for better build caching.
COPY pyproject.toml uv.lock ./

# Install production dependencies, excluding development tools like pytest.
RUN uv sync --frozen --no-dev

# Copy the backend application.
COPY main.py sleeper_client.py league_service.py guillotine.py ./

EXPOSE 8000

CMD ["uv", "run", "--frozen", "--no-dev", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
