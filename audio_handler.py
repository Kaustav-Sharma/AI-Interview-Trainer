import asyncio
from groq import Groq
import edge_tts

def transcribe_audio(audio_file_path: str, groq_api_key: str) -> str:
    if not groq_api_key: raise ValueError("Groq API key is missing.")
    client = Groq(api_key=groq_api_key)
    with open(audio_file_path, "rb") as file:
        return client.audio.transcriptions.create(
            file=(audio_file_path, file.read()), model="whisper-large-v3", response_format="text"
        )

async def _generate_audio_async(text: str, output_file_path: str, voice: str = "en-US-AriaNeural"):
    await edge_tts.Communicate(text, voice).save(output_file_path)

def generate_tts(text: str, output_file_path: str = "interviewer_audio.mp3") -> str:
    asyncio.run(_generate_audio_async(text, output_file_path))
    return output_file_path
