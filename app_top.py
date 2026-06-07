import streamlit as st
import base64
import os

def load_char_b64():
    path = os.path.join(os.path.dirname(__file__), "kiyomi_character.jpg")
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

CHAR_B64 = load_char_b64()

st.set_page_config(
    page_title="たるみバスター★きよみ AIお顔診断",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'M PLUS Rounded 1c', 'Hiragino Maru Gothic Pro', sans-serif !important;
    }

    .block-container {
        max-width: 600px;
        padding: 1rem 1rem 4rem !important;
    }

    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}

    .menu-card {
        display: block;
        text-decoration: none !important;
        background: linear-gradient(135deg, #FFF0F7 0%, #F8EDFF 100%);
        border: 2px solid #F0B8D8;
        border-radius: 24px;
        padding: 1.6rem 1.4rem;
        margin-bottom: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(224,122,155,0.12);
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# イラスト＋タイトル
if CHAR_B64:
    st.markdown(
        f'<div style="text-align:center; margin-top:1.4rem; margin-bottom:0.6rem;">'
        f'<img src="data:image/jpeg;base64,{CHAR_B64}" '
        f'style="width:120px; max-width:40%; border-radius:16px;">'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<h1 style="text-align:center; font-weight:900; color:#C0468A; '
    'font-size:clamp(1.4rem, 6vw, 2rem); margin-top:0.2rem; margin-bottom:0.2rem; line-height:1.4;">'
    'たるみバスター★きよみ<br>AIお顔診断</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align:center; color:#B07090; font-size:0.95rem; margin-bottom:1.8rem;">'
    '気になる診断を選んでね✨</p>',
    unsafe_allow_html=True
)

# カード2枚をまとめて1つのmarkdownで出力
st.markdown(
    '<a class="menu-card" href="https://kuma-shindan.streamlit.app/" target="_blank">'
    '<p style="font-size:2.2rem; margin:0 0 0.3rem;">👁️</p>'
    '<p style="font-size:1.2rem; font-weight:800; color:#C0468A; margin:0 0 0.4rem;">あなたのクマはどのタイプ？</p>'
    '<p style="font-size:0.9rem; color:#A06080; margin:0; line-height:1.7;">目の下のクマをAIが分析！<br>タイプ別のケア方法をお伝えします</p>'
    '</a>'
    '<a class="menu-card" href="https://beforeafter-shindan.streamlit.app/" target="_blank">'
    '<p style="font-size:2.2rem; margin:0 0 0.3rem;">🌸</p>'
    '<p style="font-size:1.2rem; font-weight:800; color:#C0468A; margin:0 0 0.4rem;">お顔の変化check！</p>'
    '<p style="font-size:0.9rem; color:#A06080; margin:0; line-height:1.7;">ケア前後の写真を2枚アップするだけ！<br>AIが変化を詳しく診断します</p>'
    '</a>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; color:#ccc; font-size:0.8rem; margin-top:2rem;">'
    '© たるみバスター★きよみ ｜ AIによる参考診断です</p>',
    unsafe_allow_html=True
)
