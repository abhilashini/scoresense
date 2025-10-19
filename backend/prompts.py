from google.genai import types
from typing import List, Tuple

# --- CONFIGURATION AND GLOBAL CONSTANTS ---

# Configuration for image generation (requesting both image and potentially text/metadata)
response_art_config = types.GenerateContentConfig(
    response_modalities=[types.Modality.IMAGE, types.Modality.TEXT] 
)

# Text block for output consistency management
CONSISTENCY_DISCLAIMER = (
    "Visualization may not be pixel-for-pixel consistent across runs due to artistic variations in the underlying image generation model. The core musical data mapping, however, remains strictly deterministic."
)

# --- GRAPHIC SCORE PROMPTS CLASS ---
class GraphicScorePrompts:
    """Contains highly deterministic prompt templates for visualization."""
    # Placeholder string for structured JSON data insertion
    json_string = "JSON_DATA_STRING_FOR_MAPPING" 
 
    # NOTE: Prompts are abbreviated here. In a real scenario, these 
    # must contain the detailed, deterministic mapping rules.
    chromatic_landscape = f"A precise, cinematic 3D generative landscape visualization of music. Terrain height is proportional to amplitude (dynamic level). Refer {json_string} for precise guidance on pitch, amplitude, and instrument mapping."
    constellation_score = f"A deterministic cosmic data-art visualization. Vertical position (Y-axis) must be strictly mapped to MIDI pitch number. Refer {json_string} for quantitative data."
    watercolor_flow_prompt = f"A deterministic, flowing watercolor visualization of music, rendered as a dynamic, liquid abstract painting. Color Saturation encodes volume/dynamics. Refer {json_string} for data-driven consistency."
    panoramic_waveform_prompt = f"A deterministic panoramic visualization of music, rendered as a vast, undulating landscape of colorful waves. Vertical height (Amplitude) must be strictly proportional to pitch register. Refer {json_string} for quantitative mapping rules."
    light_painting_dynamic_score = f"A dark, cinematic photo composition featuring a vibrant, dynamic light painting. Light path vertical curve must be strictly mapped to the melodic contour (pitch changes). Refer {json_string} for guidance."
    abstract_3d_ribbon_score = f"A mesmerizing, high-resolution 3D abstract sculpture of sound. Ribbon Thickness encodes dynamics/amplitude. Refer {json_string} for guidance on mapping pitch range, dynamics, polyphony, and instrumental timbres to the 3D structure."
    data_cityscape = f"A futuristic cityscape where skyscraper height represents pitch and window density represents rhythm complexity. Deterministic mapping required. Refer {json_string}."
    geometric_tapestry = f"A complex, deterministic geometric tapestry where color shifts map to key changes and thread thickness maps to texture/polyphony. Refer {json_string}."
    fractal_growth_score = f"A visualization showing a fractal branching structure. Branching angle and speed are strictly mapped to tempo and dynamic shifts. Refer {json_string}."
    bio_luminescent_path = f"A mysterious bio-luminescent path in a deep ocean. Light intensity maps to dynamics; path curvature maps to melodic direction. Refer {json_string}."

    @classmethod
    def get_prompt_list(cls) -> List[Tuple[str, str]]:
        """Returns a list of tuples: (attribute_name, prompt_string)."""
        return [
            (name, getattr(cls, name))
            for name in dir(cls)
            if not name.startswith("__")
            and name not in ("json_string", "get_prompt_list")
        ]