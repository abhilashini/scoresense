import os
from google import genai
from google.genai import types
from typing import Optional

class FileManagement:
    """
    Utility class for non-AI file operations: 
    local file saving, API file uploading, and API file deletion.
    """
    def __init__(self, client: genai.Client):
        self.client = client

    def upload_to_api(self, local_file_path: str) -> Optional[types.File]:
        """Uploads a local file (e.g., PDF) to the Gemini API for processing."""
        try:
            # client.files.upload() returns a types.File object
            uploaded_file = self.client.files.upload(file=local_file_path)
            # In a real app, this would use a proper logging system
            print(f"File uploaded. Resource name: {uploaded_file.name}") 
            return uploaded_file
        except Exception as e:
            print(f"ERROR: Failed to upload file to Gemini API: {e}")
            return None

    def delete_api_file(self, uploaded_file: types.File) -> None:
        """Deletes the file resource from the Gemini API service."""
        try:
            self.client.files.delete(name=uploaded_file.name)
            print(f"API file deleted successfully: {uploaded_file.name}")
        except Exception as e:
            print(f"WARNING: Failed to delete API file {uploaded_file.name}: {e}")

    def save_local_file(self, file_stream, filename: str, upload_folder: str) -> str:
        """Saves an incoming file stream temporarily to the local filesystem."""
        filepath = os.path.join(upload_folder, filename)
        file_stream.save(filepath)
        return filepath
        
    def cleanup_local_file(self, filepath: str) -> None:
        """Removes a file from the local filesystem."""
        if os.path.exists(filepath):
            os.remove(filepath)