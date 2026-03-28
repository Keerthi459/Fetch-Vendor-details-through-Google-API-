Vendor Intelligence System
🚀 Overview

A location-based system that fetches real vendor data using the Google Places API (New), processes it with cleaning and ranking logic, and displays it through a FastAPI backend and simple frontend dashboard.

⚙️ Setup
pip install fastapi uvicorn requests python-dotenv
uvicorn api:app --reload

Frontend:

cd frontend
python -m http.server 5500
🔑 Environment Variable
GOOGLE_API_KEY=your_api_key
🛠 Features
Location-based vendor fetch
Data cleaning & deduplication
Vendor ranking
FastAPI backend
Search, filter, sort UI
📦 Output
Vendor data in JSON/DB
Interactive dashboard
