from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from .resources.database import DatabaseManager, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")

    # Initialize AGHU DB Manager and store in app.state
    aghu_dsn = os.getenv("POSTGRES_DSN")
    if aghu_dsn:
        app.state.aghu_db = DatabaseManager(aghu_dsn)
        print("AGHU PostgreSQL connection pool initialized.")
    else:
        print("WARNING: POSTGRES_DSN not found. Skipping AGHU DB initialization.")

    # Initialize App DB Manager (SQLite) and store in app.state
    app_dsn = os.getenv("SQLITE_DSN")
    if not app_dsn:
        raise ValueError("SQLITE_DSN not found in environment variables.")
    app.state.app_db = DatabaseManager(app_dsn)
    print("App SQLite connection pool initialized.")

    # Create tables for App DB (if they don't exist) - for development only, Alembic handles this in production
    async with app.state.app_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("App SQLite tables checked/created.")

    yield

    # Shutdown
    print("Shutting down...")
    if hasattr(app.state, 'aghu_db') and app.state.aghu_db:
        await app.state.aghu_db.close_connection()
        print("AGHU PostgreSQL connection pool closed.")
    if hasattr(app.state, 'app_db') and app.state.app_db:
        await app.state.app_db.close_connection()
        print("App SQLite connection pool closed.")

app = FastAPI(
    title="Esqueleto de Aplicação Web Full-Stack",
    description="Aplicação Backend monolítica (API REST) em Python/FastAPI, com foco em acesso e agregação de dados heterogêneos.",
    version="1.0.0",
    lifespan=lifespan,
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # frontend local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(os.getenv("URL_ORIGIN"))

# Placeholder para incluir os roteadores da API
from .routers import paciente, auth, admin, jornada, dashboard
app.include_router(paciente.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(jornada.router)
app.include_router(dashboard.router)
from pathlib import Path

# ... depois dos app.include_router(...)

BASE_DIR = Path(__file__).resolve().parent  # aponta pra src/
STATIC_DIR = BASE_DIR / "static" / "dist"

# serve tudo que está em src/static/dist sob o prefixo /static/dist
app.mount("/static/dist", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve o index.html para rotas do SPA (Vue Router).
    """
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API route not found")

    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "Frontend build not found"}

from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    print(f"Origin: {request.headers.get('origin')}")
    print(f"Host: {request.headers.get('host')}")
    response = await call_next(request)
    print(f"Response headers: {response.headers}")
    return response

# Exemplo:
# from .routers import aih, bpa, material
# app.include_router(aih.router)
# app.include_router(bpa.router)
# app.include_router(material.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
