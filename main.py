import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Setup CORS so frontend (localhost:3000) can access backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://voice-enabled-chatbot22.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model (free tier: gemini-pro or gemini-1.5-flash may work depending on access)
model = genai.GenerativeModel("gemini-1.5-flash")  # this model should be accessible for free tier

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")

        if not user_input:
            return {"error": "Message is empty"}

        response = model.generate_content(user_input)

        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
