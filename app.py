import streamlit as st
import pdfplumber
from google import genai
from google.genai import types
import json
import re

# Sayfa Yapılandırması
st.set_page_config(page_title="Smart HR - CV Analyzer", page_icon="💼", layout="wide")

st.markdown(
    """
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"], .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        color: #0f172a !important;
    }
    .block-container {
        background: transparent !important;
        padding: 1.2rem 1rem 2rem !important;
        max-width: 1400px !important;
    }
    #MainMenu, footer, [data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    .hero-shell {
        margin-bottom: 1.4rem;
    }
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%) !important;
        border-radius: 24px !important;
        padding: 1.6rem 1.8rem !important;
        box-shadow: 0 20px 48px rgba(15, 23, 42, 0.24) !important;
        border: 1px solid rgba(148, 163, 184, 0.16) !important;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: rgba(79, 70, 229, 0.18) !important;
        color: #c7d2fe !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.8rem !important;
    }
    .hero-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.35rem 0 !important;
        line-height: 1.15 !important;
        background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 50%, #38bdf8 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .hero-subtitle {
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        margin: 0 !important;
        max-width: 760px !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea, .stFileUploader > div {
        border-radius: 14px !important;
        border: 1px solid rgba(148, 163, 184, 0.28) !important;
        background: #ffffff !important;
        color: #0f172a !important;
        padding: 0.75rem 0.9rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        padding: 0.9rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.28) !important;
    }
    .result-card {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 22px !important;
        border: 1px solid rgba(148, 163, 184, 0.16) !important;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.06) !important;
        margin-bottom: 1.2rem !important;
    }
    .score-badge {
        background: linear-gradient(135deg, #eff6ff, #dbeafe) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        color: #1e3a8a !important;
        box-shadow: 0 12px 28px rgba(59, 130, 246, 0.12) !important;
        margin-bottom: 1.2rem !important;
    }
    .strength-box {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 14px !important;
        padding: 20px !important;
    }
    .risk-box {
        background: #fef2f2 !important;
        border: 1px solid #fecaca !important;
        border-radius: 14px !important;
        padding: 20px !important;
    }
    .question-card {
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        margin-bottom: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #0f172a !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-card">
            <div class="hero-badge">AI Recruitment Intelligence</div>
            <h1 class="hero-title">Akıllı İK & CV Değerlendirme Asistanı</h1>
            <p class="hero-subtitle">Büyük Dil Modelleri (LLM) ile pozisyon gereksinimleri ve aday CV'sini kıyaslayın.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

# Arayüz
col1, col2 = st.columns([1.15, 0.85], gap="large")

with col1:
    job_description = st.text_area(
        "Aranan Pozisyon Tanımı ve Nitelikler:",
        height=250,
        placeholder="Örn: En az Python, SQL bilen, veri analizi ve yapay zekâ projelerinde tecrübeli aday..."
    )

with col2:
    uploaded_file = st.file_uploader("Adayın CV'sini Yükleyin (PDF)", type=["pdf"])

if st.button("🚀 CV'yi Analiz Et", use_container_width=True):
    if not job_description:
        st.warning("Lütfen pozisyon tanımını giriniz!")
    elif not uploaded_file:
        st.warning("Lütfen bir CV yükleyiniz!")
    else:
        with st.spinner("Yapay zekâ CV'deki projeleri mevcut pozisyonla karşılaştırıyor..."):
            try:
                cv_text = extract_text_from_pdf(uploaded_file)
                cv_text = " ".join(cv_text.split())
                if len(cv_text) > 10000:
                    cv_text = cv_text[:10000]

                if not api_key:
                    st.error("API Key bulunamadı (.streamlit/secrets.toml dosyasını kontrol edin).")
                else:
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
Sen kıdemli bir İnsan Kaynakları (İK) ve Teknik İşe Alım Uzmanısın.
Aşağıda verilen İlan Tanımı ile Adayın CV metnini derinlemesine karşılaştır.

POZİSYON TANIMI:
{job_description}

ADAY CV METNİ:
{cv_text}

SİZDEN BEKLENENLER:
1. `uyum_skoru`: Adayın teknik becerileri, tecrübe seviyesi ve eğitim durumunu ilanla kıyaslayarak 0 ile 100 arasında KADEMELİ ve DİNAMİK bir skor belirle (Örn: 42, 58, 67, 73, 84 gibi). Kesinlikle sadece 0, 5, 85 veya 100 gibi sabit değerler verme.
2. `ozet_degerlendirme`: Adayın CV'sindeki somut tecrübelere değinen 2 cümlelik profesyonel İK özeti yaz.
3. `guclu_yonler`: Adayın CV'sinde BİREBİR YER ALAN gerçek projeler, kullandığı teknolojiler veya öne çıkan yetkinliklerden 3 somut madde yaz.
4. `gelisime_acik_yonler`: İlanda istenip adayın CV'sinde bulunmayan veya eksik görünen 2 somut teknik/tecrübe maddesi yaz.
5. `mulakat_sorulari`: Adayın CV'sinde bahsettiği SPESİFİK BİR PROJEYE VEYA TEKNOLOJİYE doğrudan atıfta bulunan 3 özgün mülakat sorusu hazırla.

ÖNEMLİ METİN KURALI: Döneceğin JSON metnindeki string değerlerin içinde çift tırnak (") kullanma, gerekirse tek tırnak (') kullan.

Yanıtını SADECE geçerli bir JSON olarak ver:
{{
    "uyum_skoru": 45,
    "ozet_degerlendirme": "Adayın CV'sindeki tecrübeler ilanla örtüşmektedir.",
    "guclu_yonler": ["Güçlü yön 1", "Güçlü yön 2", "Güçlü yön 3"],
    "gelisime_acik_yonler": ["Eksik yön 1", "Eksik yön 2"],
    "mulakat_sorulari": ["Soru 1", "Soru 2", "Soru 3"]
}}
"""

                    candidate_models = [
                        'gemini-2.5-flash',
                        'gemini-2.5-pro',
                        'gemini-2.0-flash',
                        'gemini-2.0-flash-lite',
                        'gemini-flash-latest',
                        'gemini-pro-latest'
                    ]

                    raw_response = None
                    last_error = None

                    for model_name in candidate_models:
                        try:
                            raw_response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json",
                                    temperature=0.2,
                                    max_output_tokens=2500
                                )
                            )
                            if raw_response and getattr(raw_response, "text", None):
                                break
                        except Exception as err:
                            last_error = err
                            continue

                    if raw_response and getattr(raw_response, "text", None):
                        clean_json = raw_response.text.strip()
                        
                        # Markdown bloklarını temizle
                        clean_json = re.sub(r'^```json\s*', '', clean_json, flags=re.MULTILINE)
                        clean_json = re.sub(r'^```\s*', '', clean_json, flags=re.MULTILINE)
                        clean_json = re.sub(r'\n```$', '', clean_json, flags=re.MULTILINE)
                        clean_json = clean_json.strip()

                        try:
                            result = json.loads(clean_json)
                        except json.JSONDecodeError:
                            # Eğer model yine de hatalı tırnak kaçırdıysa regex ile süslü parantez arasını zorla al
                            match = re.search(r'\{.*\}', clean_json, re.DOTALL)
                            if match:
                                result = json.loads(match.group(0))
                            else:
                                raise

                        # EKRANA BASMA
                        st.divider()
                        st.subheader("📊 Analiz Raporu")

                        st.markdown('<div class="score-badge">', unsafe_allow_html=True)
                        st.metric(label="Pozisyon Uyum Skoru", value=f"%{result.get('uyum_skoru', 50)}")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.info(f"**Özet:** {result.get('ozet_degerlendirme', '')}")
                        st.markdown('</div>', unsafe_allow_html=True)

                        res_col1, res_col2 = st.columns(2)

                        with res_col1:
                            st.markdown('<div class="strength-box">', unsafe_allow_html=True)
                            st.subheader("✅ Güçlü Yönler / Artılar")
                            for item in result.get('guclu_yonler', []):
                                st.write(f"• {item}")
                            st.markdown('</div>', unsafe_allow_html=True)

                        with res_col2:
                            st.markdown('<div class="risk-box">', unsafe_allow_html=True)
                            st.subheader("⚠️ Eksik / Gelişime Açık Yönler")
                            for item in result.get('gelisime_acik_yonler', []):
                                st.write(f"• {item}")
                            st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.subheader("❓ Adaya Özel Mülakat Soruları")
                        for i, q in enumerate(result.get('mulakat_sorulari', []), 1):
                            st.markdown(f'<div class="question-card"><strong>{i}.</strong> {q}</div>', unsafe_allow_html=True)

                    else:
                        st.error(f"Denenen modellerin hiçbirinden yanıt alınamadı. Son alınan hata: {str(last_error)}")

            except Exception as e:
                st.error(f"Analiz üretilirken genel bir hata oluştu: {str(e)}")