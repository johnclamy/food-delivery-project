from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("🚀 Starting up the FastAPI application...")
    yield
    # Shutdown code here
    print("🪂 Shutting down the FastAPI application...")


app = FastAPI(
    title="Food Delivery App",
    description="This is a food delivery application built with FastAPI.",
    version="0.1.0",
    lifespan=lifespan
)


@app.get('/')
def root():
    return { 'message': 'testing food delivery app from main.py'}


if __name__ == '__main__':
    uvicorn.run(__name__ + ":app", host='0.0.0.0', port=8000, reload=True)
