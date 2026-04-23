import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io
import time

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Sweet Talk", page_icon="🧸")

# 디자인 (파스텔 톤 유지)
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
        transition: all 0.1s ease !important;
    }
    .chat-box { 
        background-color: white; 
        padding: 25px; 
        border-radius: 30px; 
        border: 5px solid #AED6F1;
        margin-top: 20px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧸 NATHAN'S SWEET TALK")

# 대화 기록 대신 '현재 대화'만 저장하는 방식으로 변경
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

# 3. 마이크 및 음성 처리
def get_audio_html(audio_bytes, unique_id):
    b64 = base64.b64encode(audio_bytes).decode()
    # 캐시 방지를 위해 랜덤 쿼리 스트링(?t=)을 추가한 데이터 URI 방식
    return f'<audio controls autoplay key="{unique_id}" style="width: 100%; margin-top: 10px;"><source src="data:audio/mp3;base64,{b64}#t={unique_id}" type="audio/mp3"></audio>'

st.info("나단! 하늘색 버튼을 누르고 영어로 말해봐!")

text = speech_to_text(
    language='en',
    start_prompt="🩵 눌러서 말하기 (START)",
    stop_prompt="✅ 다 했어! (번역하기)",
    key='nathan_stt'
)

if text:
    if "last_text" not in st.session_state or st.session_state.last_text != text:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        
        tts = gTTS(text=translated, lang=target_lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # 기존 기록을 덮어쓰고 오직 '현재 대화'만 저장 (ID도 새로 갱신)
        st.session_state.current_chat = {
            "id": str(time.time()), # 문자열 ID로 더 확실하게 구분
            "en": text, 
            "trans": translated, 
            "lang": target_lang_name,
            "audio": audio_buffer.getvalue()
        }
        st.session_state.last_text = text
        st.rerun()

# 4. 결과 출력 (오직 최신 대화 하나만 표시)
if st.session_state.current_chat:
    chat = st.session_state.current_chat
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; margin: 0;'>나단이가 한 말:</p>
            <h3 style='color: #333; margin-top: 5px; font-weight: bold;'>"{chat['en']}"</h3>
            <p style='color: #888; margin-top: 20px; margin-bottom: 0;'>AI 친구의 대답 ({chat['lang']}):</p>
            <h2 style='color: #4A90E2; margin-top: 5px; font-weight: bold;'>{chat['trans']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 고유 ID를 audio 태그에 강제로 심어 브라우저 캐시를 완전히 무시하게 함
    st.markdown(get_audio_html(chat['audio'], chat['id']), unsafe_allow_html=True)