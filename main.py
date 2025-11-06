from fastapi import FastAPI
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
import os

# ------------------------------------------------------
# 🔧 SETUP
# ------------------------------------------------------
SUPABASE_URL = "https://twlduqptfrkmwhyglzsi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3bGR1cXB0ZnJya213aHlnbXpsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTI2MjI0NiwiZXhwIjoyMDc2ODM4MjQ2fQ._JSvX4KZKnAh4nvRaoAYfFyhliTLPzh0QZk4_hbN7To"  # (not anon)

app = FastAPI()

# CORS – allow Wix, Bolt, Emergent to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------------------------------------
# 🧠 TEST ROUTE
# ------------------------------------------------------
@app.get("/")
def root():
    return {"status": "✅ Supabase Bridge is running!"}

# ------------------------------------------------------
# 📦 GET ROOM ITEMS
# ------------------------------------------------------
@app.get("/getRoomItems")
def get_room_items(limit: int = 5):
    try:
        data = supabase.table("sdb05_room_items").select("*").limit(limit).execute()
        return {"data": data.data}
    except Exception as e:
        return {"error": str(e)}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os

app = FastAPI()

# ✅ Allow Wix access (open for now — we’ll tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"status": "ok", "message": "Bridge connected to Supabase"}

@app.get("/room_items")
def get_room_items():
    # Replace 'sdb05_room_items' with your actual Supabase table
    response = supabase.table("sdb05_room_items").select("*").execute()
    return response.data
