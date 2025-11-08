# 🎶 ScoreSense: AI-Powered Musical Visualization

**ScoreSense** was born from a common challenge: for many novices, sheet music is a complex, abstract barrier to intuitively feeling and understanding a piece's true emotional and dynamic structure.

The project is fundamentally about bridging this gap using Generative AI. It draws inspiration from the rich tradition of graphic scores, which visualize music's form, as explored by artists like [David Hall](https://davidhall.io/visualising-music-graphic-scores/). The concept is further informed by contemporary methods such as [light painting music visualization](https://www.designer-daily.com/visualizing-music-with-the-help-of-light-painting-54503) and real-time visualization systems like [Partitura](https://cdm.link/partitura-spectacular-real-time-visualization-of-music-and-thinking-in-1d/). These artistic methods confirm that music, structure, and visual art are deeply interconnected - a concept explored in depth by authors and composers of ["Notations 21"](https://www.amazon.com/dp/0979554640/).

ScoreSense automates this artistic translation using the Gemini API's multimodal capabilities. It translates complex PDF sheet music into accessible visual art and simple, structural narratives. This tool is designed to help novices, students, and individuals with visual or hearing impairments gain an intuitive understanding of a piece's core structure, rhythm, and emotional dynamics.

## 🖼️ Demo Gallery: Visualizing Music's Core

These screenshots illustrate the ScoreSense application interface and show how complex sheet music is translated into a structured narrative and a corresponding visual score, offering an intuitive "guided listen."

| Musical Score | Generated Narrative & Visualization |
| :--- | :--- |
| **Sonata No. 14 "Moonlight"** | ![Moonlight Sonata 3D Ribbon Score](https://github.com/abhilashini/scoresense/blob/main/assets/Moonlight.png?raw=true) |
| **L'inaccessible étoile** | ![L'inaccessible étoile Bio Luminescent Path](https://github.com/abhilashini/scoresense/blob/main/assets/L'inaccessible%20e%CC%81toile.png?raw=true) |

### Note on Visualization Consistency
Visualization may not be pixel-for-pixel consistent across runs due to artistic variations in the underlying image generation model. The core musical data mapping, however, remains strictly deterministic.

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
