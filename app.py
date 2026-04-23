import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Poke-Translator", page_icon="⚡")

# 디자인: 포켓몬 도감(Pokedex) 스타일
st.markdown("""
    <style>
    /* 전체 배경: 포켓몬 레드 */
    .stApp { 
        background-color: #CC0000; 
        border: 10px solid #3B4CCA; /* 포켓몬 블루 테두리 */
    }
    
    /* 제목: 포켓몬 폰트 느낌 */
    h1 {
        color: #FFDE00 !important; /* 포켓몬 옐로우 */
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        text-shadow: 3px 3px 0px #3B4CCA;
        -webkit-text-stroke: 1px #3B4CCA;
    }

    /* 몬스터볼 스타일 버튼 */
    .stButton > button {
        width: 100%;
        height: 120px !important;
        background: radial-gradient(circle at center, #ffffff 0%, #ffffff 10%, #ff0000 11%, #ff0000 100%) !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 60px !important;
        border: 8px solid #333 !important;
        box-shadow: 0 10px 0 #888, 0 15px 20px rgba(0,0,0,0.4) !important;
        transition: all 0.1s ease !important;
        text-shadow: 2px 2px 2px #000;
        margin-top: 20px;
    }

    /* 버튼 클릭 시 몬스터볼이 흔들리는 느낌 */
    .stButton > button:active {
        box-shadow: 0 2px 0 #333 !important;
        transform: translateY(8px) rotate(2deg) !important;
    }

    /* 대화창: 도감 화면 느낌 */
    .chat-box { 
        background-color: #DEF3FD; /* 연한 하늘색 화면 */
        padding: 20px; 
        border-radius: 15px; 
        border: 5px solid #333;
        margin-top: 30px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
    }

    /* 사이드바 글자색 */
    .css-17l2qt2 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NATHAN'S POKE-TRANS")

if "history" not in st.session_state:
    st.session_state.history = []

# 2. 언어 선택 (사이드바)
st.sidebar.markdown("<h2 style='color:white;'>🌐 Language</h2>", unsafe_allow_html=True)
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

st.warning("나단! 몬스터볼 버튼을 누르고 영어로 말해봐!")

text = speech_to_text(
    language='en',
    start_prompt="🔴 POKE-BALL START!",
    stop_prompt="⚪ GOTCHA! (번역하기)",
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
            <p style='color: #555; margin: 0; font-weight: bold;'>[나단이의 영어]</p>
            <h3 style='color: #000; margin-top: 5px;'>"{chat['en']}"</h3>
            <p style='color: #555; margin-top: 15px; margin-bottom: 0; font-weight: bold;'>[도감 번역 - {chat['lang']}]</p>
            <h2 style='color: #CC0000; margin-top: 5px;'>{chat['trans']}</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(get_audio_html(chat['audio']), unsafe_allow_html=True)
    st.write("---")