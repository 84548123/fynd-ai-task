# Google Cloud Run Automated Deployment Script for Customer AI Feedback System
param (
    [Parameter(Mandatory=$false)]
    [string]$ProjectId = "",

    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",

    [Parameter(Mandatory=$false)]
    [string]$GeminiApiKey = $env:GEMINI_API_KEY
)

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  La Maison Customer AI System - GCP Cloud Run Deploy" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# 1. Check if gcloud is installed
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Host "`n[!] Google Cloud SDK (gcloud) is not found in PATH." -ForegroundColor Yellow
    Write-Host "Please install it from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    Write-Host "Or run these commands inside the Google Cloud Shell in your browser console.`n" -ForegroundColor Yellow
    Exit 1
}

# 2. Authenticate and select project
if ([string]::IsNullOrWhiteSpace($ProjectId)) {
    $currentProject = gcloud config get-value project 2>$null
    if ([string]::IsNullOrWhiteSpace($currentProject) -or $currentProject -match "\(unset\)") {
        $ProjectId = Read-Host "Enter your GCP Project ID"
    } else {
        $ProjectId = $currentProject
    }
}

Write-Host "`n[+] Configuring GCP Project: $ProjectId" -ForegroundColor Green
gcloud config set project $ProjectId

# 3. Prompt for Gemini API Key if missing
if ([string]::IsNullOrWhiteSpace($GeminiApiKey)) {
    $GeminiApiKey = Read-Host "Enter your GEMINI_API_KEY (from Google AI Studio)"
}

# 4. Enable required APIs
Write-Host "`n[+] Enabling Cloud Run, Cloud Build, and Artifact Registry APIs..." -ForegroundColor Green
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 5. Deploy directly to Google Cloud Run
Write-Host "`n[+] Deploying to Google Cloud Run (Region: $Region)..." -ForegroundColor Green
gcloud run deploy customer-ai-feedback `
    --source . `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars GEMINI_API_KEY="$GeminiApiKey" `
    --min-instances 0 `
    --max-instances 2 `
    --memory 512Mi `
    --cpu 1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=====================================================" -ForegroundColor Green
    Write-Host "  ✅ Successfully Deployed to Google Cloud Run!" -ForegroundColor Green
    Write-Host "=====================================================" -ForegroundColor Green
    $serviceUrl = gcloud run services describe customer-ai-feedback --platform managed --region $Region --format 'value(status.url)'
    Write-Host "`n🌐 Live Application URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "📊 Admin Dashboard URL:  $serviceUrl/admin" -ForegroundColor Cyan
} else {
    Write-Host "`n[X] Deployment failed. Check the error messages above." -ForegroundColor Red
}
