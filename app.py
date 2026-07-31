# python -m streamlit run app.py
import streamlit as st
import edge_tts
import asyncio
import io

st.title("Text to Speech")

text = st.text_area("Enter text to convert to speech:")
lang = st.selectbox("Select language:", ["English", "Arabic"])

VOICES = {
    "Arabic": {
        
        " زارية (امرأة - السعودية)": "ar-SA-ZariyahNeural",
        " شاكر (رجل - مصر)":         "ar-EG-ShakirNeural",
        " سلمى (امرأة - مصر)":       "ar-EG-SalmaNeural",
    },
    "English": {
        " Guy (male - USA)":       "en-US-GuyNeural",
        " Jenny (female - USA)":    "en-US-JennyNeural",
        " Ryan (male - UK)":   "en-GB-RyanNeural",
        " Libby (female - UK)": "en-GB-LibbyNeural",
    },
}

sound = st.selectbox("Select sound:",list(VOICES[lang].keys()))
voice = VOICES[lang][sound]
async def generate_audio(text,voice):
    communicate = edge_tts.Communicate(text = text , voice = voice)
    audio_chunks =[]
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks)
if st.button("Convert to Speech"):
    if text:
        audio_bytes= asyncio.run(generate_audio(text, voice))
        st.audio(audio_bytes, format="audio/mp3")

    else:
        st.warning("Please enter your text...")