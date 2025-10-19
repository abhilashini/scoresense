import json
from typing import Any, Dict, Optional
from google import genai
from google.genai import types

class MusicAnalyzer:
    """
    AI Service for analyzing sheet music features using a constrained Gemini prompt.
    This service translates a raw file into structured, machine-readable data (JSON).
    """
    def __init__(self, client: genai.Client, model: str = "gemini-2.5-flash"):
        self.client = client
        self.model = model
        self.prompt_template = """
You are an expert AI musicologist. Analyze the uploaded sheet music to translate its core structure and feeling into a strictly defined JSON object.

GOAL: The analysis must be structured and descriptive, suitable for both human reading and machine-readable visualization mapping.

--- RESPONSE FORMAT (MUST be a single JSON object) ---
{{
    "title": "Piece Title or Placeholder", 
    "composer": "Composer Name or Unknown",
    "key_signature": "Major/Minor (e.g., 'C Minor')", 
    "time_signature": "Time structure (e.g., '4/4')",
    "initial_tempo": {{ "bpm": "100", "description": "Tempo term (e.g., 'Moderato', 'A steady, measured speed')", "term": "Moderato" }},
    "initial_dynamics": {{ "level": "mf", "description": "Loudness term (e.g., 'Moderately loud')", "articulation": "Texture (e.g., 'smoothly', 'sharp/staccato')" }},
    "overall_mood": "Emotional quality (e.g., 'Determined and slightly melancholy')",
    "structural_analysis": [{{ 
        "section_id": "A", 
        "feature_focus": "Melody", 
        "description": "Melody contour (e.g., 'gently moving up and down like shallow waves.')", 
        "pitch_range_midinotes": "List of typical MIDI notes (e.g., [55, 60, 65, 67])" 
    }}],
    "repeating_motifs": [{{ "type": "Rhythmic", "description": "A driving, consistent 'long-short-short' beat repeats every two measures.", "duration": "2 measures" }}]
}}
--- END OF RESPONSE FORMAT ---
Return ONLY the JSON object. Do not include any explanation or markdown text outside the JSON block.
"""

    def extract_features(self, uploaded_file: types.File) -> Optional[Dict[str, Any]]:
        """Calls the Gemini model to analyze the file and extract structured musical features."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[uploaded_file, self.prompt_template],
            )
            
            raw_text = response.text.strip()
            
            # Simple cleanup for common markdown wrapper if present
            if raw_text.startswith("```"):
                raw_text = raw_text.lstrip("```json").rstrip("```")
                
            return json.loads(raw_text)
            
        except json.JSONDecodeError as e:
            print(f"ERROR: Music Analyzer failed to parse model output as JSON: {e}")
            return None
        except Exception as e:
            print(f"ERROR: Gemini API call failed during feature extraction: {e}")
            return None