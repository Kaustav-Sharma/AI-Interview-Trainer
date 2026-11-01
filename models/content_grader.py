from groq import Groq
import json

def grade_text_content(groq_key: str, job_role: str, experience_level: str, question: str, answer_transcript: str) -> dict:
    client = Groq(api_key=groq_key)
    system = f"Grade a {experience_level} {job_role}. Output STRICTLY in JSON with exact keys: technical_score (int), communication_score (int), strengths (list of strings), weaknesses (list of strings), ideal_answer_snippet (string)."
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": f"Question: {question}\nAnswer: {answer_transcript}"}],
        temperature=0.2, response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
