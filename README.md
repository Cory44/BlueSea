# BlueSea

Marine themed BlueSky clone running on the AT Protocol.

## 1. Overview

BlueSea is a full-stack project with a Flask backend and a Vue 3 + Vite frontend. Development tooling is centered around Docker Compose so that the backend and frontend can both be run with hot reload and share a common configuration surface.

## 2. Local development with Docker

### Prerequisites
- Docker with Compose v2 support (`docker compose`)
- GNU Make (optional, used for the convenience commands below)

### Starting the stack

The repository provides a root `Makefile` that wraps the most common `docker compose` workflows:

| Command | Description |
| --- | --- |
| `make up` | Builds (if necessary) and starts the frontend and backend together with attached logs. |
| `make fe` | Starts only the frontend service (the backend is started automatically because of the dependency). |
| `make be` | Starts only the backend service. |
| `make db-reset` | Removes the local SQLite database file and reseeds the admin user inside a one-off backend container. |

All targets rely on the `docker-compose.yml` file at the repository root. The Compose file enables hot reload by bind mounting the local `backend/` and `frontend/` directories into their respective containers. Static uploads are persisted to `backend/uploads` on the host, keeping files available between container restarts.

The backend service listens on [http://localhost:5000](http://localhost:5000) and automatically reloads when files under `backend/` change. The frontend service is exposed on [http://localhost:5173](http://localhost:5173) with Vite’s development server configured for polling-based hot module replacement so that edits under `frontend/` are reflected immediately.

### Environment variables

The Compose configuration supplies a development-friendly set of defaults:

- `FLASK_APP=bluesea_app:create_app` ensures the Flask auto-reloader uses the application factory.
- `FLASK_ENV=development` enables debug mode for better error messages.
- `CORS_ORIGINS=http://localhost:5173` allows the frontend dev server to call the backend API.
- `UPLOAD_FOLDER=/app/uploads` persists uploads to the bind-mounted `backend/uploads` directory.
- `VITE_API_BASE_URL=http://localhost:5000` is available for frontend code that needs to call the backend.
- `CHOKIDAR_USEPOLLING=true` forces Vite to use polling, improving file watch reliability when running inside Docker.

You can override any of these values by creating a `.env` file next to `docker-compose.yml`.

## 3. Running services without Docker

Docker is the recommended workflow, but you can still run each service directly on your host machine.

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=bluesea_app:create_app
flask run --debug --host 0.0.0.0 --port 5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## 4. Project structure

```
BlueSea/
├── Makefile
├── README.md
├── docker-compose.yml
├── backend/
│   ├── bluesea_app/
│   ├── requirements.txt
│   └── wsgi.py
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── public/
    └── src/
```

This layout keeps the backend, frontend, and containerization assets organized while enabling straightforward development with Docker or local tooling.
