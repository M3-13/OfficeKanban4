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
- Board CRUD endpoints (list/create/get implemented, update/delete stubs)
- Column CRUD endpoints with owner guard
- Card CRUD endpoints with card move/reorder and owner guard
- React frontend with auth context, protected routes, responsive login/register pages
- Kanban board view with column lanes, cards, and drag & drop (@dnd-kit)

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
Create a new board.

**Request:**
```json
{"title": "string (1-100 chars)"}
```

**Response (201):**
```json
{"id": 1, "title": "My Board", "owner_id": 1}
```

### GET /boards/{board_id}
Get a single board. Requires owner access (403 otherwise).

**Response (200):**
```json
{"id": 1, "title": "My Board", "owner_id": 1}
```

### PUT /boards/{board_id}
Update a board. *(stub – currently returns 501)*

### DELETE /boards/{board_id}
Delete a board. *(stub – currently returns 501)*

### GET /boards/{board_id}/columns
List columns for a board, sorted by position. Requires owner access.

**Response (200):**
```json
[{"id": 1, "title": "To Do", "position": 0, "board_id": 1}]
```

### POST /boards/{board_id}/columns
Create a new column with auto-assigned position.

**Request:**
```json
{"title": "string (1-100 chars)"}
```

**Response (201):**
```json
{"id": 1, "title": "To Do", "position": 0, "board_id": 1}
```

### PUT /boards/{board_id}/columns/{column_id}
Rename a column.

**Request:**
```json
{"title": "string (1-100 chars)"}
```

**Response (200):**
```json
{"id": 1, "title": "New Title", "position": 0, "board_id": 1}
```

### DELETE /boards/{board_id}/columns/{column_id}
Delete a column and all its cards. Returns 204.

### GET /columns/{column_id}/cards
List cards in a column, sorted by position. Requires board owner access.

**Response (200):**
```json
[{"id": 1, "title": "Task", "description": "", "position": 0, "column_id": 1}]
```

### POST /columns/{column_id}/cards
Create a new card with auto-assigned position.

**Request:**
```json
{"title": "string (1-200 chars)", "description": "string (optional)"}
```

**Response (201):**
```json
{"id": 1, "title": "Task", "description": "", "position": 0, "column_id": 1}
```

### PUT /cards/{card_id}
Update a card's title and/or description.

**Request:**
```json
{"title": "string (optional)", "description": "string (optional)"}
```

**Response (200):**
```json
{"id": 1, "title": "Updated", "description": "Desc", "position": 0, "column_id": 1}
```

### PUT /cards/{card_id}/move
Move a card to a different column and/or position. Other cards are reordered automatically.

**Request:**
```json
{"column_id": 2, "position": 0}
```

**Response (200):**
```json
{"id": 1, "title": "Task", "description": "", "position": 0, "column_id": 2}
```

### DELETE /cards/{card_id}
Delete a card. Requires board owner access. Returns 204.
