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
    .block-container { max-width: 680px; }
    h1 { color: #9B59B6; text-align: center; }
    .subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
    .result { background: #FDF5FF; border-left: 4px solid #9B59B6;
              padding: 1.2rem; border-radius: 8px; margin-top: 1rem; }
    .cta { background: #FFE4F3; border-radius: 12px; padding: 1.2rem;
           text-align: center; margin-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("kiyomi_character.jpg", width=200)

st.markdown("# 👁️ あなたのクマはどのタイプ？")
st.markdown('<p class="subtitle">写真をアップロードするだけ！AIがくまのタイプと改善アドバイスをお伝えします</p>',
            unsafe_allow_html=True)

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("システムエラーが発生しました。しばらくしてから再度お試しください。")
    st.stop()

st.markdown("### 📸 お顔の写真をアップロード")
st.caption("目の下がよく見える、正面からの写真が最適です")

uploaded = st.file_uploader("写真を選ぶ（JPG・PNG）", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    image = ImageOps.exif_transpose(image)  # スマホ写真の向きを自動補正
    image = image.convert("RGB")            # PNG/HEIC等の形式を統一

    # 大きすぎる画像はリサイズ（API制限対策）
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
                img_base64 = base64.b64encode(buf.getvalue()).decode()

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
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.success("診断が完了しました！")
                st.markdown("---")
                st.markdown("### 🔍 あなたのくま診断結果")
                st.markdown(
                    f'<div class="result">{result.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("""
<div class="cta">
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
st.caption("© 小顔マジシャン認定トレーナー きよみ ｜ AIによる参考診断です")
