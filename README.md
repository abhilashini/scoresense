# 🎶 ScoreSense: AI-Powered Musical Visualization

**ScoreSense** transforms complex PDF sheet music into accessible visual art and simple, structural narratives using the Gemini API. This project aims to bridge the gap between technical musical notation and intuitive understanding, particularly for novices, students, and those with visual or hearing impairments.

## ✨ Quick Overview

ScoreSense uses a modular, two-stage GenAI pipeline:
1.  **Analysis:** Extracts musical features (tempo, key, dynamics) from an uploaded PDF.
2.  **Visualization & Narration:** Maps those features onto an artistic prompt to generate a stunning visual score and a concise, beginner-friendly narrative.

## 🚀 Setup and Installation

This project is configured to run smoothly using **Visual Studio Code Dev Containers** (Codespaces).

### Prerequisites

* Git
* Node.js (LTS recommended)
* Python 3.10+
* **A Google Gemini API Key**

### A. Initial Setup (Manual Method)

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/abhilashini/scoresense.git](https://github.com/abhilashini/scoresense.git)
    cd scoresense
    ```

2.  **Set Environment Variables:**
    Set your Gemini API key in your terminal session or a `.env` file (if using dotenv):
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  **Install Dependencies:**
    You need two terminals for the concurrent backend and frontend processes.

    **Terminal 1 (Backend - Python):**
    ```bash
    # Setup Virtual Environment
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    **Terminal 2 (Frontend - Node.js):**
    ```bash
    npm install --prefix ./frontend
    ```

4.  **Start the Servers:**

    **Terminal 1: Start Flask Backend (API)**
    ```bash
    export FLASK_APP=backend.app
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    flask run --host 0.0.0.0 --port 5000
    ```

    **Terminal 2: Start React Frontend (UI)**
    ```bash
    npm run dev --prefix ./frontend
    ```
    Open the address displayed (usually `http://localhost:3000` or the Codespace port URL).

## 💡 Architecture

The application employs a clean separation of concerns:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS | Provides the accessible, centered Gold/Charcoal UI. Uses a **Vite Proxy** to route API calls to the backend. |
| **Backend API** | Python, Flask, Flask-CORS | Handles routing, file management, and orchestration of the GenAI pipeline. |
| **AI Services** | `google-genai` SDK | Modular services for **Analysis** (PDF to JSON), **Narration** (text generation), and **Visualization** (image generation). |
