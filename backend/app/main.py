import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.app.routers import entries


app = FastAPI(title="Journal & Mood Tracker API")


# CORS — allow the React dev server by default
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(entries.router, prefix="/api")

# Create tables on startup (dev convenience). Replace with Alembic later if you want.
# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:  # type: AsyncEngine
#         await conn.run_sync(Base.metadata.create_all)
