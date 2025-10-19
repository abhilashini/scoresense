import json
import random
from typing import Any, Dict, Optional, Type, Tuple, List
from google import genai
from google.genai import types

# Use relative import for modularity
from ..prompts import GraphicScorePrompts, response_art_config

class VisualizationGenerator:
    """
    AI Service for generating the visual representation and narrative 
    based on structured musical analysis data.
    """
    def __init__(self, client: genai.Client):
        self.client = client
        self.prompts_class = GraphicScorePrompts
        self.art_config = response_art_config

    def _generate_narration(self, data_summary: Dict[str, str]) -> str:
        """Generates a concise narrative based on the summarized musical features."""
        narration_prompt_text = f"""
        Based on the musical summary for '{data_summary['title']}' and the graphic style described below, create a concise narration (max 70 words) for a beginner/non-musician/deaf user. The narration MUST emphasize STRUCTURAL MAPPING and include the technical term in parentheses where appropriate.
        
        --- MUSIC SUMMARY --- 
        Style: {data_summary['key_mood']} Key, {data_summary['time_signature']} time. 
        Start: {data_summary['initial_tempo_desc']} ({data_summary['initial_tempo_term']}), {data_summary['initial_dynamics_desc']} ({data_summary['initial_dynamics_term']}), {data_summary['initial_articulation_term']} texture. 
        Highlight: {data_summary['rhythm_highlight']}
        """
        try:
            response_narration = self.client.models.generate_content(model="gemini-2.5-flash", contents=[narration_prompt_text])
            return response_narration.text.strip()
        except Exception as e:
            print(f"ERROR: Narration generation failed: {e}")
            return "[Error generating narrative. Focus on the core structural data.]"

    def generate_visualization(self, sheet_data: Dict[str, Any], sheet_data_raw_string: str, prompt_to_use: Optional[Tuple[str, str]] = None) -> Dict[str, Any]:
        """
        Generates narrative and image for a single, chosen prompt.
        
        :param sheet_data: The structured JSON output from MusicAnalyzer.
        :param sheet_data_raw_string: The stringified JSON data for prompt injection.
        :param prompt_to_use: Optional (name, prompt_string) tuple to force a style.
        """
        
        # 1. Select the prompt
        prompt_list = self.prompts_class.get_prompt_list()
        name, prompt = prompt_to_use if prompt_to_use else random.choice(prompt_list)
        
        # 2. Prepare summary for Narration
        try:
            data_summary = {
                "title": sheet_data.get("title", "The Music"),
                "key_mood": sheet_data.get("key_signature", "Neutral").split(" ")[0],
                "time_signature": sheet_data.get("time_signature", "N/A").split(" ")[0],
                "initial_tempo_desc": sheet_data.get("initial_tempo", {}).get("description", "A moderate pace"),
                "initial_tempo_term": sheet_data.get("initial_tempo", {}).get("term", "Moderato").strip("()"), 
                "initial_dynamics_desc": sheet_data.get("initial_dynamics", {}).get("description", "Quiet"),
                "initial_dynamics_term": sheet_data.get("initial_dynamics", {}).get("level", "p"),
                "initial_articulation_term": sheet_data.get("initial_dynamics", {}).get("articulation", "smoothly"),
                "rhythm_highlight": sheet_data.get("repeating_motifs", [{}])[0].get("description", "A consistent, simple beat."),
            }
        except Exception as e:
            return {"error": f"Failed to parse features for narration: {e}", "status": 500}

        # 3. Generate Narration and Image concurrently (sequentially here for simplicity)
        narration = self._generate_narration(data_summary)
        
        try:
            # Inject the JSON data string into the specific visualization prompt
            final_prompt = prompt.replace(self.prompts_class.json_string, sheet_data_raw_string)
            
            response_art = self.client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=[final_prompt], 
                config=self.art_config
            )

            image_base64 = ""
            for part in response_art.candidates[0].content.parts:
                if part.inline_data:
                    # Retrieve the base64 data
                    image_base64 = part.inline_data.data
                    # Convert bytes to utf-8 string for JSON serialization
                    if isinstance(image_base64, bytes):
                        image_base64 = image_base64.decode('utf-8') 
                    break 
            
            if not image_base64:
                 raise Exception("No image data found in response.")

            return {
                "title": sheet_data.get("title", "Untitled Score"),
                "visualization_type": name.replace('_', ' ').title(),
                "narration": narration,
                "image_base64": image_base64,
                "prompt_name": name, 
                "status": 200
            }

        except Exception as e:
            print(f"ERROR: Image generation failed for {name}: {e}")
            return {"error": f"Image generation failed: {e}", "status": 500}