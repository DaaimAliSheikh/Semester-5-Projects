from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.db.main import init_db
from fastapi.middleware.cors import CORSMiddleware
from src.users.routes import user_router
from src.caterings.routes import catering_router
from src.venues.routes import venue_router
import logging


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server starting up...")
    await init_db()  # creates the tables
    yield
    print(f"Stopping server...")


app = FastAPI(lifespan=life_span)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your React app's URL
    allow_credentials=True,  # allow client to send cookies
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_router)
app.include_router(catering_router)
app.include_router(venue_router)


@app.exception_handler(Exception)
async def global_exception_handler(request:Request,exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )
