from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__)
expenses_collection = None

def set_collection(collection):
    global expenses_collection
    expenses_collection = collection

# 1. Combined Route for GET and POST
@expenses_bp.route('/expenses', methods=['GET', 'POST'])
def handle_expenses():
    if expenses_collection is None:
        return jsonify({"error": "Database collection not initialized"}), 500

    # --- HANDLE GET (Fetching Expenses) ---
    if request.method == 'GET':
        try:
            expenses = list(expenses_collection.find().sort('date', -1))
            for expense in expenses:
                expense['_id'] = str(expense['_id'])
            return jsonify(expenses), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- HANDLE POST (Saving New Expense) ---
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            new_expense = {
                "amount": float(data.get('amount')),
                "category": data.get('category'),
                "description": data.get('description', ''),
                "date": data.get('date'),
                "created_at": datetime.now()
            }

            result = expenses_collection.insert_one(new_expense)
            return jsonify({"_id": str(result.inserted_id), "status": "success"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# 2. Route for DELETE
@expenses_bp.route('/expenses/<id>', methods=['DELETE'])
def delete_expense(id):
    try:
        result = expenses_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Deleted successfully"}), 200
        return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500