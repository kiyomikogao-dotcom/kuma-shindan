import streamlit as st
from groq import Groq
from PIL import Image, ImageOps
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
        font-size: 1.1rem !important;
        height: 3.4rem !important;
        letter-spacing: 0.05em;
        width: 100% !important;
    }

    .photo-label {
        text-align: center;
        font-weight: bold;
        font-size: 1rem;
        color: #E07A9B;
        margin-bottom: 0.4rem;
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

    .cta-card {
        background: linear-gradient(135deg, #FFE4F3 0%, #F8EDFF 100%);
        border-radius: 20px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
        line-height: 1.9;
    }

    /* スマホ向け調整 */
    @media (max-width: 640px) {
        .block-container {
            padding: 0.5rem 0.5rem 4rem !important;
        }
        .photo-label {
            font-size: 0.9rem;
        }
        .result-card {
            font-size: 0.9rem;
            padding: 1rem 0.8rem;
            line-height: 1.9;
        }
        div[data-testid="stButton"] > button {
            font-size: 1rem !important;
            height: 3rem !important;
        }
        /* ファイルアップローダーをタップしやすく */
        div[data-testid="stFileUploader"] {
            min-height: 80px;
        }
        div[data-testid="stFileUploader"] label {
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### 🌸 お顔の変化check！")
st.markdown(
    '<p style="text-align:center; color:#888; margin-bottom:1.5rem; font-size:0.95rem;">'
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

st.markdown("#### 📸 写真をアップロード")
st.caption("正面から撮影した、なるべく同じ角度・明るさの写真がより正確に分析できます")

col1, col2 = st.columns(2)

def prepare_image(uploaded_file) -> Image.Image:
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    img.thumbnail((1024, 1024))
    return img

with col1:
    st.markdown('<div class="photo-label">📷 BEFORE（ケア前）</div>', unsafe_allow_html=True)
    before_file = st.file_uploader("BEFORE", type=["jpg", "jpeg", "png"], key="before", label_visibility="collapsed")
    if before_file:
        before_image = prepare_image(before_file)
        st.image(before_image, use_container_width=True)

with col2:
    st.markdown('<div class="photo-label">✨ AFTER（ケア後）</div>', unsafe_allow_html=True)
    after_file = st.file_uploader("AFTER", type=["jpg", "jpeg", "png"], key="after", label_visibility="collapsed")
    if after_file:
        after_image = prepare_image(after_file)
        st.image(after_image, use_container_width=True)

if before_file and after_file:
    st.markdown("---")
    if st.button("✨ 変化を診断する", type="primary", use_container_width=True):
        with st.spinner("AIが2枚の写真を比較分析中です…少々お待ちください🔍"):
            try:
                def encode_image(image: Image.Image) -> str:
                    buf = io.BytesIO()
                    image.save(buf, format="JPEG", quality=85)
                    return base64.b64encode(buf.getvalue()).decode()

                before_b64 = encode_image(before_image)
                after_b64 = encode_image(after_image)

                prompt = """
あなたは美容・小顔ケアの専門家「きよみ」です。すべてです・ます調の温かい口調で話してください。
1枚目がビフォー（ケア前）、2枚目がアフター（ケア後）の写真です。

【重要】まず2枚の写真をしっかり見比べて、実際に見えている具体的な違いを観察してください。
たとえば「右の頬がビフォーよりわずかに上がっている」「輪郭の左側がすっきりしている」など、
写真から実際に読み取れる変化を根拠にして分析してください。
毎回同じ内容にならないよう、この写真だけに当てはまる具体的なコメントをしてください。

口調のポイント：
- 変化が小さくても「この部分がこう変わっていますよ」と具体的に伝えた上で褒める
- 「お顎」は使わず「顎」と書く
- 読んだ人が「続けよう！」と思える前向きな締めにする

---
【✨ 変化スコア】
実際に見えた変化の大きさを10点満点で（例：7.5 / 10）
このスコアにした理由を写真から見えた根拠とともに一言で

【フェイスラインの変化】
ビフォーとアフターで顎まわり・輪郭・たるみが実際にどう変わって見えるか具体的に

【目元・頬の変化】
目の印象・目元・頬の位置が写真でどう違って見えるか具体的に

【ほうれい線・口元の変化】
ほうれい線の深さや口角が2枚でどう違うか具体的に

【全体的な印象の変化】
2枚を並べたときの全体の印象の違いを2〜3文で

【特によく変化した部分】
2枚の中で最も差がはっきり出ているポイントをひとつ具体的に

【顔の歪みチェック】
左右の目の高さ・顎のライン・顔全体の左右バランスを確認してください。
ビフォーとアフターで改善があればそれも伝えてください。
気になる点は「ケアで整えていけますよ！」と前向きに。

【きよみからのひとこと】
この写真の方だけへの言葉として、頑張りをねぎらい継続への励ましを伝えてください
---

※角度や光の差がある場合も、見えている範囲で具体的に分析してください。
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
                                    "image_url": {"url": f"data:image/jpeg;base64,{before_b64}"}
                                },
                                {
                                    "type": "text",
                                    "text": "2枚目：アフター（ケア後）の写真です"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{after_b64}"}
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


st.markdown("---")
st.caption("© たるみバスター★きよみ ｜ AIによる参考診断です")
