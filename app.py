import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

st.set_page_config(page_title="My Lord Real-time", page_icon="⚡")
st.title("⚡ My Lord Real-time Translator")

if "history" not in st.session_state:
    st.session_state.history = []

st.info("한 번만 [Start]를 누르세요. 말을 멈추면 자동으로 번역됩니다.")

# 'just_once=False'와 'key'를 조합하여 연속 인식이 가능하게 설정합니다.
text = speech_to_text(
    language='en',
    start_prompt="🎙️ 실시간 통역 시작 (Start)",
    stop_prompt="🛑 완전히 종료 (Stop)",
    just_once=False,  # <--- 이 부분이 핵심입니다!
    key='realtime_stt'
)

if text:
    translated = GoogleTranslator(source='en', target='ko').translate(text)
    st.session_state.history.insert(0, {"en": text, "ko": translated})

for chat in st.session_state.history:
    st.write(f"**🇬🇧 English:** {chat['en']}")
    st.write(f"**🇰🇷 번역:** {chat['ko']}")
    st.write("---")