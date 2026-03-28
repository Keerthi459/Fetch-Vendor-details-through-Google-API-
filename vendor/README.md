How to Run the Project

This project has two parts: Backend (API) and Frontend (UI).
You must run both in separate terminals.

1️⃣ Start the Backend (FastAPI Server)

Open terminal in the main project folder (vendor) and run:

python -m uvicorn api:app --reload

If successful, you will see:

Uvicorn running on http://127.0.0.1:8000
2️⃣ Start the Frontend (Web Server)

Open a new terminal and go to the frontend folder:

cd frontend
python -m http.server 8080
3️⃣ Open the Application

Open your browser and go to:

http://localhost:8080

Now you can search vendors by location and category.