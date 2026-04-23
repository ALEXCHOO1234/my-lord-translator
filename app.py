import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

# 앱 설정
st.set_page_config(page_title="My Lord Translator", page_icon="🎙️")
st.title("🎙️ My Lord Translator")

# 대화 기록 유지
if "history" not in st.session_state:
    st.session_state.history = []

# 디자인 개선
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .chat-box { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.info("My Lord, [Start]를 누르고 말씀을 마친 뒤 [Stop]을 누르시면 즉시 번역됩니다.")

# 가장 안정적인 기본형 마이크 로직
text = speech_to_text(
    language='en',
    start_prompt="🎤 영어 듣기 시작 (Start)",
    stop_prompt="🛑 번역하기 (Stop)",
    key='stable_stt'
)

# 텍스트가 들어오면 즉시 번역 처리
if text:
    translated = GoogleTranslator(source='en', target='ko').translate(text)
    # 최신 대화가 맨 위로 오도록 저장
    st.session_state.history.insert(0, {"en": text, "ko": translated})
    # 화면 즉시 갱신
    st.rerun()

# 기록 출력
st.write("---")
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; font-size: 0.8em; margin: 0;'>English</p>
            <p style='font-size: 1.1em; font-weight: bold; margin-bottom: 5px;'>{chat['en']}</p>
            <p style='color: #888; font-size: 0.8em; margin: 0;'>한국어 해석</p>
            <p style='font-size: 1.2em; color: #4CAF50; font-weight: bold; margin: 0;'>{chat['ko']}</p>
        </div>
    """, unsafe_allow_html=True)