import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Apex Engine", page_icon="📈", layout="centered")

# API Anahtarı
GEMINI_API_KEY = "AQ.Ab8RN6K35qo-6ev0-e0OQGOt5AgOIUoswAlG1iP_afW17p1m8A"

# Özel CSS ile Modern FinTek Teması
st.markdown("""
    <style>
        .main { background-color: #070d19; }
        .stButton>button {
            width: 100%;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
            color: #000000;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Logo Yapısı
LOGO_HTML = """
<div style="text-align: center; margin-bottom: 20px;">
    <div style="display: inline-block; padding: 12px; border-radius: 16px; background: #0b132b; border: 1px solid #1e293b; box-shadow: 0 4px 20px rgba(56, 189, 248, 0.2);">
        <svg width="120" height="80" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
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
            <text x="200" y="270" font-family="'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="36" fill="#ffffff" text-anchor="middle" letter-spacing="3">APEX.AI</text>
        </svg>
    </div>
</div>
"""
st.html(LOGO_HTML)

def dinamik_ai_yorum_uret(hisse_kodu, tablo_str, degisim_orani):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        calisan_model = 'gemini-1.5-flash'
        prompt = f"""
        Sen 'Apex AI' adında profesyonel bir FinTek yapay zekâ asistanısın.
        Aşağıda Borsa İstanbul'da işlem gören {hisse_kodu} hissesinin son 1 haftalık verileri yer alıyor:
        
        {tablo_str}
        
        Son 1 haftalık toplam değişim: %{degisim_orani:.2f}
        Lütfen yatırımcıya yönelik 3-4 cümlelik kısa, net ve şık bir analiz sun. Yatırım tavsiyesi verme.
        """
        response = client.models.generate_content(model=calisan_model, contents=prompt)
        return response.text
    except Exception:
        return "AI Yorumu şu an oluşturulamıyor."

def teknik_analiz_uret(df, haftalik_degisim):
    son_fiyat = df['Close'].iloc[-1]
    sma_5 = df['Close'].rolling(window=5).mean().iloc[-1]
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=5).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=5).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs.iloc[-1])) if loss.iloc[-1] != 0 else 50
    trend = "Yükseliş" if haftalik_degisim > 0 else "Düşüş"
    ortak_durum = "üzerinde" if son_fiyat > sma_5 else "altında"
    rsi_yorum = "Aşırı alım" if rsi > 70 else ("Aşırı satım" if rsi < 30 else "Nötr")

    return f"""
    • **Trend:** Son 1 haftada **%{haftalik_degisim:.2f}** ({trend})  
    • **5 Günlük Ortalama:** {sma_5:.2f} TL (Fiyat ortalamanın **{ortak_durum}**)  
    • **RSI İndikatörü:** {rsi:.1f} — *{rsi_yorum}*
    """

# Kullanıcı Arayüzü
st.title("Apex Engine")
st.caption("Borsa İstanbul Yapay Zekâ Analiz Platformu")

sorgu = st.text_input("Hisse Kodu Girin:", placeholder="Örn: THYAO, ASELS, GARAN")

if st.button("Analiz Et"):
    if not sorgu:
        st.warning("Lütfen bir hisse kodu girin.")
    else:
        sorgu_temiz = sorgu.lower().strip()
        if "halil aybars" in sorgu_temiz:
            st.balloons()
            st.success("👶 Halil Aybars: Dayısının tatlı bebişi ve dayısı onu çok seviyor! ❤️")
        elif "halil" in sorgu_temiz:
            st.info("👤 **Halil Alp Benli**: Tosçelik Fen Lisesi mezunu, geleceğin startup kurucusu ve mühendisi.")
        else:
            kod_bist = sorgu.upper().strip() + ".IS"
            with st.spinner(f"{sorgu.upper()} verileri analiz ediliyor..."):
                hisse = yf.Ticker(kod_bist)
                df = hisse.history(period="10d")
                
                if df.empty or len(df) < 5:
                    st.error(f"❌ '{sorgu}' koduna ait veri bulunamadı. Geçerli bir BIST kodu yazın.")
                else:
                    df = df.dropna(subset=['Close']).copy()
                    df['Günlük Değişim (%)'] = df['Close'].pct_change() * 100
                    df_son = df.tail(5).copy().reset_index()
                    df_son['Tarih'] = df_son['Date'].dt.strftime('%d.%m.%Y')
                    
                    ilk_fiyat = df_son['Close'].iloc[0]
                    son_fiyat = df_son['Close'].iloc[-1]
                    haftalik_degisim = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100

                    col1, col2 = st.columns(2)
                    col1.metric("Son Kapanış", f"{son_fiyat:.2f} TL")
                    col2.metric("Haftalık Değişim", f"%{haftalik_degisim:.2f}", delta=f"{haftalik_degisim:.2f}%")

                    fig = px.line(df.tail(10), x=df.tail(10).index, y='Close', 
                                  title=f"{sorgu.upper()} Canlı Fiyat Grafiği",
                                  template='plotly_dark')
                    fig.update_traces(line=dict(color='#00f2fe', width=3))
                    fig.update_layout(plot_bgcolor='#070d19', paper_bgcolor='#070d19')
                    st.plotly_chart(fig, use_container_width=True)

                    st.subheader("📋 Son 5 Günlük Kapanış Verileri")
                    tablo_df = df_son[['Tarih', 'Close', 'Günlük Değişim (%)']].rename(columns={'Close': 'Kapanış (TL)'})
                    st.dataframe(tablo_df.style.format({'Kapanış (TL)': '{:.2f} ₺', 'Günlük Değişim (%)': '{:+.2f}%'}), use_container_width=True)

                    st.subheader("📈 Teknik Göstergeler")
                    st.markdown(teknik_analiz_uret(df, haftalik_degisim))

                    st.subheader("🤖 Yapay Zekâ Analizi")
                    tablo_metni = tablo_df.to_string(index=False)
                    ai_analizi = dinamik_ai_yorum_uret(sorgu.upper(), tablo_metni, haftalik_degisim)
                    st.info(ai_analizi)
