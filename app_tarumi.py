import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="目のたるみ診断 | きよみの小顔ケア",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>
    .block-container { max-width: 680px; }
    h1 { color: #E07A9B; text-align: center; }
    .subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
    .result { background: #FFF5F9; border-left: 4px solid #E07A9B;
              padding: 1.2rem; border-radius: 8px; margin-top: 1rem; }
    .cta { background: #FFE4F3; border-radius: 12px; padding: 1.2rem;
           text-align: center; margin-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ✨ 目のたるみ診断")
st.markdown('<p class="subtitle">写真をアップロードするだけ！AIが目のたるみのタイプと改善アドバイスをお伝えします</p>',
            unsafe_allow_html=True)

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("システムエラーが発生しました。しばらくしてから再度お試しください。")
    st.stop()

st.markdown("### 📸 お顔の写真をアップロード")
st.caption("目元がよく見える、正面からの写真が最適です（明るい場所で撮影するとより正確に診断できます）")

uploaded = st.file_uploader("写真を選ぶ（JPG・PNG）", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, use_container_width=True)

    if st.button("✨ たるみを診断する", type="primary", use_container_width=True):
        with st.spinner("AIが分析中です…少々お待ちください"):
            try:
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                img_base64 = base64.b64encode(buf.getvalue()).decode()

                prompt = """
あなたは美容・スキンケアの専門家です。
この写真から目元のたるみを分析し、以下の形式で日本語で答えてください。

---
【たるみのタイプ】
上まぶたのたるみ・下まぶたのたるみ・目尻のたるみ・全体的なたるみ のうち最も当てはまるものを1〜2つ

【重症度】
軽度 / 中度 / 重度

【たるみの特徴と原因】
2〜3文で分かりやすく説明（筋肉の衰え・むくみ・皮膚の弾力低下など）

【今日からできるセルフケア】
タイプに合った具体的なケアを箇条書き3〜4つ（顔筋トレ・マッサージ・生活習慣など）

【きよみからのひとこと】
温かく励ましながら、プロのアドバイスを添えてください
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
                                        "url": f"data:image/png;base64,{img_base64}"
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
                st.markdown("### 🔍 あなたのたるみ診断結果")
                st.markdown(
                    f'<div class="result">{result.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("""
<div class="cta">
    💗 <strong>もっと詳しくケアを学びたい方へ</strong><br><br>
    小顔トレーナー「<strong>たるみバスター★きよみ</strong>」の<br>
    <strong>オンライン体験会</strong>で、<br>
    あなたのたるみに合ったセルフケアをマンツーマンでお伝えします✨<br><br>
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
