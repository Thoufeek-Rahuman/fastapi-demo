from fastapi import FastAPI

from app.database import engine, Base
from app.routers import products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Demo",
    description="A demo API for managing products",
    version="1.0.0"
)

# Include routers
app.include_router(products.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to FastAPI Demo"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
