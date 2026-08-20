# 🍽️ La Maison — AI-Powered Customer Feedback & Restaurant Intelligence System

[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud%20Run-Deployed-4285F4?logo=googlecloud&logoColor=white)](https://customer-ai-feedback-1035927964593.us-central1.run.app)
[![Gemini 2.5 Flash](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Flash-8E75B2?logo=googlegemini&logoColor=white)](https://aistudio.google.com)
[![Flask](https://img.shields.io/badge/Backend-Flask%20%7C%20Python%203.12-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack, enterprise-grade AI customer experience and executive operations platform built for **La Maison** fine dining. The system processes customer dining reviews in real time using **Google Gemini 2.5 Flash**, delivers instant personalized dining suggestions to guests, and generates strategic 1-click executive briefings for restaurant management.

---

## 🌐 Live Cloud Deployments (Google Cloud Platform)

| Portal | Live URL | Description |
|---|---|---|
| **🍽️ Guest Feedback & Menu Portal** | [https://customer-ai-feedback-1035927964593.us-central1.run.app](https://customer-ai-feedback-1035927964593.us-central1.run.app) | Priority 5-star review form, post-review VIP AI suggestions, and interactive Best Sellers menu |
| **📊 Executive Admin Portal** | [https://customer-ai-feedback-1035927964593.us-central1.run.app/admin](https://customer-ai-feedback-1035927964593.us-central1.run.app/admin) | Real-time review analytics, live sentiment tracking, and 1-Click AI Executive Operations Briefing |

---

## ✨ Key Features & Capabilities

### 🌟 1. Guest Experience Portal (`/`)
- **⭐️ Priority Review Submission**: Interactive 5-star rating selector with real-time feedback emojis (🤩 *Excellent* → 😞 *Terrible*) and character counter.
- **✨ Post-Review VIP AI Suggestions Showcase**:
  - **General Manager's Note**: Warm, AI-personalized note crafted by Gemini addressing specific guest feedback.
  - **💡 Tailored Next-Visit Perks**: Actionable recommendations (wine/beverage pairings, intimate table seating tips, chef tasting recommendations).
  - **🍽️ Click-to-Locate Handpicked Dishes**: Interactive dish buttons that smoothly scroll down to the Best Sellers menu and highlight matching items with a gold pulse animation.
- **🔥 Best Sellers & Culinary Highlights**: Category filter tabs (*All*, *Starters*, *Main Course*, *Desserts*, *Beverages*) with order counters and popularity tags.
- **📐 Company-Standard 2-Column Split Ratio**: Balanced 44% Sticky Feedback : 56% Dynamic Menu Grid on desktop inside a 1280px container, seamlessly responsive on mobile.

---

### 👑 2. Executive Management & Review Intelligence (`/admin`)
- **🤖 1-Click AI Executive Briefing**:
  - **🩺 Sentiment Health Score**: Real-time gauge (0–100) assessing overall dining satisfaction.
  - **📜 Strategic Executive Summary**: High-level overview of dining sentiment across all logged reviews.
  - **🏆 Guest Praises & Strengths**: Key culinary highlights, celebrated dishes, and praised staff members.
  - **⚠️ Critical Operational Friction Points**: Identifies recurring pain points (e.g. peak weekend table wait times, bar turnaround).
  - **👨‍🍳 Chef & Kitchen Directives**: Operational action items for the kitchen pass and recipe consistency.
  - **🤵 Floor & Hospitality Directives**: Actionable staffing and service directives for the General Manager.
- **📊 1:1:1:1 KPI Metric Grid**: Total Reviews, Average Rating, Positive Reviews (4–5⭐), and Needs Attention (1–2⭐).
- **🔍 Filter & Search Engine**: Instant star-rating filtering (All / 5 / 4 / 3 / 2 / 1) and live full-text search across reviews and summaries.

---

## 🛠️ Tech Stack & Architecture

```
                                  +-----------------------------+
                                  |   Google Cloud Run (GCP)    |
                                  |   Serverless Docker Host    |
                                  +--------------+--------------+
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                                                               |
         v                                                                               v
+------------------+                                                           +-------------------+
|  Guest Portal /  |                                                           |   Admin Portal    |
| (user_dashboard) |                                                           | (admin_dashboard) |
+--------+---------+                                                           +---------+---------+
         |                                                                               |
         |  POST /api/submit_review                               POST /api/generate_    |
         |  GET  /api/best_sellers                                executive_report       |
         v                                                                               v
+--------------------------------------------------------------------------------------------------+
|                                    Flask Application Backend (app.py)                            |
|                                    Gunicorn WSGI Server (PORT: 8080)                             |
+--------------------------------+-----------------------------------------------+-----------------+
                                 |                                               |
                                 v                                               v
                 +-------------------------------+               +-------------------------------+
                 |    Google Gemini 2.5 Flash    |               |       SQLite Database         |
                 |      (Prompt Engineering)     |               |         (reviews.db)          |
                 +-------------------------------+               +-------------------------------+
```

* **Frontend:** Semantic HTML5, CSS3 Custom Properties (60-30-10 Design System), Vanilla JS (Zero heavy dependencies).
* **Backend:** Python 3.12, Flask, Gunicorn WSGI Server.
* **AI Engine:** Google Gemini 2.5 Flash (`google-generativeai`).
* **Database:** SQLite with persistent storage and automatic schema initialization.
* **Cloud Infrastructure:** Google Cloud Run, Google Cloud Build, Google Artifact Registry, Docker.

---

## 🚀 Local Installation & Setup

### Prerequisites
* Python 3.10+
* Google Gemini API Key ([Get one free at Google AI Studio](https://aistudio.google.com/apikey))

### 1. Clone the Repository
```bash
git clone https://github.com/84548123/Customer_AI_Feedback_System.git
cd Customer_AI_Feedback_System
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables & Run
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
python app.py

# macOS / Linux (Bash)
export GEMINI_API_KEY="your_api_key_here"
python app.py
```

Open in your browser:
* **User Portal**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Admin Portal**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

---

## 🐳 Docker Container Deployment

### Build & Run Locally
```bash
# Build Docker image
docker build -t customer-ai-feedback:latest .

# Run container on port 8080
docker run -d -p 8080:8080 -e GEMINI_API_KEY="your_api_key_here" --name restaurant-ai customer-ai-feedback:latest
```
Access at [http://localhost:8080](http://localhost:8080).

---

## ☁️ Google Cloud Run Deployment

Deploy directly to GCP using the Google Cloud SDK:

```bash
gcloud run deploy customer-ai-feedback \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --clear-base-image \
  --set-env-vars GEMINI_API_KEY="your_api_key_here"
```

---

## 📂 Project Structure

```
Customer_AI_Feedback_System/
├── app.py                     # Main Flask application & Gemini API integration
├── requirements.txt           # Python dependencies (Flask, google-generativeai, Gunicorn)
├── Dockerfile                 # Multi-stage production container definition
├── .dockerignore              # Docker build exclusions
├── app.yaml                   # Google App Engine deployment configuration
├── cloudbuild.yaml            # Google Cloud Build CI/CD pipeline
├── deploy_gcp.ps1             # Automated PowerShell GCP deployment script
├── GCP_DEPLOYMENT_GUIDE.md    # Step-by-step cloud deployment documentation
├── templates/
│   ├── user_dashboard.html    # La Maison Guest Experience & Menu Portal
│   └── admin_dashboard.html   # Executive Review Intelligence & Briefing Portal
├── Dinakar_Fynd_Ai_Engineer.ipynb  # Task 1 Prompt Engineering Jupyter Notebook
├── Dinakar_Saipogu_Fynd_Assessment_2.pdf # Assessment documentation & report
└── README.md                  # Project documentation & live links
```

---

## 🔒 Security & Best Practices
- **Credential Protection**: Uses `os.environ` to isolate API keys in production; no hardcoded keys in application code.
- **Graceful Error Handling**: Fallback mechanisms handle API quota limits (`429 Resource Exhausted`) smoothly without crashing the server.
- **Serverless Autoscaling**: Scales down to 0 instances when idle on Google Cloud Run to ensure zero unwanted infrastructure cost.

---

## 👤 Author
* **Dinakar Saipogu**
* **Project**: AI-Powered Customer Feedback & Restaurant Intelligence System
* **Submission**: Fynd AI Engineer Assessment
