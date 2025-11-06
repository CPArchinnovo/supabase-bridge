# ------------------------------------------------------
# 🚀 SUPABASE BRIDGE — FastAPI + Render + Wix
# ------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os

# ------------------------------------------------------
# 🌐 FASTAPI APP SETUP
# ------------------------------------------------------
app = FastAPI(title="Supabase Bridge", version="1.0")

origins = [
    "https://cpart14.wixsite.com",  # your Wix site
    "https://editor.wix.com",       # Wix editor
    "https://www.wix.com",          # fallback
    "http://localhost:3000",        # optional local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# 🔑 SUPABASE CONNECTION
# ------------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Safety check — if vars not set, log it
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ Missing SUPABASE_URL or SUPABASE_KEY in environment!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------------------------------------
# 🧠 ROOT ROUTE — Health Check
# ------------------------------------------------------
@app.get("/")
def root():
    return {"status": "✅ Supabase Bridge is running!"}

# ------------------------------------------------------
# 📦 ROOM ITEMS ENDPOINT
# ------------------------------------------------------
@app.get("/room_items")
def get_room_items(limit: int = 5):
    """
    Test endpoint for Wix — reads sdb05_room_items from Supabase.
    """
    try:
        data = supabase.table("sdb05_room_items").select("*").limit(limit).execute()
        return {"data": data.data}
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------
# ⚡ WAKEUP ENDPOINT (optional)
# ------------------------------------------------------
@app.get("/ping")
def ping():
    return {"status": "awake"}
