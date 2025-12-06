# Indeks Branż Polski - PKO BP Hackathon

Aplikacja do analizy kondycji i perspektyw rozwoju branż w Polsce na podstawie danych finansowych i wskaźników ryzyka.

## Struktura Projektu

```
IndeksBranz/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── config/
│   │   │   └── settings.py  # Konfiguracja (wagi, progi kategorii)
│   │   └── models/
│   │       └── schemas.py   # Modele Pydantic dla API
│   ├── routers/
│   │   └── industries.py    # API endpoints
│   ├── processing/          # Logika przetwarzania danych
│   │   ├── data_loader.py   # Ładowanie i agregacja danych
│   │   └── index_calculator.py  # Obliczanie indeksu
│   ├── data/                # Dane źródłowe CSV
│   └── main.py              # Aplikacja główna
│
├── frontend/               # React TypeScript Frontend
│   └── src/
│       ├── components/     # Komponenty React
│       │   ├── Dashboard.tsx
│       │   ├── KPICard.tsx
│       │   ├── CategoryCard.tsx
│       │   └── RankingTable.tsx
│       ├── constants/      # Stałe konfiguracyjne
│       ├── services/       # API service
│       ├── types/          # TypeScript typy
│       └── utils/          # Funkcje pomocnicze
│
└── README.md
```

## Technologie

**Backend:**
- FastAPI
- Pandas, NumPy
- Scikit-learn

**Frontend:**
- React 18
- TypeScript
- Vite

## Instalacja i Uruchomienie

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend dostępny na: http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny na: http://localhost:5173

## Metodologia Indeksu

Indeks obliczany jest jako średnia ważona 5 wskaźników:

- **30%** - Ryzyko upadłości (odwrócone)
- **25%** - Dynamika przychodów
- **20%** - Rentowność (marża zysku)
- **15%** - Wielkość branży
- **10%** - Efektywność (udział firm rentownych)

### Klasyfikacja

- **A** (70-100 pkt) - Rozwijające się
- **B** (50-69 pkt) - Stabilne
- **C** (30-49 pkt) - Wymagające monitorowania
- **D** (0-29 pkt) - Ryzykowne

## API Endpoints

- `GET /api/stats` - Statystyki ogólne
- `GET /api/industries` - Lista wszystkich branż
- `GET /api/industries/{pkd_code}` - Szczegóły branży
- `GET /api/ranking` - Top 10 i Bottom 10 branż

## Źródła Danych

- Dane finansowe przedsiębiorstw (GUS)
- Krajowy Rejestr Zadłużonych (upadłości)
- Klasyfikacja PKD 2007 (poziom działu - 2 cyfry)

## Licencja

MIT
