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

    .menu-card {
        display: block;
        text-decoration: none;
        background: linear-gradient(135deg, #FFF0F7 0%, #F8EDFF 100%);
        border: 2px solid #F0B8D8;
        border-radius: 24px;
        padding: 1.6rem 1.4rem;
        margin-bottom: 1.2rem;
        text-align: center;
        transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 16px rgba(224,122,155,0.12);
    }

    .menu-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(224,122,155,0.22);
    }

    .menu-card .icon {
        font-size: 2.4rem;
        margin-bottom: 0.4rem;
    }

    .menu-card .label {
        font-size: 1.25rem;
        font-weight: 800;
        color: #C0468A;
        margin-bottom: 0.3rem;
    }

    .menu-card .desc {
        font-size: 0.9rem;
        color: #A06080;
        line-height: 1.7;
    }

    @media (max-width: 480px) {
        .menu-card { padding: 1.3rem 1rem; }
        .menu-card .label { font-size: 1.1rem; }
        .menu-card .desc { font-size: 0.85rem; }
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

# くま診断カード
st.markdown(
    '<a class="menu-card" href="https://kuma-shindan.streamlit.app/" target="_blank">'
    '<div class="icon">👁️</div>'
    '<div class="label">あなたのクマはどのタイプ？</div>'
    '<div class="desc">目の下のクマをAIが分析！<br>タイプ別のケア方法をお伝えします</div>'
    '</a>',
    unsafe_allow_html=True
)

# お顔の変化チェックカード
st.markdown(
    '<a class="menu-card" href="https://beforeafter-shindan.streamlit.app/" target="_blank">'
    '<div class="icon">🌸</div>'
    '<div class="label">お顔の変化check！</div>'
    '<div class="desc">ケア前後の写真を2枚アップするだけ！<br>AIが変化を詳しく診断します</div>'
    '</a>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; color:#ccc; font-size:0.8rem; margin-top:2rem;">'
    '© たるみバスター★きよみ ｜ AIによる参考診断です</p>',
    unsafe_allow_html=True
)
