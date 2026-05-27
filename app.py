import streamlit as st
from groq import Groq
from PIL import Image, ImageOps
import io
import base64

st.set_page_config(
    page_title="あなたのクマはどのタイプ？ | きよみの小顔ケア",
    page_icon="👁️",
    layout="centered"
)

st.markdown("""
<style>
    .block-container {
        max-width: 640px;
        padding: 1rem 1rem 4rem !important;
    }

    /* ボタンを丸くして押しやすく */
    div[data-testid="stButton"] > button {
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        height: 3.2rem !important;
        letter-spacing: 0.05em;
    }

    /* 結果カード */
    .result-card {
        background: #FDF5FF;
        border: 2px solid #E0C8F0;
        border-radius: 20px;
        padding: 1.4rem 1.2rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 1.9;
    }

    /* CTAカード */
    .cta-card {
        background: linear-gradient(135deg, #FFE4F3 0%, #F8EDFF 100%);
        border-radius: 20px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
        line-height: 1.9;
    }

    /* スマホ向け調整 */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.4rem 0.4rem 4rem !important;
        }
        .result-card {
            font-size: 0.88rem;
            padding: 1rem 0.9rem;
        }
        .cta-card {
            font-size: 0.92rem;
            padding: 1.2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# キャラクター画像をbase64に変換（HTMLに直接埋め込むため）
def get_img_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

char_b64 = get_img_b64("kiyomi_character.jpg")
hero_img = (
    f'<img src="data:image/jpeg;base64,{char_b64}" '
    'style="width:140px; max-width:45%; border-radius:14px; '
    'display:block; margin:0 auto 0.8rem;">'
    if char_b64 else ""
)

# ヒーローセクション
st.markdown(f"""
<div style="
    background: #FFFFFF;
    border-radius: 24px;
    padding: 1.8rem 1rem 1.4rem;
    text-align: center;
    margin-bottom: 1.6rem;
">
    {hero_img}
    <div style="
        color: #7B2FAB;
        font-size: 1.4rem;
        font-weight: 900;
        margin: 0 0 0.4rem;
        line-height: 1.4;
    ">👁️ あなたのクマはどのタイプ？</div>
    <div style="color: #aaa; font-size: 0.85rem; line-height: 1.7;">
        写真をアップロードするだけ！<br>
        AIがくまのタイプと改善アドバイスをお伝えします
    </div>
</div>
""", unsafe_allow_html=True)

# API接続
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("システムエラーが発生しました。しばらくしてから再度お試しください。")
    st.stop()

# アップロードセクション
st.markdown("### 📸 お顔の写真をアップロード")
st.caption("目の下がよく見える、正面からの写真が最適です")

uploaded = st.file_uploader("写真を選ぶ（JPG・PNG）", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    max_size = 1024
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        image = image.resize(
            (int(image.width * ratio), int(image.height * ratio)),
            Image.LANCZOS
        )

    st.image(image, use_container_width=True)

    if st.button("✨ くまを診断する", type="primary", use_container_width=True):
        with st.spinner("AIが分析中です…少々お待ちください"):
            try:
                buf = io.BytesIO()
                image.save(buf, format="JPEG", quality=85)
                img_b64 = base64.b64encode(buf.getvalue()).decode()

                prompt = """
あなたは美容・スキンケアの専門家です。
この写真から目の下のくまを分析し、以下の形式で日本語で答えてください。

---
【くまのタイプ】
青くま・茶くま・黒くま・混合型 のうち最も当てはまるものを1つ

【重症度】
軽度 / 中度 / 重度

【このくまの特徴と原因】
2〜3文で分かりやすく説明

【今日からできるセルフケア】
タイプに合った具体的なケアを箇条書き3〜4つ

【きよみからのひとこと】
温かく励ましながら、セルフケアへの前向きなアドバイスを添えてください。クリニックや医療機関への案内は不要です。
---

※写真が不鮮明でも、見えている範囲で最善の分析をしてください。
"""

                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                                },
                                {"type": "text", "text": prompt}
                            ]
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.success("診断が完了しました！")
                st.markdown("### 🔍 あなたのくま診断結果")
                st.markdown(
                    f'<div class="result-card">{result.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("""
<div class="cta-card">
    💜 <strong>もっと詳しくケアを学びたい方へ</strong><br><br>
    小顔トレーナー「<strong>たるみバスター★きよみ</strong>」の<br>
    <strong>オンライン体験会</strong>で、<br>
    あなたに合ったセルフケアをマンツーマンでお伝えします✨<br><br>
    👇 お気軽にInstagramからDMください<br>
    <strong>@kiyomi_kogao28</strong>
</div>
""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"エラー: {e}")

else:
    st.info("👆 上のボタンから写真を選んでください")

st.markdown("---")
st.caption("© たるみバスター★きよみ ｜ AIによる参考診断です")
