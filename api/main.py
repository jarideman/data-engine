from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from connection import init_mt5, deinit_mt5


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not init_mt5():
        raise RuntimeError("Failed to initialize MT5 for API")

    try:
        yield
    finally:
        deinit_mt5()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
