import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Talking AI", page_icon="👦")
st.title("👦 NATHAN's Talking AI")

if "history" not in st.session_state:
    st.session_state.history = []

# 디자인 (나단이가 좋아할 노란색 포인트)
st.markdown("""
    <style>
    .stApp { background-color: #f0f8ff; }
    .chat-box { background-color: white; padding: 15px; border-radius: 15px; border-left: 5px solid #FFD700; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 언어 선택
st.sidebar.header("🌐 Language Setting")
target_lang_name = st.sidebar.selectbox(
    "어느 나라 말로 번역할까요?",
    ["한국어", "Japanese", "Chinese", "French", "Spanish", "German"],
    index=0
)

lang_map = {
    "한국어": "ko", "Japanese": "ja", "Chinese": "zh-CN",
    "French": "fr", "Spanish": "es", "German": "de"
}
target_lang = lang_map[target_lang_name]

st.info(f"Hi Nathan! 영어를 말하면 인공지능이 **{target_lang_name}**로 읽어줄 거야!")

# 3. 마이크 입력
text = speech_to_text(
    language='en',
    start_prompt="🎤 Start Speaking (English)",
    stop_prompt="🛑 Stop & Translate",
    key='nathan_stt'
)

if text:
    if "last_text" not in st.session_state or st.session_state.last_text != text:
        # 번역
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        
        # 음성 파일 생성 (메모리에서 바로 생성)
        tts = gTTS(text=translated, lang=target_lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # 기록 저장 (오디오 데이터를 바이트로 저장)
        st.session_state.history.insert(0, {
            "en": text, 
            "trans": translated, 
            "lang": target_lang_name,
            "audio": audio_buffer.getvalue()
        })
        st.session_state.last_text = text
        st.rerun()

# 4. 결과 출력 및 소리바 표시
st.write("---")
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; font-size: 0.8em; margin: 0;'>English</p>
            <p style='font-size: 1.1em; font-weight: bold;'>{chat['en']}</p>
            <p style='color: #888; font-size: 0.8em; margin: 0;'>{chat['lang']} Translation</p>
            <p style='font-size: 1.2em; color: #1E90FF; font-weight: bold;'>{chat['trans']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 이 부분이 소리바를 만드는 핵심 코드입니다!
    st.audio(chat['audio'], format='audio/mp3')
    st.write("") # 간격 띄우기