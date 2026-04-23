import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

st.set_page_config(page_title="My Lord Live Translator", page_icon="🎙️")

st.title("🎙️ My Lord Live Translator")
st.subheader("실시간 동시통역 모드")

# 세션 상태 초기화 (대화 기록 저장용)
if "history" not in st.session_state:
    st.session_state.history = []

# 중앙 정렬을 위한 스타일
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; font-weight: bold; }
    .chat-box { background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.info("My Lord, 말씀을 멈추시면 자동으로 번역이 시작됩니다.")

# 실시간 음성 인식 (말을 멈추면 자동으로 결과 반환)
text = speech_to_text(
    language='en', 
    start_prompt="🇬🇧 영어 듣기 시작",
    stop_prompt="🛑 중지",
    just_once=False, # 계속해서 들을 수 있도록 설정
    use_mic_indicator=True,
    key='STT'
)

if text:
    # 영어 -> 한국어 번역
    translated = GoogleTranslator(source='en', target='ko').translate(text)
    
    # 기록 추가
    st.session_state.history.insert(0, {"en": text, "ko": translated})

# 대화 기록 표시
st.write("---")
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #666; font-size: 0.9em; margin-bottom: 5px;'>🇬🇧 English</p>
            <p style='font-size: 1.1em; font-weight: bold;'>{chat['en']}</p>
            <p style='color: #666; font-size: 0.9em; margin-top: 10px; margin-bottom: 5px;'>🇰🇷 한국어 해석</p>
            <p style='font-size: 1.2em; color: #4CAF50; font-weight: bold;'>{chat['ko']}</p>
        </div>
    """, unsafe_allow_html=True)

# 화면 하단 여백
st.write("\n" * 5)