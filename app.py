import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Sweet Talk", page_icon="🧸")

# 디자인: 편안하고 부드러운 파스텔 톤
st.markdown("""
    <style>
    /* 전체 배경: 눈이 편안한 부드러운 아이보리/연노랑 */
    .stApp { 
        background-color: #FEFDF5; 
    }
    
    /* 제목: 둥글둥글하고 귀여운 파란색 */
    h1 {
        color: #4A90E2 !important; 
        font-family: 'Arial Rounded MT Bold', sans-serif;
        text-align: center;
        padding-bottom: 20px;
    }

    /* 포근한 솜사탕 느낌의 버튼 */
    .stButton > button {
        width: 100%;
        height: 100px !important;
        /* 몬스터볼 컨셉은 유지하되 색상을 파스텔로 변경 */
        background: radial-gradient(circle at center, #ffffff 0%, #ffffff 15%, #AED6F1 16%, #AED6F1 100%) !important;
        color: #333 !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: 6px solid #fff !important;
        /* 그림자도 연하게 */
        box-shadow: 0 8px 0 #85C1E9, 0 12px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.1s ease !important;
        margin-top: 20px;
    }

    /* 버튼 클릭 효과 */
    .stButton > button:active {
        box-shadow: 0 2px 0 #85C1E9 !important;
        transform: translateY(6px) !important;
    }

    /* 대화창: 구름같이 부드러운 디자인 */
    .chat-box { 
        background-color: white; 
        padding: 20px; 
        border-radius: 25px; 
        border: 4px solid #EAECEE;
        margin-top: 30px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧸 NATHAN'S SWEET TALK")

if "history" not in st.session_state:
    st.session_state.history = []

# 2. 언어 선택 (사이드바)
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

# 3. 마이크 및 음성 재생 함수
def get_audio_html(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio controls autoplay style="width: 100%; margin-top: 10px;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

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
        
        st.session_state.history.insert(0, {
            "en": text, 
            "trans": translated, 
            "lang": target_lang_name,
            "audio": audio_buffer.getvalue()
        })
        st.session_state.last_text = text
        st.rerun()

# 4. 결과 출력
for chat in st.session_state.history:
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; margin: 0; font-weight: normal;'>나단이가 한 말:</p>
            <h3 style='color: #333; margin-top: 5px; font-weight: bold;'>"{chat['en']}"</h3>
            <p style='color: #888; margin-top: 15px; margin-bottom: 0; font-weight: normal;'>AI 친구의 대답 ({chat['lang']}):</p>
            <h2 style='color: #4A90E2; margin-top: 5px; font-weight: bold;'>{chat['trans']}</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(get_audio_html(chat['audio']), unsafe_allow_html=True)
    st.write("---")