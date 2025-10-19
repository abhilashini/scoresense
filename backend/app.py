import os
import json
import random
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from google import genai
from typing import Any, Dict, Optional, Tuple, List
from flask_cors import CORS

# Import Modular Services
from .utils.file_management import FileManagement
from .services.analysis_service import MusicAnalyzer 
from .services.visualization_service import VisualizationGenerator
from .prompts import GraphicScorePrompts, CONSISTENCY_DISCLAIMER

# ====================================================================
# A. FLASK SETUP AND INITIALIZATION
# ====================================================================

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the Gemini Client
try:
    client = genai.Client() 
except Exception as e:
    print(f"FATAL: Failed to initialize Gemini Client. Check API Key environment variable. Error: {e}")
    client = None

# Initialize modular service instances
if client:
    file_manager = FileManagement(client)
    analyzer = MusicAnalyzer(client)
    generator = VisualizationGenerator(client)
else:
    # Use placeholder classes if client fails to initialize
    class MockService:
        def __init__(self, *args, **kwargs): pass
        def __call__(self, *args, **kwargs): return {"error": "Client unavailable"}, 503
    
    file_manager = MockService(None)
    analyzer = MockService(None)
    generator = MockService(None)

# Store persistent data (in a real app, use a secure DB/Cache)
music_data_store: Dict[str, Any] = {} 
last_prompt_name: Optional[str] = None

# ====================================================================
# B. API ROUTES
# ====================================================================

@app.route("/api/trivia", methods=["GET"])
def get_music_trivia():
    """Endpoint for fetching a quick music fact during the loading process."""
    if not client:
        return jsonify({"trivia": "Music is the space between the notes. - Claude Debussy"}), 200
    try:
        trivia_prompt = "Generate one single 10-second digestible snippet/trivia from the music world. Start directly with the fact, no salutations or headings."
        response = client.models.generate_content(model="gemini-2.5-flash", contents=[trivia_prompt])
        return jsonify({"trivia": response.text.strip()})
    except Exception as e:
        print(f"Trivia error: {e}")
        return jsonify({"trivia": "Music is the space between the notes. - Claude Debussy"}), 200


@app.route("/api/process-music", methods=["POST"])
def process_music_file():
    """
    Handles file upload, feature extraction, and initial visualization generation.
    """
    global last_prompt_name
    
    if not client:
        return jsonify({"error": "Gemini client not initialized. Check API Key."}), 503
        
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file selected."}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    # 1. Local File Management (Non-AI)
    filepath = file_manager.save_local_file(file, filename, app.config['UPLOAD_FOLDER'])
    
    # 2. API File Upload (Non-AI)
    uploaded_file = file_manager.upload_to_api(filepath)
    file_manager.cleanup_local_file(filepath) # Clean up temporary local file

    if not uploaded_file:
        return jsonify({"error": "Failed to upload file to processing API."}), 500

    # 3. Feature Extraction (AI Service 1)
    music_features_dict = analyzer.extract_features(uploaded_file)
    
    file_manager.delete_api_file(uploaded_file) # Clean up the Gemini File API resource
    
    if not music_features_dict:
        return jsonify({"error": "Failed to extract structured musical features."}), 500

    # 4. Visualization Generation (AI Service 2)
    music_data_store['current_score'] = music_features_dict 
    last_prompt_name = None 
    
    music_features_raw_string = json.dumps(music_features_dict)
    result = generator.generate_visualization(music_features_dict, music_features_raw_string)
    
    if result.get("status") != 200:
        return jsonify({"error": result.get("error")}), result.get("status")

    last_prompt_name = result.get("prompt_name")
    result["disclaimer"] = CONSISTENCY_DISCLAIMER
    return jsonify(result), 200

@app.route("/api/regenerate", methods=["POST"])
def regenerate_visual():
    """
    Generates a new, random visualization using the previously analyzed music data.
    This hits only the Visualization Generator Service (AI Service 2).
    """
    global last_prompt_name
    
    if not client:
        return jsonify({"error": "Gemini client not initialized. Check API Key."}), 503
        
    music_features_dict = music_data_store.get('current_score')
    if not music_features_dict:
        return jsonify({"error": "No music data found. Please upload a file first."}), 400

    music_features_raw_string = json.dumps(music_features_dict)
    
    # Logic to ensure the *new* prompt is different from the *last* one
    all_prompts = GraphicScorePrompts.get_prompt_list()
    available_prompts = [p for p in all_prompts if p[0] != last_prompt_name]
    
    # Pick a prompt
    prompt_to_use = random.choice(available_prompts) if available_prompts else random.choice(all_prompts)

    # Visualization Generation (AI Service 2)
    result = generator.generate_visualization(
        music_features_dict, 
        music_features_raw_string, 
        prompt_to_use=prompt_to_use
    )

    if result.get("status") != 200:
        return jsonify({"error": result.get("error")}), result.get("status")

    last_prompt_name = result.get("prompt_name")
    result["disclaimer"] = CONSISTENCY_DISCLAIMER
    return jsonify(result), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # The application will run on port 5000 inside the dev container
    app.run(host='0.0.0.0', port=5000, debug=True)