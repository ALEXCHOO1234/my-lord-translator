import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64

# 1. 앱 설정
st.set_page_config(page_title="NATHAN's Talking AI", page_icon="👦")

# 디자인: 버튼 크기 확대 및 제목 색상 수정
st.markdown("""
    <style>
    .stApp { background-color: #f0f8ff; }
    
    /* 제목 디자인 */
    h1 {
        color: #1E90FF !important;
        font-family: 'Arial Rounded MT Bold', sans-serif;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* 나단이를 위한 큼직한 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        height: 80px !important;
        font-size: 24px !important;
        border-radius: 40px !important;
        border: 5px solid #FFD700 !important;
        background-color: #FF6347 !important; /* 토마토 색상 */
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    /* 결과 박스 */
    .chat-box { 
        background-color: white; 
        padding: 20px; 
        border-radius: 25px; 
        border: 4px solid #1E90FF;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👦 NATHAN's Talking AI")

if "history" not in st.session_state:
    st.session_state.history = []

# 2. 사이드바 설정
st.sidebar.header("🌐 Language Setting")
target_lang_name = st.sidebar.selectbox(
    "어느 나라 말로 번역할까요?",
    ["한국어", "Japanese", "Chinese", "French", "Spanish", "German"]
)

lang_map = {
    "한국어": "ko", "Japanese": "ja", "Chinese": "zh-CN",
    "French": "fr", "Spanish": "es", "German": "de"
}
target_lang = lang_map[target_lang_name]

# 3. 마이크 입력 및 음성 처리
# 오디오 에러 해결을 위한 데이터 변환 함수
def get_audio_html(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio controls autoplay="true" style="width: 100%;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

text = speech_to_text(
    language='en',
    start_prompt="🎤 누르고 말하기 (START)",
    stop_prompt="🛑 다 했어! (STOP)",
    key='nathan_stt'
)

if text:
    if "last_text" not in st.session_state or st.session_state.last_text != text:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        
        # 음성 생성
        tts = gTTS(text=translated, lang=target_lang)
        import io
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # 최신 결과 저장
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
            <p style='color: #888; margin: 0;'>나단이가 한 말:</p>
            <h3 style='color: #333; margin-top: 5px;'>{chat['en']}</h3>
            <p style='color: #888; margin-top: 15px; margin-bottom: 0;'>AI 친구의 대답 ({chat['lang']}):</p>
            <h2 style='color: #1E90FF; margin-top: 5px;'>{chat['trans']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 에러 방지용 HTML5 오디오 태그 직접 삽입
    st.markdown(get_audio_html(chat['audio']), unsafe_allow_html=True)
    st.write("---")