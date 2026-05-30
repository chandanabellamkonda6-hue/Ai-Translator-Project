# =========================================
# IMPORTS
# =========================================

import streamlit as st
import streamlit.components.v1 as components
from deep_translator import GoogleTranslator
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
import whisper
import os

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
import tempfile
import uuid
import base64
# =========================================
# LOAD WHISPER MODEL
# =========================================

model = whisper.load_model("base")

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Multilingual Voice Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# SESSION STATE
# =========================================

if "history" not in st.session_state:
    st.session_state.history = []

# =========================================
# SIDEBAR MENU
# =========================================

with st.sidebar:

    st.markdown("""
    <h1 style='text-align:center;color:#2563eb;'>
    ☰ MENU
    </h1>
    """, unsafe_allow_html=True)

    st.divider()

    # =========================================
    # THEME SETTINGS
    # =========================================

    st.subheader("🎨 Theme Settings")

    theme = st.radio(
        "",
        ["Dark", "Light", "System Theme"]
    )

    st.divider()

    # =========================================
    # TRANSLATION HISTORY
    # =========================================

    st.subheader("📜 Translation History")

    if len(st.session_state.history) == 0:

        st.info("No history available")

    else:

        for item in reversed(st.session_state.history):

            st.markdown(f"""
            <div style="
                background:#172554;
                padding:15px;
                border-radius:12px;
                margin-bottom:12px;
                color:white;
            ">

            🕒 <b>{item['Time']}</b><br><br>

            🌐 <b>{item['Input Language']}</b>
            ➜
            <b>{item['Output Language']}</b><br><br>

            📝 <b>Input:</b><br>
            {item['Input Text']}<br><br>

            🔊 <b>Output:</b><br>
            {item['Translated Text']}

            </div>
            """, unsafe_allow_html=True)

    st.divider()

    if st.button("🗑 Clear History"):

        st.session_state.history = []

        st.rerun()

# =========================================
# THEME COLORS
# =========================================

if theme == "Dark":

    bg_color = "#020617"
    text_color = "white"
    box_color = "#172554"

elif theme == "Light":

    bg_color = "#ffffff"
    text_color = "black"
    box_color = "#dbeafe"

else:

    bg_color = "#0f172a"
    text_color = "white"
    box_color = "#1e293b"

# =========================================
# CSS
# =========================================

st.markdown(f"""
<style>

.stApp{{
    background:{bg_color};
    color:{text_color};
}}

header{{
    background:transparent;
}}

footer{{
    visibility:hidden;
}}

.title{{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:{text_color};
    margin-bottom:30px;
}}

.result-box{{
    background:{box_color};
    padding:25px;
    border-radius:15px;
    margin-top:20px;
    color:{text_color};
    font-size:24px;
}}

textarea{{
    font-size:24px !important;
    color:{text_color} !important;
}}

div.stButton > button:first-child {{

    background: linear-gradient(90deg,#14b8a6,#2563eb);

    color:white;

    border:none;

    border-radius:20px;

    width:100%;

    height:70px;

    font-size:22px;

    font-weight:bold;

    box-shadow:0px 0px 20px rgba(37,99,235,0.5);

    transition:0.3s;
}}

div.stButton > button:first-child:hover {{

    transform:scale(1.03);

    background:linear-gradient(90deg,#2563eb,#14b8a6);
}}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================

st.markdown(f"""
<div class="title">
🌍 AI MULTILINGUAL VOICE TRANSLATOR
</div>
""", unsafe_allow_html=True)

# =========================================
# LANGUAGES
# =========================================

languages = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur",
    "Bengali": "bn"
}

# =========================================
# TOP CONTROLS
# =========================================

top1, top2 = st.columns(2)

with top1:

    input_language = st.selectbox(
        "🎤 Input Language",
        list(languages.keys())
    )

with top2:

    output_language = st.selectbox(
        "🔊 Output Language",
        list(languages.keys())
    )

# =========================================
# INPUT TEXT
# =========================================

st.markdown("### ⌨ Type Your Words")

typed_text = st.text_area(
    "",
    height=180,
    label_visibility="collapsed"
)

translate_clicked = st.button("🌐 Translate")

# =========================================
# LANGUAGE CODES
# =========================================

input_lang_code = languages[input_language]
output_lang_code = languages[output_language]

# =========================================
# CUSTOM AUDIO PLAYER
# =========================================

def autoplay_audio(file_path, auto_play=True):

    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    b64 = base64.b64encode(audio_bytes).decode()

    audio_id = str(uuid.uuid4())

    autoplay_script = ""

    if auto_play:

        autoplay_script = f"""
        <script>
            var audio=document.getElementById('{audio_id}');
            audio.play().catch(e=>console.log(e));
        </script>
        """

    custom_audio = f"""
    <div style="
        width:120px;
        height:60px;
        background:#0f2a5f;
        border-radius:40px;
        display:flex;
        align-items:center;
        justify-content:center;
        margin-top:10px;
        box-shadow:0 0 15px rgba(37,99,235,0.3);
    ">

        <audio id="{audio_id}">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>

        <button onclick="
            var audio=document.getElementById('{audio_id}');
            audio.play();
        "
        style="
            background:none;
            border:none;
            cursor:pointer;
            font-size:34px;
            color:white;
        ">
            🔊
        </button>

    </div>

    {autoplay_script}
    """

    components.html(custom_audio, height=80)

# =========================================
# ONLINE VOICE TRANSLATION
# =========================================

st.markdown("## 🎤 Speak & Translate")

audio_bytes = audio_recorder(
    text="",
    recording_color="#ff4b4b",
    neutral_color="#2563eb",
    icon_name="microphone",
    icon_size="3x",
    pause_threshold=3.0,
    sample_rate=44100
)

if audio_bytes:

    st.success("✅ Audio Recorded")

    st.audio(audio_bytes, format="audio/wav")

    try:

        # SAVE AUDIO

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:

            tmp_file.write(audio_bytes)

            temp_audio_path = tmp_file.name

        # WHISPER SPEECH TO TEXT

        result = model.transcribe(temp_audio_path)

        recognized_text = result["text"]

        # SHOW RECOGNIZED TEXT

        st.markdown(f"""
        <div class="result-box">
        📝 <b>Recognized Speech:</b><br><br>
        {recognized_text}
        </div>
        """, unsafe_allow_html=True)

        # TRANSLATE

        translated_text = GoogleTranslator(
            source='auto',
            target=output_lang_code
        ).translate(recognized_text)

        # SHOW TRANSLATED TEXT

        st.markdown(f"""
        <div class="result-box">
        🌍 <b>Translated Output:</b><br><br>
        {translated_text}
        </div>
        """, unsafe_allow_html=True)

        # AUDIO OUTPUT

        output_audio_file = f"{uuid.uuid4()}_output.mp3"

        output_tts = gTTS(
            text=translated_text,
            lang=output_lang_code
        )

        output_tts.save(output_audio_file)

        autoplay_audio(output_audio_file, auto_play=True)

        # SAVE HISTORY

        st.session_state.history.append({

            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Input Language": input_language,

            "Output Language": output_language,

            "Input Text": recognized_text,

            "Translated Text": translated_text
        })

    except Exception as e:

        st.error(f"❌ Voice Translation Error: {e}")

# =========================================
# TEXT TRANSLATION
# =========================================

if translate_clicked:

    try:

        if typed_text.strip() == "":

            st.warning("Please enter text")

        else:

            translated_text = GoogleTranslator(
                source='auto',
                target=output_lang_code
            ).translate(typed_text)

            st.markdown(f"""
            <div class="result-box">
            📝 <b>Input Text:</b><br><br>
            {typed_text}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-box">
            🌍 <b>Translated Output:</b><br><br>
            {translated_text}
            </div>
            """, unsafe_allow_html=True)

            output_audio_file = f"{uuid.uuid4()}_output.mp3"

            output_tts = gTTS(
                text=translated_text,
                lang=output_lang_code
            )

            output_tts.save(output_audio_file)

            autoplay_audio(output_audio_file, auto_play=True)

            st.session_state.history.append({

                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "Input Language": input_language,

                "Output Language": output_language,

                "Input Text": typed_text,

                "Translated Text": translated_text
            })

    except Exception as e:

        st.error(f"❌ Error: {e}")