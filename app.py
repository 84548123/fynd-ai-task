import os
import sqlite3
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# This tells the app: "Look for the key in the secure Environment Variables"
API_KEY = os.environ.get("GEMINI_API_KEY")

# Safety Check: If the key is missing, print an error to the logs
if not API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in environment variables!")

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

            # --- MENU ITEMS TABLE ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    category TEXT NOT NULL,
                    emoji TEXT DEFAULT '🍽️',
                    orders_count INTEGER DEFAULT 0,
                    is_bestseller INTEGER DEFAULT 0,
                    is_available INTEGER DEFAULT 1
                )
            ''')

            # Seed menu items if table is empty
            cursor.execute('SELECT COUNT(*) FROM menu_items')
            if cursor.fetchone()[0] == 0:
                seed_menu_items(cursor)
                print("Menu items seeded successfully.")

            # Seed initial reviews if table is empty
            cursor.execute('SELECT COUNT(*) FROM reviews')
            if cursor.fetchone()[0] == 0:
                seed_initial_reviews(cursor)
                print("Initial reviews seeded successfully.")

            conn.commit()
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")


def seed_menu_items(cursor):
    """Seeds the menu with popular restaurant items."""
    items = [
        # Starters
        ("Truffle Mushroom Soup", "Creamy wild mushroom soup with truffle oil drizzle", 349, "Starters", "🍄", 1820, 1, 1),
        ("Bruschetta Trio", "Tomato basil, olive tapenade & ricotta honey on sourdough", 299, "Starters", "🍞", 1540, 1, 1),
        ("Crispy Calamari", "Golden fried squid rings with spicy aioli & lemon", 399, "Starters", "🦑", 1210, 0, 1),
        ("Caesar Salad", "Romaine, parmesan crisps, croutons & house-made dressing", 279, "Starters", "🥗", 980, 0, 1),

        # Main Course
        ("Grilled Ribeye Steak", "200g prime ribeye with herb butter, roasted vegetables & mashed potatoes", 899, "Main Course", "🥩", 2450, 1, 1),
        ("Pan-Seared Salmon", "Atlantic salmon with lemon dill sauce, asparagus & quinoa", 749, "Main Course", "🐟", 1980, 1, 1),
        ("Butter Chicken", "Tender chicken in rich tomato-cream gravy with naan & rice", 449, "Main Course", "🍛", 3200, 1, 1),
        ("Margherita Wood-Fired Pizza", "San Marzano tomatoes, fresh mozzarella, basil on hand-tossed dough", 499, "Main Course", "🍕", 2870, 1, 1),
        ("Mushroom Risotto", "Arborio rice slow-cooked with porcini, parmesan & white wine", 549, "Main Course", "🍚", 1650, 1, 1),
        ("Lamb Shank", "Slow-braised lamb with rosemary jus, polenta & roasted root vegetables", 799, "Main Course", "🍖", 1120, 0, 1),
        ("Pasta Carbonara", "Spaghetti with smoked pancetta, egg yolk, pecorino & black pepper", 449, "Main Course", "🍝", 1890, 1, 1),

        # Desserts
        ("Tiramisu", "Classic Italian coffee-mascarpone layers with cocoa dust", 349, "Desserts", "🍰", 2100, 1, 1),
        ("Molten Chocolate Lava Cake", "Warm dark chocolate cake with vanilla bean ice cream", 399, "Desserts", "🍫", 2680, 1, 1),
        ("Crème Brûlée", "Vanilla custard with caramelized sugar crust", 329, "Desserts", "🍮", 1450, 0, 1),
        ("Mango Cheesecake", "Baked cheesecake topped with fresh Alphonso mango coulis", 379, "Desserts", "🥭", 1320, 0, 1),

        # Beverages
        ("Signature Mojito", "Fresh mint, lime, soda & a secret house twist (non-alcoholic)", 249, "Beverages", "🍹", 3100, 1, 1),
        ("Cold Brew Coffee", "18-hour slow-steeped cold brew served over ice", 199, "Beverages", "☕", 2750, 1, 1),
        ("Berry Smoothie Bowl", "Blended açai, berries & banana topped with granola & chia", 299, "Beverages", "🫐", 1680, 0, 1),
        ("Fresh Watermelon Juice", "Chilled pressed watermelon with a hint of mint", 179, "Beverages", "🍉", 2200, 1, 1),
    ]

    cursor.executemany('''
        INSERT INTO menu_items (name, description, price, category, emoji, orders_count, is_bestseller, is_available)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', items)


def seed_initial_reviews(cursor):
    """Seeds realistic restaurant reviews for executive briefing analysis."""
    sample_reviews = [
        (5, "The grilled ribeye steak was cooked to absolute perfection and the truffle soup was divine! Romantic ambiance and great hospitality.",
         "Thank you so much! We are thrilled to hear your anniversary dinner was memorable.",
         "Customer praised steak doneness, truffle soup, and romantic ambiance.",
         json.dumps(["Maintain consistent meat grilling standards", "Compliment kitchen team on truffle soup"])),
        
        (5, "Exceptional service by our waiter Marco. The Molten Lava cake is the best dessert in the city! Will definitely return.",
         "Thank you for recognizing Marco! We are delighted you loved the lava cake.",
         "High praise for server Marco and molten chocolate lava cake.",
         json.dumps(["Acknowledge Marco during pre-shift staff briefing", "Ensure sufficient chocolate lava cake stock"])),

        (4, "Delicious wood-fired pizza and fresh burrata. The drinks took a little long on Friday evening, but food made up for it.",
         "We are glad you loved the pizza! We are streamlining bar service during peak hours.",
         "Positive food rating; minor delay noted in beverage turnaround on busy night.",
         json.dumps(["Review bar service queue during Friday peak dinner rush", "Ensure extra barback on weekend shifts"])),

        (2, "The salmon was fresh but arrived slightly lukewarm, and we waited 25 minutes for our table despite having a reservation.",
         "We sincerely apologize for the table delay and lukewarm entree. Our GM would like to host you for a private tasting.",
         "Negative feedback regarding table reservation wait time and entree temperature.",
         json.dumps(["Audit reservation seating buffers on weekend peak", "Review hot-holding pass procedures in kitchen"])),

        (5, "Celebrated my birthday here. The mushroom risotto and cold brew cocktail pairing was outstanding! 10/10.",
         "Happy Birthday! Thank you for choosing La Maison for your celebration.",
         "Flawless birthday dining experience praising risotto and signature pairings.",
         json.dumps(["Log guest birthday preference in VIP CRM", "Maintain risotto ingredient sourcing"]))
    ]

    cursor.executemany('''
        INSERT INTO reviews (stars, review_text, user_response, admin_summary, admin_actions)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_reviews)


# Initialize DB on start
init_db()

# --- LLM LOGIC (Server-Side) ---
def generate_ai_content(review_text, stars):
    """
    Generates User Response, Admin Summary, Admin Actions, Customer Suggestions, and Recommended Dishes in a single API call.
    """
    prompt = f"""
    You are an AI customer experience manager at 'La Maison', a luxury fine-dining restaurant.
    Analyze this customer review:
    Rating: {stars}/5
    Review: "{review_text}"

    Available Menu Specialties:
    - Truffle Mushroom Soup (Starters)
    - Bruschetta Trio (Starters)
    - Grilled Ribeye Steak (Main Course)
    - Pan-Seared Salmon (Main Course)
    - Butter Chicken (Main Course)
    - Margherita Wood-Fired Pizza (Main Course)
    - Mushroom Risotto (Main Course)
    - Pasta Carbonara (Main Course)
    - Tiramisu (Desserts)
    - Molten Chocolate Lava Cake (Desserts)
    - Signature Mojito (Beverages)
    - Cold Brew Coffee (Beverages)

    Return a valid JSON object with exactly these keys:
    1. "user_response": A warm, polite, and personal reply from the General Manager thanking them or addressing feedback (2 sentences).
    2. "summary": A 1-sentence analytical summary of the review for the management dashboard.
    3. "actions": A list of 2-3 short recommended actions for the restaurant staff.
    4. "customer_suggestions": A list of 2-3 personalized suggestions/perks for the customer on their next visit (e.g. food pairing advice, chef recommendation, special table seating tip).
    5. "recommended_dishes": A list of 2 dish names from the menu list above that this customer would love to try next based on their review.

    Output ONLY raw JSON. Do not use Markdown formatting.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"LLM Error: {e}")
        if stars >= 4:
            fallback_response = "Thank you so much for dining with us at La Maison! We are delighted to hear you had a wonderful experience."
            fallback_suggestions = [
                "Pair your next main course with our handcrafted Signature Mojito or 18-hour Cold Brew.",
                "Reserve our courtyard garden table for a candlelit evening ambiance.",
                "Try our chef-special Molten Chocolate Lava Cake on your next visit!"
            ]
            fallback_dishes = ["Grilled Ribeye Steak", "Molten Chocolate Lava Cake"]
        else:
            fallback_response = "Thank you for sharing your candid feedback. We deeply care about your experience and our culinary team is addressing your notes immediately."
            fallback_suggestions = [
                "Ask for our Head Sommelier for personalized pairings tailored to your palate.",
                "Our Chef would love to prepare our signature Truffle Mushroom Soup on your return.",
                "Enjoy priority seating with dedicated table service on your next reservation."
            ]
            fallback_dishes = ["Truffle Mushroom Soup", "Tiramisu"]

        return {
            "user_response": fallback_response,
            "summary": f"Customer gave a {stars}-star rating with feedback: {review_text[:60]}...",
            "actions": ["Review kitchen preparation notes", "Share feedback with floor manager"],
            "customer_suggestions": fallback_suggestions,
            "recommended_dishes": fallback_dishes
        }


def generate_executive_briefing(reviews):
    """
    Generates an analytical Executive Briefing report across all aggregated customer reviews using Gemini.
    """
    total = len(reviews)
    if total == 0:
        return {
            "executive_summary": "No customer reviews recorded yet. Collect initial feedback to generate a briefing.",
            "sentiment_health_score": 100,
            "top_praises": ["Awaiting initial guest feedback"],
            "recurring_pain_points": ["No issues reported"],
            "chef_action_items": ["Monitor new dish reception"],
            "hospitality_action_items": ["Prepare floor staff for guest check-ins"]
        }

    avg_rating = sum(r['stars'] for r in reviews) / total
    sample_text = "\n".join([f"- [{r['stars']} Stars]: {r['review_text']}" for r in reviews[:15]])

    prompt = f"""
    You are the Chief Culinary & Operations Consultant for 'La Maison', a luxury fine-dining restaurant.
    Review this aggregated guest feedback dataset ({total} total reviews, Average Rating: {avg_rating:.2f}/5):

    Sample Feedback Log:
    {sample_text}

    Generate a high-level, actionable Executive Management Briefing in valid JSON with exactly these keys:
    1. "executive_summary": A concise 2-3 sentence strategic overview of overall dining sentiment and guest satisfaction.
    2. "sentiment_health_score": An integer score from 0 to 100 representing current guest sentiment health.
    3. "top_praises": A list of 3 specific strengths or most celebrated highlights (dishes, ambiance, staff).
    4. "recurring_pain_points": A list of 2-3 critical areas needing improvement or recurring customer friction points.
    5. "chef_action_items": A list of 2 high-impact culinary directives for the Executive Chef & kitchen line.
    6. "hospitality_action_items": A list of 2 operational directives for the General Manager & service team.

    Output ONLY raw JSON without Markdown formatting.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Executive Report LLM Error: {e}")
        # Smart analytical fallback calculation
        health = int((avg_rating / 5.0) * 100)
        return {
            "executive_summary": f"La Maison is maintaining a strong {avg_rating:.1f}/5 average rating across {total} logged guest reviews. Guests frequently praise the steak and dessert offerings, while weekend wait times remain the primary operational focus.",
            "sentiment_health_score": health,
            "top_praises": [
                "Exceptional steak doneness and truffle culinary preparations",
                "High guest satisfaction with desserts (Molten Lava Cake, Tiramisu)",
                "Romantic ambiance and courteous floor hospitality"
            ],
            "recurring_pain_points": [
                "Weekend peak dinner reservation wait times",
                "Occasional delays in cocktail bar service during Friday rushes"
            ],
            "chef_action_items": [
                "Ensure strict heat-holding standards on salmon and fish stations",
                "Maintain premium sourcing consistency for prime ribeye cuts"
            ],
            "hospitality_action_items": [
                "Assign an extra barback during Friday-Saturday 7 PM - 10 PM peak services",
                "Implement proactive table-ready SMS notifications for reservations"
            ]
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
    """Handles submission, calls AI, saves to DB, and returns rich customer suggestions."""
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
            actions_str = json.dumps(ai_result.get('actions', []))
            
            cursor.execute('''
                INSERT INTO reviews (stars, review_text, user_response, admin_summary, admin_actions)
                VALUES (?, ?, ?, ?, ?)
            ''', (stars, review, ai_result.get('user_response', ''), ai_result.get('summary', ''), actions_str))
            conn.commit()
            
        print("Review saved to database.")
        
        # 3. Return rich user response, suggestions, and recommendations to frontend
        return jsonify({
            "success": True, 
            "ai_response": ai_result.get('user_response', 'Thank you for your review!'),
            "customer_suggestions": ai_result.get('customer_suggestions', []),
            "recommended_dishes": ai_result.get('recommended_dishes', [])
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
            reviews = [dict(row) for row in rows]
        return jsonify(reviews)
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return jsonify([])

@app.route('/api/generate_executive_report', methods=['POST', 'GET'])
def get_executive_report():
    """Generates an on-demand AI executive briefing analyzing all logged customer reviews."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reviews ORDER BY id DESC')
            rows = cursor.fetchall()
            reviews = [dict(row) for row in rows]
        
        report = generate_executive_briefing(reviews)
        return jsonify({"success": True, "report": report, "reviews_analyzed": len(reviews)})
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({"error": str(e)}), 500


# --- MENU ITEM ROUTES ---

@app.route('/api/best_sellers', methods=['GET'])
def get_best_sellers():
    """Returns top-selling menu items, optionally filtered by category."""
    category = request.args.get('category', None)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if category and category != 'All':
                cursor.execute('''
                    SELECT * FROM menu_items
                    WHERE is_available = 1 AND category = ?
                    ORDER BY orders_count DESC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT * FROM menu_items
                    WHERE is_available = 1
                    ORDER BY orders_count DESC
                ''')
            rows = cursor.fetchall()
            items = [dict(row) for row in rows]
        return jsonify(items)
    except Exception as e:
        print(f"Error fetching menu items: {e}")
        return jsonify([])

@app.route('/api/menu_categories', methods=['GET'])
def get_menu_categories():
    """Returns distinct menu categories."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT category FROM menu_items WHERE is_available = 1 ORDER BY category')
            categories = [row[0] for row in cursor.fetchall()]
        return jsonify(categories)
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify([])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)