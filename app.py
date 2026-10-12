import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from google import genai

# Sayfa Ayarları
st.set_page_config(page_title="Apex Engine", page_icon="📈", layout="centered")

# API Anahtarın
GEMINI_API_KEY = "AQ.Ab8RN6K35qo-6ev0-e0OQGOt5AgOIUoswAlG1iP_afW17p1m8A"

# 🎨 Yüklediğin Özel APEX.AI Logosu
LOGO_HTML = """
<div style="text-align: center; margin-bottom: 15px;">
    <div style="display: inline-block; padding: 10px; border-radius: 16px; background: #0b132b; border: 1px solid #1e293b; box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);">
        <svg width="120" height="90" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="blue_grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00a8ff" />
                    <stop offset="100%" stop-color="#004080" />
                </linearGradient>
                <linearGradient id="cyan_grad" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#00f2fe" />
                    <stop offset="100%" stop-color="#4facfe" />
                </linearGradient>
            </defs>
            <rect width="400" height="300" fill="#070d19" rx="20"/>
            <path d="M 120 220 L 195 70 L 230 70 L 175 220 Z" fill="url(#blue_grad)" />
            <path d="M 205 70 L 255 220 L 225 220 L 190 115 Z" fill="#005599" />
            <path d="M 140 220 L 190 140 L 220 170 L 275 80 L 240 80 L 275 80 L 275 115" 
                  fill="none" stroke="url(#cyan_grad)" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" />
            <text x="200" y="270" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-weight="800" font-size="36" fill="#ffffff" text-anchor="middle" letter-spacing="3">APEX.AI</text>
        </svg>
    </div>
</div>
"""

def dinamik_ai_yorum_uret(hisse_kodu, tablo_str, degisim_orani):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        calisan_model = None
        try:
            model_listesi = client.models.list()
            for m in model_listesi:
                if "flash" in m.name and "generateContent" in getattr(m, 'supported_generation_methods', []):
                    calisan_model = m.name
                    break
        except Exception:
            pass

        if not calisan_model:
            calisan_model = 'gemini-1.5-flash'

        prompt = f"""
        Sen 'Apex AI' adında profesyonel bir FinTek yapay zekâ asistanısın.
        Aşağıda Borsa İstanbul'da işlem gören {hisse_kodu} hissesinin son 1 haftalık kapanış verileri ve toplam değişimi yer alıyor:
        
        {tablo_str}
        
        Son 1 haftalık toplam değişim: %{degisim_orani:.2f}
        
        Lütfen bu verileri incele ve yatırımcıya yönelik 3-4 cümlelik kısa, net ve profesyonel bir haftalık değerlendirme yap. 
        Fiyat trendini (yükseliş/düşüş/yatay seyir) vurgula. Yatırım tavsiyesi vermeden objektif bir analiz sun.
        """
        
        response = client.models.generate_content(
            model=calisan_model,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Yorumu üretilirken geçici bir API hatası oluştu: {str(e)}"

def teknik_analiz_uret(df, haftalik_degisim):
    son_fiyat = df['Close'].iloc[-1]
    sma_5 = df['Close'].rolling(window=5).mean().iloc[-1]
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=5).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=5).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs.iloc[-1])) if loss.iloc[-1] != 0 else 50

    trend = "yükseliş" if haftalik_degisim > 0 else "düşüş"
    ortak_durum = "üzerinde" if son_fiyat > sma_5 else "altında"
    rsi_yorum = "Aşırı alım bölgesinde (Doygunluk olabilir)" if rsi > 70 else ("Aşırı satım bölgesinde (Tepki alımı gelebilir)" if rsi < 30 else "Nötr seviyede")

    analiz = f"""
    Hisse son 1 haftada <b>%{haftalik_degisim:.2f}</b> oranında bir <b>{trend}</b> trendi sergiledi.<br>
    • <b>5 Günlük Ortalama:</b> {sma_5:.2f} TL (Fiyat ortalamanın <b>{ortak_durum}</b>)<br>
    • <b>RSI İndikatörü:</b> {rsi:.1f} ({rsi_yorum})
    """
    return analiz

def apex_ai_v2(sorgu):
    if not sorgu:
        return "Lütfen bir hisse kodu veya isim girin."
    
    sorgu_temiz = sorgu.lower().strip()
    
    # Halil Aybars Sorgusu
    if "halil aybars" in sorgu_temiz or "aybars" in sorgu_temiz:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 550px; margin: auto; padding: 25px; border-radius: 15px; background: linear-gradient(135deg, #070d19, #1e293b); color: #ffffff; text-align: center; border: 2px solid #f43f5e; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.2);">
            {LOGO_HTML}
            <h2 style="color: #fda4af; margin-top: 10px; margin-bottom: 12px; font-size: 22px;">👶 Halil Aybars</h2>
            <p style="font-size: 16px; line-height: 1.6; color: #fecdd3; font-weight: bold; margin: 0;">
                Halil aybars dayisinin tatli bebisi ve dayisi onu çok seviyo ❤️
            </p>
        </div>
        """

    # Kurucu Sorgusu
    if "halil" in sorgu_temiz or "kurucu" in sorgu_temiz:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 550px; margin: auto; padding: 20px; border-radius: 12px; background-color: #070d19; color: #ffffff; text-align: center;">
            {LOGO_HTML}
            <h2 style="color: #38bdf8; margin-top: 10px; margin-bottom: 10px;">👤 Halil Alp Benli</h2>
            <p style="font-size: 15px; line-height: 1.6; color: #cdd6f4;">
                Tosçelik Fen Lisesi mezunu, geleceğin startup kurucusu ve mühendisi.
            </p>
        </div>
        """

    # BIST Veri Çekme Motoru
    kod_bist = sorgu.upper().strip() + ".IS"
    hisse = yf.Ticker(kod_bist)
    df = hisse.history(period="10d")
    
    if df.empty or len(df) < 5:
        return f"❌ '{sorgu}' koduna ait yeterli veri bulunamadı. Lütfen BIST kodunu doğru girdiğinizden emin olun (Örn: THYAO, GARAN)."

    df = df.dropna(subset=['Close']).copy()
    df['Günlük Değişim (%)'] = df['Close'].pct_change() * 100
    
    df_son = df.tail(5).copy()
    df_son = df_son.reset_index()
    df_son['Tarih'] = df_son['Date'].dt.strftime('%d.%m.%Y')
    df_son['Kapanış (TL)'] = df_son['Close'].apply(lambda x: f"{x:.2f} ₺")
    
    ilk_fiyat = df_son['Close'].iloc[0]
    son_fiyat = df_son['Close'].iloc[-1]
    haftalik_degisim = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100
    
    def renklendir(val):
        if pd.isna(val) or val == 0:
            return "-"
        renk = "#22c55e" if val > 0 else "#ef4444"
        isaret = "+" if val > 0 else ""
        return f"<b style='color: {renk};'>{isaret}{val:.2f}%</b>"
    
    df_son['Değişim'] = df_son['Günlük Değişim (%)'].apply(renklendir)
    ozet_df = df_son[['Tarih', 'Kapanış (TL)', 'Değişim']]
    html_tablo = ozet_df.to_html(escape=False, index=False, justify='center')
    
    teknik_yorum = teknik_analiz_uret(df, haftalik_degisim)
    tablo_metni = ozet_df.to_string(index=False)
    ai_analizi = dinamik_ai_yorum_uret(sorgu.upper(), tablo_metni, haftalik_degisim)
    
    # Canlı Grafik Çizimi (Plotly)
    fig = px.line(df.tail(10), x=df.tail(10).index, y='Close', 
                  title=f"{sorgu.upper()} Son Dönem Fiyat Grafiği",
                  labels={'x': 'Tarih', 'Close': 'Fiyat (TL)'},
                  template='plotly_dark')
    fig.update_traces(line=dict(color='#00f2fe', width=3))
    fig.update_layout(title_font_color='#38bdf8', plot_bgcolor='#070d19', paper_bgcolor='#070d19')

    st.plotly_chart(fig, use_container_width=True)
    
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 550px; margin: auto; padding: 20px; border-radius: 12px; background-color: #070d19; color: #ffffff; border: 1px solid #1e293b;">
        {LOGO_HTML}
        <h2 style="color: #38bdf8; text-align: center; margin-top: 5px; margin-bottom: 15px;">📊 Apex Engine - {sorgu.upper()} Analizi</h2>
        
        {html_tablo}
        
        <div style="margin-top: 15px; padding: 15px; border-radius: 8px; background-color: #0f172a; border-left: 4px solid #38bdf8;">
            <h4 style="margin: 0 0 8px 0; color: #38bdf8;">📈 Algoritmik Teknik Göstergeler</h4>
            <p style="font-size: 13px; line-height: 1.6; color: #e2e8f0; margin: 0;">{teknik_yorum}</p>
        </div>

        <div style="margin-top: 15px; padding: 15px; border-radius: 8px; background-color: #0f172a; border-left: 4px solid #a855f7;">
            <h4 style="margin: 0 0 8px 0; color: #a855f7;">🤖 AI Finansal Yorumu</h4>
            <p style="font-size: 13px; line-height: 1.5; color: #e2e8f0; margin: 0;">{ai_analizi}</p>
        </div>
    </div>
    <style>
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background-color: #1e293b; padding: 10px; font-size: 14px; color: #cdd6f4; text-align: center; }}
        td {{ padding: 10px; font-size: 13px; border-bottom: 1px solid #1e293b; text-align: center; }}
    </style>
    """

# Streamlit Arayüzü
st.title("Apex Engine - FinTek Analiz Motoru")
sorgu = st.text_input("Arama yapın (Örn: THYAO, Halil Aybars veya GARAN):")

if st.button("Analiz Et"):
    if sorgu:
        sonuc_html = apex_ai_v2(sorgu)
        st.markdown(sonuc_html, unsafe_allow_html=True)
    else:
        st.warning("Lütfen bir hisse kodu veya isim girin.")
