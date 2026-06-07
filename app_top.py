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

    /* リンクボタンをカード風に */
    div[data-testid="stLinkButton"] {
        margin-bottom: 1rem;
    }
    div[data-testid="stLinkButton"] a {
        display: block !important;
        background: linear-gradient(135deg, #FFF0F7 0%, #F8EDFF 100%) !important;
        border: 2px solid #F0B8D8 !important;
        border-radius: 24px !important;
        padding: 1.6rem 1.4rem !important;
        text-align: center !important;
        color: #8C1A60 !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        height: auto !important;
        min-height: 90px !important;
        box-shadow: 0 4px 16px rgba(224,122,155,0.12) !important;
        letter-spacing: 0.03em;
        line-height: 1.6 !important;
        white-space: nowrap !important;
    }
    div[data-testid="stLinkButton"] a p,
    div[data-testid="stLinkButton"] a span,
    div[data-testid="stLinkButton"] a * {
        font-size: 1.15rem !important;
        color: #8C1A60 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stLinkButton"] a:hover {
        background: linear-gradient(135deg, #FFE0F0 0%, #F0E0FF 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(224,122,155,0.22) !important;
    }
</style>
""", unsafe_allow_html=True)

# イラスト
if CHAR_B64:
    st.markdown(
        f'<div style="text-align:center; margin-top:1.4rem; margin-bottom:0.6rem;">'
        f'<img src="data:image/jpeg;base64,{CHAR_B64}" '
        f'style="width:120px; max-width:40%; border-radius:16px;">'
        f'</div>',
        unsafe_allow_html=True
    )

# タイトル
st.markdown(
    '<div style="text-align:center; font-weight:900; color:#C0468A; '
    'font-size:clamp(1.4rem, 6vw, 2rem); margin-top:0.2rem; margin-bottom:0.2rem; line-height:1.4;">'
    'たるみバスター★きよみ<br>AIお顔診断</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align:center; color:#B07090; font-size:0.95rem; margin-bottom:1.8rem;">'
    '気になる診断を選んでね✨</p>',
    unsafe_allow_html=True
)

# カードボタン
st.link_button("👁️　あなたのクマはどのタイプ？", "https://kuma-shindan.streamlit.app/", use_container_width=True)
st.link_button("🌸　お顔の変化check！", "https://beforeafter-shindan.streamlit.app/", use_container_width=True)

st.markdown(
    '<p style="text-align:center; color:#888; font-size:0.8rem; margin-top:2rem;">'
    '© たるみバスター★きよみ ｜ AIによる参考診断です</p>',
    unsafe_allow_html=True
)
