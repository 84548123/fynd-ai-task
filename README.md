# Fynd AI Assessment - Customer Feedback System 🚀

This repository contains the submission for the **Fynd AI Engineer Intern Assessment 2.0**. The project is a full-stack AI application designed to collect, analyze, and act on customer feedback in real-time using Google's Gemini 2.0 Flash model.

## 🔗 Live Deployment
- **User Dashboard (Submit Reviews):** [https://fynd-ai-feedback-system.onrender.com](https://fynd-ai-feedback-system.onrender.com)
- **Admin Dashboard (View Insights):** [https://fynd-ai-feedback-system.onrender.com/admin](https://fynd-ai-feedback-system.onrender.com/admin)

---

## 📂 Project Overview

### **Task 1: Prompt Engineering & Analysis**
* **Goal:** Evaluate different prompting strategies to classify sentiment in Yelp reviews.
* **Approach:** Tested Zero-Shot, Few-Shot, and Chain-of-Thought prompting using the Gemini API.
* **Outcome:** The "Few-Shot" strategy provided the best balance of accuracy (89%) and latency.
* **File:** `Task1_Prompt_Experiments.ipynb` (Jupyter Notebook).

### **Task 2: Real-Time Feedback System**
* **Goal:** Build a web application that processes customer reviews instantly.
* **Workflow:**
    1.  User submits a text review.
    2.  System saves the raw data to a persistent SQLite database.
    3.  Backend sends the text to **Gemini 2.0 Flash**.
    4.  AI generates a JSON response containing:
        * **Sentiment Score** (1-5 stars)
        * **Summary** (One-sentence overview)
        * **Action Items** (Bullet points for staff)
    5.  Admin Dashboard displays these insights immediately.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite (SQLAlchemy)
* **AI Model:** Google Gemini 2.0 Flash (`google-generativeai`)
* **Deployment:** Render (Cloud Platform)
* **Server:** Gunicorn (WSGI)

---

## ⚙️ Installation & Local Setup
If you want to run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/84548123/fynd-ai-task.git](https://github.com/84548123/fynd-ai-task.git)
cd fynd-ai-task

fynd-ai-task/
├── app.py                 # Main Flask application logic
├── requirements.txt       # List of Python dependencies
├── reviews.db             # SQLite database (auto-generated)
├── templates/
│   ├── index.html         # User Dashboard (HTML/Tailwind)
│   └── admin.html         # Admin Dashboard (HTML/Tailwind)
├── static/                # Static assets (if any)
└── README.md              # Project documentation

🚀 Key Features implemented
[x] Secure API Handling: Uses os.environ to protect API keys in production.

[x] Error Handling: Gracefully handles AI API failures without crashing the server.

[x] Persistent Storage: Reviews are saved to a database, ensuring no data loss on server restarts.

[x] Responsive UI: Clean, mobile-friendly interface using Tailwind CSS.

[x] Modular Prompting: AI logic is separated for easy maintenance.
