# BlueSea

Marine themed BlueSky clone running on the AT Protocol.

## 1. Overview

BlueSea is envisioned as a full-stack project with a Python-powered backend, a modern TypeScript/React frontend, and containerized tooling for local development. This repository currently provides the foundational structure needed to start building out those services.

## 2. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Apply migrations or initialize the database once they are available
alembic upgrade head
# Start the local development server
uvicorn app.main:app --reload
```

These commands assume a FastAPI-style application and SQLAlchemy migrations via Alembic. Update them as the backend implementation takes shape.

## 3. Frontend setup

```bash
cd frontend
npm install
# or: pnpm install / yarn install
npm run dev
```

During development the frontend assets are served from `frontend/public`. Place any provided brand logos or images under `frontend/public/assets/`. Refer to them in your components using relative paths such as `/assets/logo.svg`.

## 4. Project structure

```
BlueSea/
├── backend/
│   └── .gitkeep
├── docker/
│   └── .gitkeep
├── frontend/
│   ├── .gitkeep
│   ├── public/
│   │   ├── .gitkeep
│   │   └── assets/
│   │       └── .gitkeep
│   └── src/
│       ├── .gitkeep
│       ├── components/
│       │   └── .gitkeep
│       ├── hooks/
│       │   └── .gitkeep
│       ├── pages/
│       │   └── .gitkeep
│       ├── styles/
│       │   └── .gitkeep
│       └── utils/
│           └── .gitkeep
├── .gitignore
└── README.md
```

This layout gives backend, frontend, and containerization workspaces while keeping empty directories under version control through `.gitkeep` placeholders.
