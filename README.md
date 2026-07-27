# OfficeKanban4

Mehrbenutzerfähiges Kanban-Board mit Web-UI. Jeder User verwaltet seine eigenen
Boards mit Spalten und Karten. Authentifizierung per JWT.

## Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy (ORM), SQLite, python-jose (JWT), bcrypt
- **Frontend:** React 18+, Vite, TypeScript, React Router, Axios

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## How to Run

### Backend (dev server, port 8000)

```bash
cd backend
JWT_SECRET=your-secret-key uvicorn backend.main:app --reload
```

### Frontend (dev server, port 5173)

```bash
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## Umgebungsvariablen

| Variable | Default | Beschreibung |
|---|---|---|
| `JWT_SECRET` | *(required)* | Secret key for JWT signing |
| `JWT_EXPIRATION_MINUTES` | `15` | Token lifetime in minutes |
| `DATABASE_URL` | `sqlite:///officekanban.db` | Database connection URL |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | Frontend origin for CORS |

## Features

- User registration and login with JWT authentication
- Password hashing with bcrypt
- Protected API endpoints with Bearer token auth
- CORS configured for frontend dev server
- Board, Column, and Card CRUD endpoints (stubs)
- React frontend with auth context, protected routes, and responsive login/register pages

## API Endpoints

### POST /auth/register
Create a new user account. Returns a JWT token.

**Request:**
```json
{"username": "string (3-50 chars)", "password": "string (6-100 chars)"}
```

**Response (201):**
```json
{"access_token": "string", "token_type": "bearer"}
```

### POST /auth/login
Authenticate and receive a JWT token.

**Request:**
```json
{"username": "string", "password": "string"}
```

**Response (200):**
```json
{"access_token": "string", "token_type": "bearer"}
```

### GET /auth/me
Return the current authenticated user. Requires `Authorization: Bearer <token>`.

**Response (200):**
```json
{"id": 1, "username": "alice"}
```

### GET /boards
List boards for the authenticated user. *(stub – currently returns 501)*

### POST /boards
Create a new board. *(stub – currently returns 501)*

### GET /boards/{board_id}
Get a single board. *(stub – currently returns 501)*

### PUT /boards/{board_id}
Update a board. *(stub – currently returns 501)*

### DELETE /boards/{board_id}
Delete a board. *(stub – currently returns 501)*

### GET/POST /boards/{board_id}/columns
Column endpoints. *(stub – currently returns 501)*

### PUT/DELETE /boards/{board_id}/columns/{column_id}
Single column endpoints. *(stub – currently returns 501)*

### GET/POST /columns/{column_id}/cards
Card endpoints. *(stub – currently returns 501)*

### PUT/DELETE /columns/{column_id}/cards/{card_id}
Single card endpoints. *(stub – currently returns 501)*
