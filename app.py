import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Sweet Talk", page_icon="🧸")

# 디자인 (파스텔 톤)
st.markdown("""
    <style>
    .stApp { background-color: #FEFDF5; }
    h1 {
        color: #4A90E2 !important; 
        font-family: 'Arial Rounded MT Bold', sans-serif;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        height: 100px !important;
        background: radial-gradient(circle at center, #ffffff 0%, #ffffff 15%, #AED6F1 16%, #AED6F1 100%) !important;
        color: #333 !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: 6px solid #fff !important;
        box-shadow: 0 8px 0 #85C1E9, 0 12px 15px rgba(0,0,0,0.1) !important;
    }
    .chat-box { 
        background-color: white; 
        padding: 25px; 
        border-radius: 30px; 
        border: 5px solid #AED6F1;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧸 NATHAN'S SWEET TALK")

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# 2. 언어 선택
st.sidebar.markdown("## 🌐 Language", unsafe_allow_html=True)
target_lang_name = st.sidebar.selectbox(
    "어느 나라 말로 번역할까?",
    ["한국어", "Japanese", "Chinese", "French", "Spanish", "German"]
)

lang_map = {
    "한국어": "ko", "Japanese": "ja", "Chinese": "zh-CN",
    "French": "fr", "Spanish": "es", "German": "de"
}
target_lang = lang_map[target_lang_name]

st.info("나단! 하늘색 버튼을 누르고 영어로 말해봐!")

# 3. 마이크 입력
text = speech_to_text(
    language='en',
    start_prompt="🩵 눌러서 말하기 (START)",
    stop_prompt="✅ 다 했어! (번역하기)",
    key='nathan_stt'
)

if text:
    if "last_text" not in st.session_state or st.session_state.last_text != text:
        # 번역 실행
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        
        # 음성 생성 (가장 빠른 메모리 버퍼 방식)
        tts = gTTS(text=translated, lang=target_lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        st.session_state.current_chat = {
            "en": text, 
            "trans": translated, 
            "lang": target_lang_name,
            "audio": audio_buffer.getvalue()
        }
        st.session_state.last_text = text
        st.rerun()

# 4. 결과 출력
if st.session_state.current_chat:
    chat = st.session_state.current_chat
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; margin: 0;'>나단이가 한 말:</p>
            <h3 style='color: #333; margin-top: 5px;'>"{chat['en']}"</h3>
            <p style='color: #888; margin-top: 20px; margin-bottom: 0;'>AI 친구의 대답 ({chat['lang']}):</p>
            <h2 style='color: #4A90E2; margin-top: 5px;'>{chat['trans']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 무한 로딩을 방지하기 위해 st.audio의 표준 기능을 사용합니다.
    # autoplay=True를 설정하여 번역 즉시 소리가 나게 합니다.
    st.audio(chat['audio'], format='audio/mp3', autoplay=True)