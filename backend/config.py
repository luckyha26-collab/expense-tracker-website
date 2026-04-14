import os
import config
# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "expense_tracker_db"
COLLECTION_NAME = "expenses"

# Flask Configuration
DEBUG = True

# CORS Configuration
# This allows your frontend to talk to the backend
CORS_ORIGINS = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000"]