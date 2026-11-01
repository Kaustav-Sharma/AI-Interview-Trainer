from typing import TypedDict, List, Dict, Optional, Any

class InterviewState(TypedDict):
    job_role: str
    experience_level: str
    chat_history: List[Dict[str, str]]
    current_question: str
    current_answer_audio_path: Optional[str]
    current_answer_text: Optional[str]
    latest_voice_grades: Optional[Dict[str, Any]]
    latest_content_grades: Optional[Dict[str, Any]]
    all_metrics: List[Dict[str, Any]]
    question_count: int
    weakness_to_target: Optional[str]
    is_active: bool
    final_judgment: Optional[str]

def initialize_state(job_role: str, experience_level: str) -> InterviewState:
    return {
        "job_role": job_role, "experience_level": experience_level,
        "chat_history": [], "current_question": "",
        "current_answer_audio_path": None, "current_answer_text": None,
        "latest_voice_grades": None, "latest_content_grades": None,
        "all_metrics": [],
        "question_count": 0, "weakness_to_target": None,
        "is_active": True, "final_judgment": None
    }
