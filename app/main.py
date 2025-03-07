from fastapi import FastAPI
from .database import engine, Base
from .routes import routes

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI Project Setup Complete!"}
