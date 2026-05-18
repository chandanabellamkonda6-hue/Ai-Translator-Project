
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import threading
import os

# =========================================
# INITIALIZE
# =========================================

pygame.mixer.init()
recognizer = sr.Recognizer()

# =========================================
# LANGUAGE DICTIONARY
# =========================================

languages = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Russian": "ru",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Turkish": "tr",
    "Urdu": "ur",
    "Bengali": "bn"
}

# =========================================
# PLAY INPUT AUDIO
# =========================================


def play_input_audio():

    try:

        pygame.mixer.music.load("input_audio.mp3")

        pygame.mixer.music.play()

    except:

        status_label.config(text="❌ No Input Audio", fg="red")

# =========================================
# PLAY OUTPUT AUDIO
# =========================================


def play_output_audio():

    try:

        pygame.mixer.music.load("output_audio.mp3")

        pygame.mixer.music.play()

    except:

        status_label.config(text="❌ No Output Audio", fg="red")

# =========================================
# MAIN TRANSLATION FUNCTION
# =========================================


def translate_voice():

    try:

        input_text.delete("1.0", tk.END)
        output_text.delete("1.0", tk.END)

        status_label.config(text="🎤 Listening...", fg="lightgreen")

        window.update()

        input_language = input_lang.get()
        output_language = output_lang.get()

        input_code = languages[input_language]
        output_code = languages[output_language]

        # =========================================
        # MICROPHONE INPUT
        # =========================================

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

        # =========================================
        # SPEECH TO TEXT
        # =========================================

        text = recognizer.recognize_google(
            audio,
            language=input_code
        )

        # =========================================
        # INPUT TEXT LIVE DISPLAY
        # =========================================

        for char in text:

            input_text.insert(tk.END, char)

            input_text.update()

        # =========================================
        # SAVE INPUT AUDIO
        # =========================================

        input_tts = gTTS(
            text=text,
            lang=input_code
        )

        if os.path.exists("input_audio.mp3"):
            os.remove("input_audio.mp3")

        input_tts.save("input_audio.mp3")

        # =========================================
        # TRANSLATE
        # =========================================

        translated = GoogleTranslator(
            source=input_code,
            target=output_code
        ).translate(text)

        # =========================================
        # OUTPUT TEXT LIVE DISPLAY
        # =========================================

        for char in translated:

            output_text.insert(tk.END, char)

            output_text.update()

        # =========================================
        # SAVE OUTPUT AUDIO
        # =========================================

        output_tts = gTTS(
            text=translated,
            lang=output_code
        )

        if os.path.exists("output_audio.mp3"):
            os.remove("output_audio.mp3")

        output_tts.save("output_audio.mp3")

        # =========================================
        # PLAY OUTPUT AUDIO AUTOMATICALLY
        # =========================================

        pygame.mixer.music.load("output_audio.mp3")

        pygame.mixer.music.play()

        # =========================================
        # HISTORY
        # =========================================

        history_box.insert(
            tk.END,
            f"INPUT: {text}\nOUTPUT: {translated}\n\n"
        )

        status_label.config(
            text="✅ Translation Complete",
            fg="lightgreen"
        )

    except Exception as e:

        status_label.config(
            text=f"❌ Error: {e}",
            fg="red"
        )

# =========================================
# THREADING
# =========================================


def start_translation():

    thread = threading.Thread(target=translate_voice)

    thread.start()

# =========================================
# MAIN WINDOW
# =========================================

window = tk.Tk()

window.title("🌍 AI Multilingual Voice Translator")

window.geometry("1100x900")

window.configure(bg="#15152e")

# =========================================
# TITLE
# =========================================

heading = tk.Label(
    window,
    text="🌍 AI MULTILINGUAL VOICE TRANSLATOR",
    font=("Arial", 28, "bold"),
    bg="#15152e",
    fg="white"
)

heading.pack(pady=20)

# =========================================
# LANGUAGE FRAME
# =========================================

lang_frame = tk.Frame(window, bg="#15152e")

lang_frame.pack(pady=10)

# INPUT LANGUAGE

input_label = tk.Label(
    lang_frame,
    text="Input Language",
    font=("Arial", 16, "bold"),
    bg="#15152e",
    fg="white"
)

input_label.grid(row=0, column=0, padx=30)

input_lang = ttk.Combobox(
    lang_frame,
    values=list(languages.keys()),
    font=("Arial", 13),
    width=20
)

input_lang.grid(row=1, column=0, padx=30)

input_lang.set("English")

# OUTPUT LANGUAGE

output_label = tk.Label(
    lang_frame,
    text="Output Language",
    font=("Arial", 16, "bold"),
    bg="#15152e",
    fg="white"
)

output_label.grid(row=0, column=1, padx=30)

output_lang = ttk.Combobox(
    lang_frame,
    values=list(languages.keys()),
    font=("Arial", 13),
    width=20
)

output_lang.grid(row=1, column=1, padx=30)

output_lang.set("Telugu")

# =========================================
# INPUT TITLE
# =========================================

input_title = tk.Label(
    window,
    text="Recognized Speech",
    font=("Arial", 22, "bold"),
    bg="#15152e",
    fg="white"
)

input_title.pack(pady=10)

# INPUT TEXT BOX

input_text = tk.Text(
    window,
    height=5,
    width=80,
    font=("Arial", 16),
    bg="white",
    fg="black"
)

input_text.pack(pady=10)

# INPUT AUDIO BUTTON

input_audio_button = tk.Button(
    window,
    text="🔊 Play Input Audio",
    font=("Arial", 14, "bold"),
    bg="#0984e3",
    fg="white",
    command=play_input_audio
)

input_audio_button.pack(pady=5)

# =========================================
# OUTPUT TITLE
# =========================================

output_title = tk.Label(
    window,
    text="Translated Output",
    font=("Arial", 22, "bold"),
    bg="#15152e",
    fg="white"
)

output_title.pack(pady=10)

# OUTPUT TEXT BOX

output_text = tk.Text(
    window,
    height=5,
    width=80,
    font=("Arial", 16),
    bg="white",
    fg="black"
)

output_text.pack(pady=10)

# OUTPUT AUDIO BUTTON

output_audio_button = tk.Button(
    window,
    text="🔊 Play Output Audio",
    font=("Arial", 14, "bold"),
    bg="#6c5ce7",
    fg="white",
    command=play_output_audio
)

output_audio_button.pack(pady=5)

# =========================================
# TRANSLATE BUTTON
# =========================================

translate_button = tk.Button(
    window,
    text="🎤 Speak & Translate",
    font=("Arial", 20, "bold"),
    bg="#00c896",
    fg="white",
    padx=25,
    pady=12,
    command=start_translation
)

translate_button.pack(pady=20)

# =========================================
# HISTORY TITLE
# =========================================

history_title = tk.Label(
    window,
    text="Translation History",
    font=("Arial", 20, "bold"),
    bg="#15152e",
    fg="white"
)

history_title.pack(pady=10)

# HISTORY BOX

history_box = tk.Text(
    window,
    height=8,
    width=90,
    font=("Arial", 12),
    bg="#f1f2f6",
    fg="black"
)

history_box.pack(pady=10)

# =========================================
# STATUS LABEL
# =========================================

status_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 16, "bold"),
    bg="#15152e",
    fg="yellow"
)

status_label.pack(pady=10)

# =========================================
# RUN WINDOW
# =========================================

window.mainloop()
