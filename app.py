from __future__ import annotations

import os
from typing import Any

import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Sunny — EMP Teaching Companion",
    page_icon="☀️",
    layout="centered",
)


APP_CSS = """
<style>
    :root {
        --emp-orange: #ef7f1a;
        --emp-navy: #18324a;
        --emp-cream: #fff8ee;
        --emp-gold: #f6c453;
    }
    .stApp { background: linear-gradient(180deg, #fffaf3 0%, #ffffff 42%); }
    .sunny-hero {
        padding: 1.25rem 1.4rem;
        border-radius: 20px;
        background: linear-gradient(135deg, var(--emp-navy), #274f70);
        color: white;
        box-shadow: 0 8px 24px rgba(24, 50, 74, .16);
        margin-bottom: 1rem;
    }
    .sunny-hero h1 { margin: 0; font-size: 2rem; }
    .sunny-hero p { margin: .4rem 0 0; opacity: .94; }
    .sunny-note {
        border-left: 5px solid var(--emp-orange);
        background: var(--emp-cream);
        padding: .75rem 1rem;
        border-radius: 8px;
        color: var(--emp-navy);
        margin: .8rem 0 1.2rem;
    }
    .stButton > button[kind="primary"] {
        background: var(--emp-orange);
        border-color: var(--emp-orange);
    }
</style>
"""


SYSTEM_PROMPT = """
You are Sunny, the official AI teaching companion for the Explicit Mathematics
Program (EMP). You support teachers with practical, clear, encouraging guidance.

PERSONALITY AND STYLE
- Be warm, optimistic, witty, plain-spoken and reassuring.
- Use the feel of a gracious country storyteller: concise, human and encouraging.
- You are an entirely original fictional character. Never claim to be Dolly
  Parton, never imitate her, and never quote or reproduce her lyrics, catchphrases,
  or distinctive wording.
- A light country-flavoured expression is fine occasionally, but clarity comes first.
- Use Australian spelling and education terminology.

EMP SUPPORT RULES
- Focus on explicit instruction, worked examples, checking for understanding,
  guided practice, independent practice, fluency and responsive reteaching.
- Distinguish between general teaching suggestions and verified EMP guidance.
- Do not invent EMP lesson numbers, sequences, assessment rules, resource content,
  policies, prices or program claims. If the supplied conversation does not contain
  the necessary EMP information, say so and recommend checking the applicable EMP
  resource or contacting support@empschools.com.
- Never ask for or retain a student's full name, date of birth, contact details,
  health information or other identifying information. If such information appears,
  ask the user to remove it and continue using de-identified details.
- Do not diagnose disabilities or learning disorders.
- Give actionable answers. When useful, structure the response as: what to do,
  example teacher language, and what to check next.
- Keep ordinary answers under 350 words unless the teacher asks for more detail.

The user has selected the EMP level and task type shown in the current message.
Use that context naturally without repeatedly restating it.
"""


VOICE_INSTRUCTIONS = """
Speak as an original, warm and encouraging country educator. Use a gentle,
friendly Southern-inspired lilt, natural pacing, a bright smile in the voice and
light humour. Sound calm, capable and conversational. Do not imitate, evoke, or
sound like any real person or celebrity.
"""


WELCOME = (
    "Hello, lovely! I’m Sunny, your EMP teaching companion. Tell me what’s "
    "happening in the lesson, and we’ll work out a clear next step together."
)

MAX_USER_MESSAGES = 15


def get_secret(name: str, default: str = "") -> str:
    """Read hosted Streamlit secrets first, then local environment variables."""
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = default
    return str(value or os.getenv(name, default))


def initialise_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
    if "audio_by_message" not in st.session_state:
        st.session_state.audio_by_message = {}
    if "user_message_count" not in st.session_state:
        st.session_state.user_message_count = 0


def conversation_for_api(level: str, task_type: str, teacher_context: str) -> list[dict[str, str]]:
    context = (
        f"Current context: EMP level = {level}; request type = {task_type}. "
        f"Optional teacher context = {teacher_context or 'not supplied'}."
    )
    items: list[dict[str, str]] = [{"role": "user", "content": context}]
    for message in st.session_state.messages[-12:]:
        items.append({"role": message["role"], "content": message["content"]})
    return items


def generate_reply(
    api_key: str,
    model: str,
    level: str,
    task_type: str,
    teacher_context: str,
) -> str:
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=conversation_for_api(level, task_type, teacher_context),
    )
    return response.output_text.strip()


def generate_audio(api_key: str, text: str, voice: str) -> bytes:
    client = OpenAI(api_key=api_key)
    response: Any = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text[:4000],
        instructions=VOICE_INSTRUCTIONS,
        response_format="mp3",
    )
    return response.read()


st.markdown(APP_CSS, unsafe_allow_html=True)
initialise_state()

st.markdown(
    """
    <div class="sunny-hero">
        <h1>☀️ Sunny</h1>
        <p>Your warm, practical EMP Teaching Companion</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sunny-note">
      <strong>Original character:</strong> Sunny is inspired by the warmth,
      humour and generosity of country storytelling. She is not Dolly Parton
      and does not imitate Dolly Parton’s identity or distinctive voice.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Set up Sunny")
    api_key = get_secret("OPENAI_API_KEY")
    level = st.selectbox(
        "EMP level",
        ["Level A", "Level B", "Level C", "Level D", "Level E", "General EMP"],
        index=5,
    )
    task_type = st.selectbox(
        "What do you need help with?",
        [
            "Lesson preparation",
            "Explaining a concept",
            "Checking for understanding",
            "Responding to errors",
            "Fluency practice",
            "Assessment and next steps",
            "Communicating with families",
            "General question",
        ],
        index=7,
    )
    teacher_context = st.text_area(
        "Optional class context",
        placeholder="For example: Year 2 class; several students are confusing tens and ones.",
        help="Do not include student names or identifying information.",
    )
    st.divider()
    speak_replies = st.toggle("Read replies aloud", value=True)
    voice = st.selectbox("Sunny’s AI voice", ["coral", "marin", "sage"], index=0)
    model = st.selectbox(
        "Chat model",
        ["gpt-5.6-luna", "gpt-5.6-terra"],
        index=0,
        help="Luna is the economical default; Terra may provide deeper responses.",
    )
    st.caption("🔊 Spoken replies are AI-generated, not a recording of a human.")
    st.warning("Please never enter identifiable or confidential student information.")
    if st.button("Start a new conversation", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        st.session_state.audio_by_message = {}
        st.rerun()

for index, message in enumerate(st.session_state.messages):
    avatar = "☀️" if message["role"] == "assistant" else "👩‍🏫"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            if index in st.session_state.audio_by_message:
                st.audio(st.session_state.audio_by_message[index], format="audio/mp3")
            elif api_key and st.button("🔊 Listen", key=f"listen-{index}"):
                try:
                    with st.spinner("Sunny is getting ready to speak…"):
                        audio = generate_audio(api_key, message["content"], voice)
                    st.session_state.audio_by_message[index] = audio
                    st.rerun()
                except Exception as exc:
                    st.error(f"I couldn’t create the audio: {exc}")

prompt = st.chat_input("Ask Sunny an EMP teaching question…")
if prompt:
    if not api_key:
        st.error("Sunny is not connected yet. Please contact the EMP team.")
        st.stop()

    if st.session_state.user_message_count >= MAX_USER_MESSAGES:
        st.warning(
            "You’ve reached the 15-question limit for this training session. "
            "Please reopen Sunny later if you need to continue testing."
        )
        st.stop()

    prompt = prompt.strip()[:800]
    st.session_state.user_message_count += 1

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👩‍🏫"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="☀️"):
        try:
            with st.spinner("Sunny is thinking it through…"):
                reply = generate_reply(
                    api_key, model, level, task_type, teacher_context
                )
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            if speak_replies:
                with st.spinner("Creating Sunny’s spoken reply…"):
                    audio = generate_audio(api_key, reply, voice)
                message_index = len(st.session_state.messages) - 1
                st.session_state.audio_by_message[message_index] = audio
                st.audio(audio, format="audio/mp3", autoplay=True)
        except Exception as exc:
            st.error(
                "Sunny couldn’t answer just now. Check the API key, account billing "
                f"and model access, then try again. Technical detail: {exc}"
            )

st.caption(
    "Sunny provides teaching support, not official policy or student-specific professional advice. "
    "Check EMP resources when exact program guidance is required."
)
