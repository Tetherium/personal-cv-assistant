import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

# Gizli değişkenleri yükle
load_dotenv()

app = FastAPI()

# React ile konuşmak için CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini'a OpenAI kütüphanesi üzerinden bağlanıyoruz
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# --- TELEGRAM LOG FONKSİYONU ---
def telegram_log_gonder(soru: str, cevap: str, request: Request):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Kullanıcı bilgilerini al
    ip = request.client.host
    user_agent = request.headers.get('user-agent', 'Bilinmiyor')
    
    # Telegram mesaj formatı (Markdown)
    mesaj = (
        f"🚀 *Yeni CV Asistanı Sorgusu*\n"
        f"---------------------------\n"
        f"📍 *IP:* `{ip}`\n"
        f"📱 *Cihaz:* `{user_agent[:60]}...`\n"
        f"❓ *Soru:* {soru}\n"
        f"🤖 *Cevap:* {cevap[:300]}..." # Mesajın çok uzun olup Telegram'ı kitlememesi için
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram Bildirim Hatası: {e}")

# 1. bilgi.txt dosyasını (CV'ni) okuyan fonksiyon
def veri_yukle():
    try:
        with open("bilgi.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Bilgi dosyası bulunamadı."

# 2. Gemini'a soran asıl fonksiyon
def gemini_asistan_cevap(soru: str, request: Request, dil: str = "tr"):
    kisisel_veriler = veri_yukle()
    
    dil_talimati = ""
    if dil == "en":
        dil_talimati = "6. You MUST answer this question entirely in ENGLISH."
    else:
        dil_talimati = "6. Bu soruyu tamamen TÜRKÇE olarak cevaplamalısın."

    system_prompt = f"""
    Sen Onur Çinkaya'nın dijital ikizisin ve onun profesyonel asistanısın. 
    Kişiliğin: Bilgili, özgüvenli, hafif samimi ama her zaman saygılı.
    
    VERİ KAYNAĞIN:
    ---
    {kisisel_veriler}
    ---
    
    KONUŞMA STİLİ VE KURALLAR:
    1. ROBOT OLMA: "Onur şunları bilir" yerine "Onur, React ve FastAPI konusunda oldukça derinleşti..." gibi daha doğal anlatımlar kullan.
    2. DENGE: Cevapların ne çok kısa olup geçiştirici görünsün ne de çok uzun olup insanı yorsun. Az ve öz, ama etkileyici konuş.
    3. HAFIZA: Eğer kullanıcı önceki mesajlarda bir şey sorduysa, ona atıfta bulun.
    4. YARATICILIK: Bilgi dışına çıkma ama elindeki bilgileri birleştirerek yaratıcı analizler yap. 
    5. TEKNİK DERİNLİK: Gerektiğinde teknik detaylara gir (Docker, IaC, Pintos gibi), ama karşı tarafı boğma.
    {dil_talimati}
    """
    
    try:
        response = client.chat.completions.create(
            model="models/gemini-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": soru}
            ],
            temperature=0.7
        )

        cevap_metni = response.choices[0].message.content
        
        # LOGLAMA: Telegram'a gönder
        telegram_log_gonder(soru, cevap_metni, request)
        
        return cevap_metni
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

@app.get("/sor")
async def soru_sor(soru: str, request: Request, dil: str = "tr"):
    # FastAPI otomatik olarak 'request' objesini buraya enjekte eder
    cevap = gemini_asistan_cevap(soru, request, dil)
    return {"cevap": cevap}