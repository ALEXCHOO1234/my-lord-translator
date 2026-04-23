import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

# 1. 앱 설정 및 제목 변경
st.set_page_config(page_title="NATHAN's AI Translator", page_icon="👦")
st.title("👦 NATHAN's AI Translator")

# 대화 기록 유지
if "history" not in st.session_state:
    st.session_state.history = []

# 디자인 개선 (나단이를 위한 밝은 느낌)
st.markdown("""
    <style>
    .stApp { background-color: #f0f8ff; }
    .chat-box { background-color: white; padding: 15px; border-radius: 15px; border-left: 5px solid #FFD700; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stSelectbox label { font-weight: bold; color: #1E90FF; }
    </style>
    """, unsafe_allow_html=True)

# 2. 언어 선택 옵션 추가
st.sidebar.header("🌐 Language Setting")
target_lang = st.sidebar.selectbox(
    "어느 나라 말로 번역할까요?",
    ["한국어", "Japanese", "Chinese", "French", "Spanish", "German"],
    index=0
)

# 선택된 언어 코드 매핑
lang_map = {
    "한국어": "ko",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

st.info(f"Hi Nathan! 영어를 말하면 인공지능이 **{target_lang}**로 바꿔줄 거야.")

# 마이크 로직
text = speech_to_text(
    language='en',
    start_prompt="🎤 Start Speaking (English)",
    stop_prompt="🛑 Stop & Translate",
    key='nathan_stt'
)

if text:
    if "last_text" not in st.session_state or st.session_state.last_text != text:
        # 선택한 언어로 번역 실행
        translated = GoogleTranslator(source='en', target=lang_map[target_lang]).translate(text)
        st.session_state.history.insert(0, {"en": text, "trans": translated, "lang": target_lang})
        st.session_state.last_text = text
        st.rerun()

# 기록 출력
st.write("---")
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; font-size: 0.8em; margin: 0;'>English</p>
            <p style='font-size: 1.1em; font-weight: bold; margin-bottom: 5px;'>{chat['en']}</p>
            <p style='color: #888; font-size: 0.8em; margin: 0;'>{chat['lang']} Translation</p>
            <p style='font-size: 1.2em; color: #1E90FF; font-weight: bold; margin: 0;'>{chat['trans']}</p>
        </div>
    """, unsafe_allow_html=True)