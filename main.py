import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import time

# =========================================
# LANGUAGE DICTIONARY
# =========================================

languages = {
    "1": ("Telugu", "te"),
    "2": ("Hindi", "hi"),
    "3": ("Tamil", "ta"),
    "4": ("Kannada", "kn"),
    "5": ("Malayalam", "ml"),
    "6": ("English", "en"),
    "7": ("French", "fr"),
    "8": ("Spanish", "es"),
    "9": ("German", "de"),
    "10": ("Japanese", "ja"),
    "11": ("Chinese", "zh-cn"),
    "12": ("Arabic", "ar"),
    "13": ("Russian", "ru"),
    "14": ("Korean", "ko"),
    "15": ("Italian", "it"),
    "16": ("Portuguese", "pt"),
    "17": ("Dutch", "nl"),
    "18": ("Turkish", "tr"),
    "19": ("Urdu", "ur"),
    "20": ("Bengali", "bn")
}

# =========================================
# SHOW LANGUAGES
# =========================================

print("\nAvailable Languages:\n")

for key, value in languages.items():
    print(f"{key}. {value[0]}")

# =========================================
# INPUT LANGUAGE
# =========================================

input_choice = input("\nEnter INPUT language number: ")

if input_choice in languages:

    input_language = languages[input_choice][0]

    input_lang_code = languages[input_choice][1]

    print(f"\nSelected INPUT Language: {input_language}")

else:

    print("Invalid input language")

    input_lang_code = "en"

# =========================================
# OUTPUT LANGUAGE
# =========================================

output_choice = input("\nEnter OUTPUT language number: ")

if output_choice in languages:

    output_language = languages[output_choice][0]

    output_lang_code = languages[output_choice][1]

    print(f"\nSelected OUTPUT Language: {output_language}")

else:

    print("Invalid output language")

    output_lang_code = "te"

# =========================================
# SPEECH RECOGNITION
# =========================================

recognizer = sr.Recognizer()

# =========================================
# MICROPHONE INPUT
# =========================================

with sr.Microphone() as source:

    print("\n🎤 Speak now...")

    recognizer.adjust_for_ambient_noise(source)

    audio = recognizer.listen(source)

# =========================================
# SPEECH TO TEXT
# =========================================

try:

    text = recognizer.recognize_google(
        audio,
        language=input_lang_code
    )

    print("\nYou Said:", text)

    # =========================================
    # TRANSLATE
    # =========================================

    translated_text = GoogleTranslator(
        source=input_lang_code,
        target=output_lang_code
    ).translate(text)

    print("\nTranslated:", translated_text)

    # =========================================
    # TEXT TO SPEECH
    # =========================================

    tts = gTTS(
        text=translated_text,
        lang=output_lang_code
    )

    tts.save("output.mp3")

    print("\n🔊 Playing Audio...")

    # =========================================
    # PLAY AUDIO
    # =========================================

    pygame.mixer.init()

    pygame.mixer.music.load("output.mp3")

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        time.sleep(1)

except Exception as e:

    print("\nError:", e)S