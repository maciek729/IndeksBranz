from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from processing.data_loader import DataLoader
from processing.index_calculator import IndustryIndexCalculator
from app.config import CORS_ORIGINS, DATA_YEARS
from routers import industries

app = FastAPI(title="Indeks Branż API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader = DataLoader()
calculator = IndustryIndexCalculator()

print("Loading and processing data...")
raw_data = loader.get_aggregated_data(start_year=DATA_YEARS['start'], end_year=DATA_YEARS['end'])
processed_data = calculator.process_full_pipeline(raw_data)
print(f"Processed {len(processed_data)} records")

industries.set_processed_data(processed_data)

app.include_router(industries.router)

@app.get("/")
def read_root():
    return {
        "message": "Indeks Branż API - PKO BP Hackathon",
        "version": "1.0.0",
        "endpoints": [
            "/api/industries",
            "/api/industries/{pkd_code}",
            "/api/stats",
            "/api/ranking"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
