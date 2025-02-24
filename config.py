import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = os.getenv("DEBUG", True)
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///esg_analyzer.db")
