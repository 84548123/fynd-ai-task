import os
import sqlite3
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace the string below with your actual API key for local testing.
# For deployment (Render), you will set this in the "Environment Variables" section.
API_KEY = "AIzaSyAEvmxF7DZmmGC9zNjTMbjn1knFAsgZa9Y"

genai.configure(api_key=API_KEY)

# Using Gemini Flash for speed and free-tier access 
model = genai.GenerativeModel('gemini-2.5-flash')
DB_NAME = "reviews.db"

# --- DATABASE SETUP ---
def init_db():
    """Initializes the SQLite database with required columns."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # We store the inputs (stars, review) and all 3 AI outputs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stars INTEGER,
                    review_text TEXT,
                    user_response TEXT,
                    admin_summary TEXT,
                    admin_actions TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize DB on start
init_db()

# --- LLM LOGIC (Server-Side) ---
def generate_ai_content(review_text, stars):
    """
    Generates User Response, Admin Summary, and Actions in a single API call.
    """
    prompt = f"""
    You are an AI customer service manager. Analyze this review:
    Rating: {stars}/5
    Review: "{review_text}"

    Return a valid JSON object with exactly these 3 keys:
    1. "user_response": A polite, short reply to the customer based on their rating.
    2. "summary": A 1-sentence summary of the review for the admin.
    3. "actions": A list of 2-3 short recommended actions for the business.

    Output ONLY raw JSON. Do not use Markdown formatting.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean potential markdown wrappers
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "")
        return json.loads(text)
    except Exception as e:
        print(f"LLM Error: {e}")
        # Graceful failure handling to prevent app crash
        return {
            "user_response": "Thank you for your feedback! We will review it shortly.",
            "summary": "AI generation failed.",
            "actions": ["Check system logs", "Manual review required"]
        }

# --- ROUTES ---

@app.route('/')
def user_dashboard():
    """Renders the User Dashboard"""
    return render_template('user_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    """Renders the Admin Dashboard"""
    return render_template('admin_dashboard.html')

# --- FIX: SILENCE FAVICON ERRORS ---
@app.route('/favicon.ico')
def favicon():
    """Returns an empty response to stop 404 errors in logs."""
    return '', 204

@app.route('/api/submit_review', methods=['POST'])
def submit_review():
    """Handles submission, calls AI, and saves to DB."""
    data = request.json
    stars = data.get('stars')
    review = data.get('review')

    if not stars or not review:
        return jsonify({"error": "Rating and review are required"}), 400

    print(f"Processing review: {review[:20]}...") # Log to terminal

    # 1. Server-side LLM Call
    ai_result = generate_ai_content(review, stars)

    # 2. Save to Persistent Database
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Serialize list of actions to string for storage
            actions_str = json.dumps(ai_result['actions'])
            
            cursor.execute('''
                INSERT INTO reviews (stars, review_text, user_response, admin_summary, admin_actions)
                VALUES (?, ?, ?, ?, ?)
            ''', (stars, review, ai_result['user_response'], ai_result['summary'], actions_str))
            conn.commit()
            
        print("Review saved to database.")
        
        # 3. Return only the user response to frontend
        return jsonify({
            "success": True, 
            "ai_response": ai_result['user_response']
        })
    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    """API endpoint for Admin Dashboard to fetch live data"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reviews ORDER BY id DESC')
            rows = cursor.fetchall()
            # Convert DB rows to list of dicts
            reviews = [dict(row) for row in rows]
        return jsonify(reviews)
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return jsonify([])

if __name__ == '__main__':
    # Running on port 5000 in debug mode
    app.run(debug=True, port=5000)