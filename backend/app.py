from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from routes.expenses import expenses_bp, set_collection
import config

# 1. Initialize Flask app
app = Flask(__name__)

# 2. CORS setup
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

# 3. MongoDB Connection Logic
def get_db_connection():
    try:
        # Use the URI from your config.py
        client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Verify connection is alive
        client.admin.command('ping')
        
        db = client[config.DATABASE_NAME]
        return db, client
    except ServerSelectionTimeoutError:
        raise Exception("Could not connect to MongoDB. Make sure MongoDB is running.")
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")

# 4. & 5. Initialize Database and Register Routes
# Global variable to store the client for the health check
mongo_client = None

try:
    db, mongo_client = get_db_connection()
    expenses_collection = db[config.COLLECTION_NAME]
    
    # Pass the database connection to your routes
    set_collection(expenses_collection)
    
    # Register the blueprint AFTER setting the collection
    app.register_blueprint(expenses_bp, url_prefix='/api')
    
    print("✓ Connected to MongoDB and Routes Registered")
except Exception as e:
    print(f"✗ Setup failed: {str(e)}")
    print("TIP: Ensure MongoDB is running on localhost:27017")

# 6. Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    if not mongo_client:
        return jsonify({"status": "unhealthy", "database": "not initialized"}), 500
    try:
        mongo_client.admin.command('ping')
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

# 7. Start the server
if __name__ == '__main__':
    print("Starting Expense Tracker API on http://localhost:5000")
    # Use config.DEBUG to control debug mode
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)