# 💼 Akıllı İK & CV Değerlendirme Asistanı (Smart HR - CV Analyzer)

Bu proje, Microsoft Yaz Staj Programı kapsamında geliştirilmiş yapay zekâ destekli bir İK analiz ve değerlendirme asistanıdır. Büyük Dil Modelleri (LLM) entegrasyonu sayesinde aranan pozisyon gereksinimleri ile aday CV'lerini otomatik olarak karşılaştırır, objektif bir uyum analizi sunar ve adaya özel mülakat soruları üretir.

---

## 🚀 Öne Çıkan Özellikler

* 📄 PDF Metin Çıkarımı: Yüklenen aday CV'lerinden metin verilerini pdfplumber kütüphanesi ile hızlı ve güvenilir şekilde ayıklar.
* 🎯 Dinamik Uyum Analizi: Adayın teknik yetkinliklerini, tecrübelerini ve projelerini pozisyon ilanıyla kıyaslayarak detaylı değerlendirme sunar.
* ✅ Güçlü ve Eksik Yön Analizi: Adayın CV'sindeki öne çıkan güçlü yönleri ve ilanda istenip eksik kalan gelişim alanlarını somut maddeler halinde listeler.
* ❓ Adaya Özel Mülakat Soruları: Adayın CV'sinde belirttiği spesifik projelere ve teknolojilere atıfta bulunan özgün mülakat soruları üretir.

---

## 🛠️ Kullanılan Teknolojiler & Kütüphaneler

* Programlama Dili: Python 3.10+
* Arayüz Frameworkü: Streamlit
* Yapay Zekâ / LLM Entegrasyonu: Google Gemini API (google-genai)
* Veri Ayıklama: pdfplumber

---

## ⚙️ Kurulum ve Çalıştırma

1. Repoyu klonlayın:
   git clone https://github.com/nurgulyildiz34/HR_CV_Analyzer.git
   cd HR_CV_Analyzer

2. Gerekli kütüphaneleri yükleyin:
   pip install streamlit pdfplumber google-genai

3. API Key Yapılandırması:
   .streamlit/secrets.toml dosyasını oluşturun ve Gemini API anahtarınızı ekleyin:
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

4. Uygulamayı çalıştırın:
   streamlit run app.py

   
