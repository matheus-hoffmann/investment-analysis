import os
import requests
from openai import OpenAI

from src.handlers.abstract.speech2text_interface import Speech2TextInterface


class OpenAITranscriberHandler(Speech2TextInterface):
    def transcribe(self, local_path, return_raw = True):
        url = f"{os.getenv("AZURE_OPENAI_ENDPOINT")}openai/deployments/{os.getenv("AZURE_OPENAI_AUDIO_DEPLOYMENT_NAME")}/audio/transcriptions?api-version={os.getenv("AZURE_OPENAI_AUDIO_API_VERSION")}"
        headers = {"Authorization": f"Bearer {os.getenv("AZURE_OPENAI_API_KEY")}"}
        files = {"file": (f"audio.{local_path.split('.')[-1]}", open(local_path, "rb"), f"audio/{local_path.split('.')[-1]}")}
        data = {"model": os.getenv("AZURE_OPENAI_AUDIO_DEPLOYMENT_NAME")}
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            response = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            return None
        return response if return_raw else response["text"]