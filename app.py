import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="My Lord's Interpreter", page_icon="🎙️")

st.title("My Lord 전용 실시간 통역기")
st.write("상대방의 영어만 골라내어 번역해 드립니다.")

# 번역기 엔진 준비 (영어를 한국어로)
translator = GoogleTranslator(source='en', target='ko')

# 마이크 버튼 생성
text = speech_to_text(
    language='en', 
    start_prompt="🎤 영어 듣기 시작 (클릭)",
    stop_prompt="⏹️ 중지 (클릭)",
    just_once=False,
    key='speech'
)

# 소리가 인식되었을 때
if text:
    st.write("---")
    st.info(f"🎤 상대방(영어): {text}")
    
    try:
        # 번역 실행
        translation = translator.translate(text)
        
        st.subheader("📢 번역 결과")
        st.success(translation)
        
    except Exception as e:
        st.error("번역 과정에서 오류가 발생했습니다.")