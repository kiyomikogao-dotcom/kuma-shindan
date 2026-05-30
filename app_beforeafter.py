import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="ビフォーアフター変化診断 | きよみの小顔ケア",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<style>
    .block-container {
        max-width: 680px;
        padding: 1rem 1rem 4rem !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        height: 3.2rem !important;
        letter-spacing: 0.05em;
    }

    .photo-label {
        text-align: center;
        font-weight: bold;
        font-size: 1rem;
        color: #E07A9B;
        margin-bottom: 0.3rem;
    }

    .result-card {
        background: #FDF5FF;
        border: 2px solid #E0C8F0;
        border-radius: 20px;
        padding: 1.4rem 1.2rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 2.0;
    }

    .score-box {
        background: linear-gradient(135deg, #FFE4F3 0%, #F8EDFF 100%);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.1rem;
    }

    .cta-card {
        background: linear-gradient(135deg, #FFE4F3 0%, #F8EDFF 100%);
        border-radius: 20px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
        line-height: 1.9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🌸 ビフォーアフター変化診断")
st.markdown(
    '<p style="text-align:center; color:#888; margin-bottom:1.5rem;">'
    'セルフケア前後の写真を2枚アップロードするだけ！<br>AIがお顔の変化を詳しく分析します✨'
    '</p>',
    unsafe_allow_html=True
)

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("システムエラーが発生しました。しばらくしてから再度お試しください。")
    st.stop()

st.markdown("### 📸 写真をアップロード")
st.caption("正面から撮影した、なるべく同じ角度・明るさの写真がより正確に分析できます")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="photo-label">ビフォー（ケア前）</div>', unsafe_allow_html=True)
    before_file = st.file_uploader("ビフォー写真", type=["jpg", "jpeg", "png"], key="before", label_visibility="collapsed")
    if before_file:
        before_image = Image.open(before_file)
        st.image(before_image, use_container_width=True)

with col2:
    st.markdown('<div class="photo-label">アフター（ケア後）</div>', unsafe_allow_html=True)
    after_file = st.file_uploader("アフター写真", type=["jpg", "jpeg", "png"], key="after", label_visibility="collapsed")
    if after_file:
        after_image = Image.open(after_file)
        st.image(after_image, use_container_width=True)

if before_file and after_file:
    st.markdown("---")
    if st.button("✨ 変化を診断する", type="primary", use_container_width=True):
        with st.spinner("AIが2枚の写真を比較分析中です…少々お待ちください🔍"):
            try:
                def encode_image(image: Image.Image) -> str:
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    return base64.b64encode(buf.getvalue()).decode()

                before_b64 = encode_image(before_image)
                after_b64 = encode_image(after_image)

                prompt = """
あなたは美容・小顔ケアの専門家です。
1枚目がビフォー（ケア前）、2枚目がアフター（ケア後）の写真です。
この2枚を比較して、お顔がどれくらいどのように変化したかを、以下の形式で日本語で分析してください。

---
【変化スコア】
10点満点で変化の度合いを数字で評価（例：7.5 / 10）
スコアの理由を一言で

【フェイスラインの変化】
顎まわり・輪郭のシャープさ・たるみの改善など

【目元・頬の変化】
目の大きさの印象・目元のたるみ・頬のリフトアップ感など

【ほうれい線・口元の変化】
ほうれい線の薄さ・口角の上がり方など

【全体的な印象の変化】
顔全体のバランス・明るさ・若々しさの変化を2〜3文で

【特によく変化した部分】
最も効果が出ているポイントを具体的に

【きよみからのひとこと】
頑張りをねぎらいつつ、さらなるアドバイスを温かく伝えてください
---

※写真の角度や光の違いがある場合も、見えている範囲で最善の分析をしてください。
"""

                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "1枚目：ビフォー（ケア前）の写真です"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{before_b64}"}
                                },
                                {
                                    "type": "text",
                                    "text": "2枚目：アフター（ケア後）の写真です"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{after_b64}"}
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

                st.success("分析が完了しました！")
                st.markdown("---")
                st.markdown("### 🔍 あなたのビフォーアフター診断結果")
                st.markdown(
                    f'<div class="result-card">{result.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )


            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

elif before_file and not after_file:
    st.info("👆 アフター（ケア後）の写真もアップロードしてください")
elif after_file and not before_file:
    st.info("👆 ビフォー（ケア前）の写真もアップロードしてください")
else:
    st.info("👆 ビフォー・アフター2枚の写真をアップロードしてください")

st.markdown("---")
st.caption("© 小顔マジシャン認定トレーナー きよみ ｜ AIによる参考診断です")
