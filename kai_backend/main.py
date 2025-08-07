from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from pydantic import BaseModel
from chatbot import Chatbot
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

app = FastAPI()
kai_bot = Chatbot(api_key=API_KEY)

# --- Add CORS Middleware ---
# This will allow your React frontend (running on a different port)
# to communicate with this backend.
origins = [
    "http://localhost",
    "http://localhost:3000", # The default port for React dev server
    "*" # Allow all origins - for development purposes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)


class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Receives a user message and returns Kai's response for a given session."""
    response_text = kai_bot.get_response(request.session_id, request.message)
    return {"session_id": request.session_id, "response": response_text}

@app.get("/chats/{session_id}")
async def get_chat_history_endpoint(session_id: str):
    """Retrieves the full chat history for a given session."""
    history = kai_bot.get_chat_history(session_id)
    return {"session_id": session_id, "history": history}

@app.get("/")
def read_root():
    return {"message": "Kai Chatbot API is running. Go to /docs to see the API documentation."}
