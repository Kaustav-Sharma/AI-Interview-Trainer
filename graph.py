import asyncio
from typing import Dict, Any
from audio_handler import transcribe_audio, generate_tts
from models.content_grader import grade_text_content
from models.voice_grader import grade_voice_delivery
from models.orchestrator import evaluate_turn_and_route
from models.question_generator import generate_next_question

async def _run_graders_concurrently(audio_path, transcript, question, job_role, exp_level, groq_key, assembly_key):
    voice_task = asyncio.to_thread(grade_voice_delivery, audio_path, assembly_key)
    content_task = asyncio.to_thread(grade_text_content, groq_key, job_role, exp_level, question, transcript)
    return await asyncio.gather(voice_task, content_task)

def run_interview_turn(state: Dict[str, Any], api_keys: Dict[str, str]) -> Dict[str, Any]:
    audio_path = state["current_answer_audio_path"]
    transcript = transcribe_audio(audio_path, api_keys["groq"])
    state["current_answer_text"] = transcript
    state["chat_history"].append({"role": "candidate", "content": transcript})
    
    voice_grades, content_grades = asyncio.run(_run_graders_concurrently(
        audio_path, transcript, state["current_question"], state["job_role"], 
        state["experience_level"], api_keys["groq"], api_keys["assembly"]
    ))
    
    state["latest_voice_grades"] = voice_grades
    state["latest_content_grades"] = content_grades
    state["all_metrics"].append({
        "question": state["current_question"],
        "answer": transcript,
        "voice": voice_grades,
        "content": content_grades
    })
    
    state["question_count"] += 1
    routing = evaluate_turn_and_route(api_keys["groq"], state["question_count"], content_grades, voice_grades)
    
    if routing.get("decision") == "stop":
        state["is_active"] = False
        state["final_judgment"] = routing.get("final_judgment")
    else:
        state["weakness_to_target"] = routing.get("weakness_to_target")
        next_q = generate_next_question(api_keys["groq"], state["job_role"], state["experience_level"], state["chat_history"], state["weakness_to_target"], voice_grades)
        state["current_question"] = next_q
        state["chat_history"].append({"role": "interviewer", "content": next_q})
        generate_tts(next_q, "interviewer_audio.mp3")
        
    return state
