from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.seed import load_policies_from_csv


load_policies_from_csv()

from app.routers.policy import router as policy_router


app = FastAPI(
    title="Travel Policy Assistant",
    description="API for answering questions about the travel expense policy.",
    version="1.0.0",
)

app.include_router(policy_router)


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)