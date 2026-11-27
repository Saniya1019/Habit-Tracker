# Habit Tracker (Django + React)

Daily check-ins, streaks, and progress charts. Django serves both the API and the (pre-built) React app.

## Run it
One-time install: `pip install django djangorestframework`

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000**, sign up, and add a habit. No Node.js needed.

## Tests
`python manage.py test`

## Editing the React code (optional)
The source is in `frontend/`. After changes: `cd frontend && npm install && npm run build`
(this rebuilds into `backend/static/app`). For hot reload use `npm run dev` and open http://localhost:5173.

## API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register/`, `/api/login/` | returns `{token, username}` |
| GET/POST | `/api/habits/` | list / create habits |
| DELETE | `/api/habits/<id>/` | delete a habit |
| POST | `/api/habits/<id>/toggle/` | check in / undo (optional `{"date": "YYYY-MM-DD"}`) |
| GET | `/api/stats/?days=14` | daily completion data for the chart |

Token auth: send `Authorization: Token <token>`.

"Today" uses `TIME_ZONE` in `backend/config/settings.py` (default `Asia/Kolkata`); change it to yours.
