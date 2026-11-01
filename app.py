import gradio as gr
from state import initialize_state
from graph import run_interview_turn
from audio_handler import generate_tts
from models.question_generator import generate_next_question

def start_interview(job_role, exp_level, groq_key, assembly_key):
    if not (groq_key and assembly_key):
        return gr.update(), None, None, "Error: Missing Keys", gr.update(), None
    state = initialize_state(job_role, exp_level)
    first_q = generate_next_question(groq_key, job_role, exp_level, [])
    state["current_question"] = first_q
    state["chat_history"].append({"role": "interviewer", "content": first_q})
    generate_tts(first_q, "interviewer_audio.mp3")
    return [{"role": "assistant", "content": first_q}], state, "interviewer_audio.mp3", "Interview Active!", gr.update(value=None), None

def process_turn(audio_path, state, groq_key, assembly_key):
    if not audio_path or state is None or not state["is_active"]:
        return gr.update(), state, None, "Start interview first.", gr.update(), None

    state["current_answer_audio_path"] = audio_path
    state = run_interview_turn(state, {"groq": groq_key, "assembly": assembly_key})

    chat_ui = [{"role": "user" if m["role"] == "candidate" else "assistant", "content": m["content"]} for m in state["chat_history"]]
    metrics = {"Voice": state.get("latest_voice_grades"), "Content": state.get("latest_content_grades")}
    return chat_ui, state, "interviewer_audio.mp3" if state["is_active"] else None, state.get("final_judgment", "Interview Active"), gr.update(value=None), metrics

with gr.Blocks() as demo:
    gr.Markdown("# AI Interview Trainer")
    state = gr.State()

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Setup")
            groq_key = gr.Textbox(label="Groq API Key (Logic & STT)", type="password")
            assembly_key = gr.Textbox(label="AssemblyAI Key (Voice)", type="password")
            job_role = gr.Textbox(label="Target Job Role", value="Software Engineer")
            exp_level = gr.Dropdown(["Junior", "Mid-Level", "Senior"], label="Experience Level", value="Junior")
            start_btn = gr.Button("Start Interview", variant="primary")
            status_text = gr.Textbox(label="Status", interactive=False)
            metrics_display = gr.JSON(label="Real-Time Analytics")

        with gr.Column(scale=2):
            gr.Markdown("### 2. Interview")
            chatbot = gr.Chatbot(label="Interview Chat")
            audio_out = gr.Audio(label="Interviewer Voice", autoplay=True)
            audio_in = gr.Audio(label="Your Answer", sources=["microphone"], type="filepath")
            submit_btn = gr.Button("Submit Answer")

    start_btn.click(fn=start_interview, inputs=[job_role, exp_level, groq_key, assembly_key], outputs=[chatbot, state, audio_out, status_text, audio_in, metrics_display])
    submit_btn.click(fn=process_turn, inputs=[audio_in, state, groq_key, assembly_key], outputs=[chatbot, state, audio_out, status_text, audio_in, metrics_display])

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
