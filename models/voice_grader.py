import assemblyai as aai
from typing import Dict, Any

def grade_voice_delivery(audio_path: str, assembly_key: str) -> Dict[str, Any]:
    aai.settings.api_key = assembly_key
    transcript = aai.Transcriber(config=aai.TranscriptionConfig(sentiment_analysis=True, disfluencies=True)).transcribe(audio_path)
    if transcript.error: return {"error": transcript.error}

    dur_min = transcript.audio_duration / 60.0
    wpm = round(len(transcript.words) / dur_min) if transcript.words and dur_min > 0 else 0
    fillers = sum(1 for w in transcript.words if w.text.lower().strip(",.") in ["um", "uh", "like", "ah", "you know"]) if transcript.words else 0

    sents = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    if transcript.sentiment_analysis:
        for res in transcript.sentiment_analysis: sents[res.sentiment] += 1
    dom = max(sents, key=sents.get) if any(sents.values()) else "NEUTRAL"
    return {"words_per_minute": wpm, "filler_word_count": fillers, "dominant_sentiment": dom}
