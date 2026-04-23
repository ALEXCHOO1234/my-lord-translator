import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

st.set_page_config(page_title="My Lord Instant", page_icon="⚡")
st.title("⚡ My Lord Instant Translator")

# 대화 내역 저장
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .chat-box { background-color: white; padding: 10px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.info("시작 버튼을 한 번만 누르고 계속 말씀하세요. 말을 멈추면 자동으로 번역됩니다.")

# 실시간 감도와 반응 속도를 높인 설정입니다.
text = speech_to_text(
    language='en',
    start_prompt="🎤 실시간 통역 가동 (Start)",
    stop_prompt="🛑 종료 (Stop)",
    just_once=False, # 한 번 번역 후 꺼지지 않고 계속 대기
    use_mic_indicator=True,
    key='instant_stt'
)

if text:
    # 번역 속도가 가장 빠른 GoogleTranslator 사용
    translated = GoogleTranslator(source='en', target='ko').translate(text)
    # 최신 대화가 위로 오게 저장
    st.session_state.history.insert(0, {"en": text, "ko": translated})
    # 화면 강제 갱신으로 즉시 표시
    st.rerun()

# 기록 표시
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <b>🇬🇧 {chat['en']}</b><br>
            <span style='color: #4CAF50; font-weight: bold;'>🇰🇷 {chat['ko']}</span>
        </div>
    """, unsafe_allow_html=True)