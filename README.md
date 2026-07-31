# Delta Sysads Onsites 3
You're given a frontend (with Vite React) and backend (with Python Flask).

## Running locally
```
cd backend
pip install -r requirements.txt
python app.py
```
```
cd frontend
npm i
npm run dev
```


## The app
- **Taskwise** — a tiny task tracker.
- Anyone can create an account and log in.
- Logged-in users can add, complete and delete **their own** todos.
- Todos are stored in a SQLite database and are expected to be **private per user**.

## Goal
Your job is to get it running properly behind nginx, served under the `/app/` base path, with accounts, sessions and
the todo list working end to end.

When the app is deployed (using nginx) it must be reachable at /app.
Both the dev setup and the deployed setup should work.

The `docker-compose.yml` and `nginx.conf` in the repo root are empty stubs. You need to fill
them in so the built frontend is served under `/app/`, and API requests reach the backend.

## Ideas Symptoms you should see (all on purpose)
1. The page is unstyled or entirely blank under `/app/` — assets are 404ing
2. The todo list can't load — the fetch to the backend is failing (CORS)
3. You log in successfully but are immediately treated as logged out (cookies)
4. Some icons in the footer are missing (assets)
5. In local dev everything appears to work 

## Hints (read only if truly stuck)
- The task is about *configuration, deployment and session handling*, not feature work.
- The React components and the Flask endpoints themselves are correct.
- The browser's **Network tab** tells you the real story. Follow the failing requests
- Vite docs for config file might help
- What is CORs and cookies?

Good luck.
May the force be with you.