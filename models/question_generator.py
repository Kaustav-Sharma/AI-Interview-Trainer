from groq import Groq
from typing import List, Dict, Optional

def generate_next_question(groq_key: str, job_role: str, experience_level: str, chat_history: List[Dict[str, str]], weakness_to_target: Optional[str] = None, voice_grades: Optional[Dict] = None) -> str:
    client = Groq(api_key=groq_key)
    system = f"You are a strict hiring manager interviewing a {experience_level} {job_role}. Ask ONE clear Verbal question."

    if not chat_history:
        prompt = "Ask a realistic technical question to start."
    else:
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        prompt = f"Interview History:\n{history_text}\n\nCandidate's last answer: '{chat_history[-1]['content']}'.\n"

        if voice_grades:
            prompt += f"VOICE ANALYSIS: {voice_grades.get('filler_word_count', 0)} filler words (um/uh), {voice_grades.get('words_per_minute', 0)} WPM, Tone: {voice_grades.get('dominant_sentiment', 'NEUTRAL')}.\n"
            prompt += "CRITICAL: If they used many filler words or sound nervous, call it out directly (e.g., 'You sound unsure,' or 'You are fumbling').\n"

        if weakness_to_target: prompt += f"Target this weakness: {weakness_to_target}."
        else: prompt += "Move to a new scenario."

    return client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.7
    ).choices[0].message.content.strip()
