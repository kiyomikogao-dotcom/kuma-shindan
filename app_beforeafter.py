import streamlit as st
from groq import Groq
from PIL import Image, ImageOps
import io
import base64
import os
import re

def load_illust_b64():
    path = os.path.join(os.path.dirname(__file__), "illust_kiyomi.jpg")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

ILLUST_B64 = load_illust_b64()

def load_char_b64():
    path = os.path.join(os.path.dirname(__file__), "kiyomi_character.jpg")
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

CHAR_B64 = load_char_b64()

st.set_page_config(
    page_title="ビフォーアフター変化診断 | きよみの小顔ケア",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'M PLUS Rounded 1c', 'Hiragino Maru Gothic Pro', 'ヒラギノ丸ゴ Pro', sans-serif !important;
    }

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

    /* Streamlit ツールバー・フッターを非表示 */
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .viewerBadge_link__qRIco {display: none !important;}

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

if CHAR_B64:
    st.markdown(
        f'<div style="text-align:center; margin-top:1.2rem; margin-bottom:0.4rem;">'
        f'<img src="data:image/jpeg;base64,{CHAR_B64}" '
        f'style="width:140px; max-width:45%; border-radius:14px;">'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<h2 style="text-align:center; font-family:\'M PLUS Rounded 1c\', sans-serif; font-weight:800; color:#E07A9B; margin-top:0.4rem; margin-bottom:0.3rem; font-size:clamp(1.5rem, 6vw, 2.2rem);">🌸 お顔の変化check！</h2>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align:center; font-size:1.05rem; color:#C05A8A; font-weight:700; margin-bottom:0.5rem;">'
    '自分では気づきにくいお顔の変化を、<br>AIが診断してくれるよ！'
    '</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align:center; color:#aaa; margin-bottom:1.5rem; font-size:0.9rem;">'
    'セルフケア前後の写真を2枚アップロードするだけ✨'
    '</p>',
    unsafe_allow_html=True
)

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("システムエラーが発生しました。しばらくしてから再度お試しください。")
    st.stop()

st.markdown('<p style="font-size:0.95rem; font-weight:700; margin-bottom:0;">📸 写真をアップロード</p>', unsafe_allow_html=True)
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

【出力ルール】各セクションは【】のタイトルをそのまま出力し、その直下に診断内容だけを書いてください。指示文・説明文は出力しないでください。

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
変化の内容には触れず、これからも自分を大切にセルフケアを続けていけるような前向きな一言を伝えてください。
毎回必ず違うパターンで書いてください。以下から毎回ランダムに1つ選んでください：
- 「続けることの大切さ・習慣の力」を伝えるパターン
- 「自分を愛すること・自分が一番の味方」を伝えるパターン
- 「小さな積み重ねがいつか大きな変化になる」という気づきのパターン
- 「あなたが輝くことで周りも明るくなる」という広がりのパターン
- きよみ自身の失敗談や経験を交えた共感パターン
- 「鏡を見るのが楽しみになる」という未来をイメージさせるパターン
- 「今日の自分を褒めてあげて」という自己肯定のパターン
- 「疲れた日こそケアが心のリセットになる」という癒しのパターン
- 「キレイになる過程そのものを楽しんで」というプロセス重視のパターン
- 「あなたのケアは、未来の自分へのプレゼント」というギフトのパターン
- 「何歳からでも変われる、今日が一番若い日」という勇気のパターン
- 「完璧じゃなくていい、続けることが正解」という気楽さのパターン
- 「自分の顔が好きになると、人生が変わる」という自信のパターン
- 「頑張りすぎなくていい、5分のケアで十分」というハードルを下げるパターン
- 「ケアをしている自分を、ちゃんと認めてあげて」という承認のパターン
- 「毎日の積み重ねが、一番高級な美容液より効く」という継続力のパターン
- 「自分のために時間を使うことは、わがままじゃない」という許可のパターン
- 「笑顔が一番の小顔！今日もたくさん笑って」という明るさのパターン
- 「焦らなくていい、あなたのペースで進んでいい」という安心のパターン
- 「セルフケアは自分への愛のことば」という詩的なパターン
- 「きれいになりたいと思う気持ち、それだけで十分すごい」という気持ちを称えるパターン
- 「続けている自分は、もうすでにすごい」という事実を伝えるパターン
- 「今日のケアが、3ヶ月後の自分を作っている」という未来投資のパターン
- 「自分の顔を触ってあげる時間が、心もほぐしてくれる」という心身つながりのパターン
- 「昨日より少しでも自分を大切にできたら、それで100点」という優しい評価のパターン
- 「ケアをしながら、自分と話す時間を大切に」という内省のパターン
- 「変わりたいと思う心が、すでにあなたを動かしている」という行動力を褒めるパターン
- 「鏡の前に立つ勇気、それがすでに第一歩」という勇気を称えるパターン
- 「あなたがキレイになることを、きよみは全力で応援しています」という応援パターン
- 「自分を後回しにしてきたあなたへ、今日からが本番です」という新スタートのパターン
心があたたかくなり、またケアを頑張ろうと思えるメッセージを2〜3文で書いてください。
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
                st.markdown("### 🔍 診断結果")
                st.markdown(
                    f'<div class="result-card">{result.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div style="text-align:center; margin-top:1.5rem;">'
                    f'<img src="data:image/jpeg;base64,{ILLUST_B64}" style="width:120px; border-radius:16px;">'
                    f'</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


st.markdown("---")
st.caption("© たるみバスター★きよみ ｜ AIによる参考診断です")
