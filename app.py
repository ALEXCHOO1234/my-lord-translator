import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

st.set_page_config(page_title="My Lord Live Translator", page_icon="🎙️")

st.title("🎙️ My Lord Live Translator")

# 세션 상태 초기화 (대화 기록 보관)
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .chat-box { background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.info("My Lord, 아래 마이크 아이콘을 누르고 말씀을 마친 뒤 다시 눌러주세요.")

# 에러를 유발할 수 있는 옵션을 모두 제거한 가장 표준적인 형태입니다.
text = speech_to_text(
    language='en',
    start_prompt="🇬🇧 Click to Speak",
    stop_prompt="🛑 Stop",
    key='STT'
)

if text:
    # 번역 실행
    translated = GoogleTranslator(source='en', target='ko').translate(text)
    # 기록의 맨 위에 추가
    st.session_state.history.insert(0, {"en": text, "ko": translated})

# 대화 기록 표시
st.write("---")
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #666; font-size: 0.8em;'>English</p>
            <p style='font-size: 1.1em; font-weight: bold;'>{chat['en']}</p>
            <p style='color: #666; font-size: 0.8em; margin-top: 10px;'>한국어 해석</p>
            <p style='font-size: 1.2em; color: #4CAF50; font-weight: bold;'>{chat['ko']}</p>
        </div>
    """, unsafe_allow_html=True)