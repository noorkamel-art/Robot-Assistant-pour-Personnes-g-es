from fastapi import FastAPI
from backend.database import init_database

app = FastAPI(
    title="Robot Assistant API",
    description="Backend du Robot Assistant pour Personnes Âgées",
    version="1.0.0"
)
init_database()


@app.get("/")
def home():
    return {
        "message": "Robot Assistant Backend fonctionne !"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


