# ⚽ PitchIQ: Soccer Learning App

> 🚧 **Work in progress.** This project is in active development. Features, the data model and the API may change, and some parts described below are only partly built.

PitchIQ is a Duolingo-style web app that teaches soccer one short lesson at a time: rules, tactics, terminology and the basics of the game. It's aimed at people who are new to soccer, especially fans in the United States who want to understand what's happening on the pitch.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS |
| Authentication | Clerk |
| Backend | FastAPI, Pydantic, Uvicorn |
| Database | PostgreSQL, SQLAlchemy 2.0, Alembic (migrations) |
| Auth verification | PyJWT with Clerk JWKS |
| Testing | pytest |

## Current Status

### ✅ Working now
- **Lessons API:** full CRUD for lessons (`GET`, `POST`, `PATCH`, `DELETE`) with Pydantic validation
- **Lesson browsing UI:** a home page that lists lessons as cards, plus a page for each lesson
- **Resilient data fetching:** loading, error, empty and retry states, with request cancellation on the frontend
- **Authentication:** sign up, sign in and sign out with Clerk
- **Protected endpoint:** `/me` checks the Clerk JWT (RS256 via JWKS) and returns the signed-in user's ID
- **Database schema:** `lessons`, `users` and `user_lesson_progress` tables, managed with Alembic migrations

### 🛠️ In progress
- Linking Clerk accounts to internal `users` records
- Lesson completion and progress tracking (endpoints and UI)
- Interactive questions and quizzes inside lessons
- XP totals and a user progress view

### 🗺️ Planned (after the MVP)
- Courses that group lessons into learning paths
- Achievements and streaks
- Knowledge arenas and challenges
- An AI study assistant
- Deployment

## Project Structure

```
SoccerLearningApp/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── main.py           # FastAPI app and routes
│   │   ├── models.py         # SQLAlchemy models (Lesson, User, UserLessonProgress)
│   │   ├── database.py       # Engine, session and DB dependency
│   │   ├── auth.py           # Clerk JWT verification
│   │   └── schemas/          # Pydantic request/response schemas
│   ├── alembic.ini
│   └── requirements.txt
└── frontend/
    ├── app/
    │   ├── page.tsx          # Lesson list (home)
    │   └── lessons/[lessonId]/page.tsx   # Lesson detail page
    ├── components/           # Navbar, LessonCard, CurrentUser, ...
    ├── types/                # Shared TypeScript types and API URL
    └── proxy.ts              # Clerk middleware
```

## Data Model

- **Lesson:** `id`, `title` (unique), `description`, `content`, `xp_reward`
- **User:** `id`, `clerk_id` (unique), `username`, `email`, `created_at`. No passwords are stored; Clerk handles login
- **UserLessonProgress:** `user_id` + `lesson_id` (composite key), `completed_at`

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/health` | Health check | No |
| GET | `/me` | Returns the signed-in user's Clerk ID | Yes |
| GET | `/lessons` | List all lessons | No |
| GET | `/lessons/{id}` | Get one lesson | No |
| POST | `/lessons` | Create a lesson | No* |
| PATCH | `/lessons/{id}` | Update a lesson | No* |
| DELETE | `/lessons/{id}` | Delete a lesson | No* |

\* Write endpoints aren't protected yet. Adding admin-only access is on the to-do list.

When the backend is running, you can find interactive API docs at `http://localhost:8000/docs`.

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL
- A [Clerk](https://clerk.com) application (the free tier works)

### 1. Clone the repository
```bash
git clone https://github.com/VitaliiVas/SoccerLearningApp.git
cd SoccerLearningApp
```

### 2. Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/<database>
CLERK_JWKS_URL=https://<your-clerk-domain>/.well-known/jwks.json
```

Run the migrations and start the API:
```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

### 3. Frontend setup
```bash
cd frontend
npm install
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the dev server:
```bash
npm run dev
```

The app runs at `http://localhost:3000`.

## Design Approach

The project is deliberately kept simple: clear separation between the frontend, API and database, with complexity added only when it's needed. The core MVP comes first (authentication, interactive lessons and progress tracking), and extras like achievements or AI features come after.

## Author

**Vitalii Vasylets**, Computer Science student at the University of Washington Bothell
GitHub: [@VitaliiVas](https://github.com/VitaliiVas)
