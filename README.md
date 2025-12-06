# FastAPI + React TypeScript Foundation Project

A basic foundation project with FastAPI backend and React TypeScript frontend that displays "Hello World".

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── main.py       # Main FastAPI application
│   ├── requirements.txt
│   └── .gitignore
├── frontend/         # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx   # Main React component
│   │   └── App.css
│   └── package.json
└── README.md
```

## Backend Setup (FastAPI)

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Navigate to the backend folder:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Mac/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Backend

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at http://localhost:8000

API Endpoints:
- `GET /` - Returns a simple hello world message
- `GET /api/hello` - Returns a hello world message (used by frontend)

## Frontend Setup (React TypeScript)

### Prerequisites
- Node.js 16 or higher
- npm or yarn

### Installation

1. Navigate to the frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Running the Frontend

```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## Running Both Services

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment first (see above)
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser to see the "Hello World" app with the frontend communicating with the backend.

## Features

- FastAPI backend with CORS enabled
- React TypeScript frontend with Vite
- API integration between frontend and backend
- Clean project structure ready for expansion

## Next Steps

- Add more API endpoints in [backend/main.py](backend/main.py)
- Create new React components in [frontend/src/](frontend/src/)
- Add database integration
- Add authentication
- Add testing
