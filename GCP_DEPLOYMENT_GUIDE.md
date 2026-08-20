# 🚀 Google Cloud Platform (GCP) Deployment Guide

This project is fully containerized and production-ready for **Google Cloud Run** and **Google App Engine**.

---

## ⚡ Method 1: Google Cloud Run (Recommended — 2 Minutes)

Google Cloud Run provides serverless autoscaling (scales down to 0 instances when not in use to save cost) and automatic HTTPS.

### Step 1: Open Google Cloud Shell
Go to [console.cloud.google.com](https://console.cloud.google.com) and click the **Cloud Shell** icon (`>_`) in the top navigation bar.

### Step 2: Clone or Upload Project
```bash
git clone https://github.com/84548123/Customer_AI_Feedback_System.git
cd Customer_AI_Feedback_System
```

### Step 3: Run the One-Line Deploy Command
```bash
gcloud run deploy customer-ai-feedback \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

* Cloud Build will automatically build the container and deploy it.
* Within ~90 seconds, you will receive a live HTTPS URL:
  `https://customer-ai-feedback-xxxxxx.a.run.app`

---

## 🔄 Method 2: Automatic GitHub Continuous Deployment (CI/CD)

1. Push this codebase to your GitHub repository.
2. In the Google Cloud Console, navigate to **Cloud Run** → **Create Service**.
3. Select **"Continuously deploy from a repository"**.
4. Connect your GitHub account and select `Customer_AI_Feedback_System`.
5. Set Build Type to **Dockerfile** (already configured in root).
6. Under **Variables & Secrets**, add:
   - `GEMINI_API_KEY`: `your_key_here`
7. Click **Create**. Any new commits will auto-build and deploy!

---

## 📦 Method 3: Google App Engine (Standard Environment)

We have provided [`app.yaml`](app.yaml):

```bash
# In Cloud Shell or Local Terminal with gcloud:
gcloud app create --region=us-central
gcloud app deploy app.yaml
```

---

## 📁 GCP Deployment Files Included

| File | Purpose |
|---|---|
| [`Dockerfile`](Dockerfile) | Multi-stage production container with Gunicorn WSGI server on `$PORT` |
| [`.dockerignore`](.dockerignore) | Filters local caches, virtual environments, and temporary files |
| [`cloudbuild.yaml`](cloudbuild.yaml) | Google Cloud Build CI/CD pipeline definition |
| [`app.yaml`](app.yaml) | App Engine standard environment runtime config |
| [`deploy_gcp.ps1`](deploy_gcp.ps1) | Automated PowerShell deployment script |
