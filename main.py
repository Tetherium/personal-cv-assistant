import os
import requests
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "I am alive!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.client.host

def get_ip_info(ip: str):
    if ip in ["127.0.0.1", "::1", "localhost"]:
        return "Localhost"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('city', 'Unknown')}, {data.get('country', '')}"
        return "Location Not Found"
    except Exception:
        return "Location Error"

def telegram_log(question: str, answer: str, request: Request, city: str, duration: float, ip: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Skip if Telegram is not configured
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        return

    user_agent = request.headers.get('user-agent', 'Unknown')
    message = (
        f"✅ *CV Assistant Query*\n"
        f"---------------------------\n"
        f"📍 *IP:* `{ip}`\n"
        f"🌍 *Location:* `{city}`\n"
        f"📱 *Device:* `{user_agent[:60]}...`\n"
        f"⏱️ *Duration:* `{duration:.2f}s`\n"
        f"❓ *Question:* {question}\n"
        f"🤖 *Answer:* {answer[:300]}..."
    )

    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
            timeout=5
        )
    except Exception as e:
        print(f"Telegram notification error: {e}")

def load_data():
    try:
        with open("bilgi.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Data file not found."

def get_ai_response(question: str, request: Request, language: str = "tr"):
    start_time = time.time()
    personal_data = load_data()

    language_instruction = (
        "6. You MUST answer this question entirely in ENGLISH."
        if language == "en"
        else "6. You MUST answer this question entirely in TURKISH."
    )

    # ⚠️ Replace [YOUR FULL NAME] with the name from your bilgi.txt
    system_prompt = f"""
    You are the digital assistant of [YOUR FULL NAME].
    Personality: Knowledgeable, confident, slightly warm but always professional.

    YOUR DATA SOURCE:
    ---
    {personal_data}
    ---

    CONVERSATION RULES:
    1. Be natural. Use engaging language, not robotic phrasing.
    2. Be balanced. Not too brief, not too long. Concise but impactful.
    3. Be contextual. Reference earlier messages in the conversation if relevant.
    4. Be creative. Combine facts to produce insightful analyses.
    5. Be technical when needed. Dive into details, but don't overwhelm the user.
    {language_instruction}
    """

    try:
        response = client.chat.completions.create(
            model="models/gemini-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        duration = time.time() - start_time
        ip = get_client_ip(request)
        city = get_ip_info(ip)
        telegram_log(question, answer, request, city, duration, ip)
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.get("/sor")
async def ask(soru: str, request: Request, dil: str = "tr"):
    return {"cevap": get_ai_response(soru, request, dil)}