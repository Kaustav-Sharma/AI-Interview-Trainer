from groq import Groq
import json
from typing import Dict, Any

def evaluate_turn_and_route(groq_key: str, question_count: int, content_grades: Dict[str, Any], voice_grades: Dict[str, Any]) -> dict:
    client = Groq(api_key=groq_key)
    system = "Output STRICTLY in JSON with exact keys: decision (string: 'continue' or 'stop'), weakness_to_target (string or null), final_judgment (string or null). If questions >= 5, decision must be 'stop' and provide final_judgment."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": f"Questions: {question_count}/5\nContent Grades: {json.dumps(content_grades)}\nVoice Grades: {json.dumps(voice_grades)}"}],
        temperature=0.1, response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
