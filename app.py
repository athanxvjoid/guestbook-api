from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.route("/")
def home():
    return "Flask Backend is Working!", 200

@app.route("/guestbook", methods=["GET"])
def get_entries():
    response = (
        supabase
        .table("guestbook")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return jsonify(response.data), 200

@app.route("/guestbook", methods=["POST"])
def add_entry():
    data = request.json

    if not data or not data.get("name") or not data.get("message"):
        return jsonify({"error": "Name and message required"}), 400

    supabase.table("guestbook").insert({
        "name": data["name"],
        "message": data["message"]
    }).execute()

    return jsonify({"success": True}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)