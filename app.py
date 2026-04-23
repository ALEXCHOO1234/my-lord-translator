import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. 앱 설정 (제목 색상 수정을 위해 CSS 강화)
st.set_page_config(page_title="NATHAN's Talking AI", page_icon="👦")

# 디자인 개선 (제목 색상 강제 지정 및 배경 최적화)
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp { background-color: #f0f8ff; }
    
    /* 상단 제목 색상 (진한 파란색으로 고정) */
    h1 {
        color: #1E90FF !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 1px 1px 2px #aaa;
    }
    
    /* 안내 문구 색상 */
    .stAlert p { color: #333 !important; }
    
    /* 결과 박스 디자인 */
    .chat-box { 
        background-color: white; 
        padding: 18px; 
        border-radius: 20px; 
        border-left: 8px solid #FFD700; 
        margin-bottom: 25px; 
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👦 NATHAN's Talking AI")

if "history" not in st.session_state:
    st.session_state.history = []

# 2. 언어 선택 (사이드바)
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
        
        # 음성 파일 생성 (오류 방지를 위해 시점을 명확히 함)
        try:
            tts = gTTS(text=translated, lang=target_lang)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_bytes = audio_buffer.getvalue()
            
            # 기록 저장
            st.session_state.history.insert(0, {
                "en": text, 
                "trans": translated, 
                "lang": target_lang_name,
                "audio": audio_bytes
            })
            st.session_state.last_text = text
            st.rerun()
        except Exception as e:
            st.error("음성을 만드는 중 잠시 문제가 생겼어. 다시 시도해봐!")

# 4. 결과 출력
st.write("---")
for i, chat in enumerate(st.session_state.history):
    st.markdown(f"""
        <div class="chat-box">
            <p style='color: #888; font-size: 0.8em; margin: 0;'>English</p>
            <p style='font-size: 1.2em; font-weight: bold; color: #333;'>{chat['en']}</p>
            <hr style='border: 0.5px solid #eee;'>
            <p style='color: #888; font-size: 0.8em; margin: 0;'>{chat['lang']} Translation</p>
            <p style='font-size: 1.3em; color: #1E90FF; font-weight: bold;'>{chat['trans']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 오디오 플레이어 출력 (오류 방지를 위해 고유 키값 부여)
    st.audio(chat['audio'], format='audio/mp3', start_time=0)
    st.write("\n")