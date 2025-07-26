from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor as Thread
from uuid import uuid4
from time import sleep
import uvicorn
from os import cpu_count
from diskcache import Cache

# ==== Inicializações ====
app = FastAPI()
cache = Cache("cache_dir")
max_active_sessions = 5

# Inicializa se ainda não houver
if "active_sessions_list" not in cache:
    cache["active_sessions_list"] = []

if "messages_queue" not in cache:
    cache["messages_queue"] = {}

# ==== Models ====
class MessageItem(BaseModel):
    session_id: str
    message: str

class MessagesPayload(BaseModel):
    messages: List[MessageItem]

# ==== Funções ====
def enqueue_message(msg: MessageItem):
    random_id = uuid4().hex
    queue = cache["messages_queue"]
    queue[random_id] = {
        "session": msg.session_id,
        "message": msg.message
    }
    cache["messages_queue"] = queue

def process_message(msg_id: str, data: Dict[str, str]):
    active_sessions = cache["active_sessions_list"]
    session = data["session"]
    message = data["message"]

    if session not in active_sessions:
        active_sessions.append(session)
        cache["active_sessions_list"] = active_sessions
        print(f"✅ Sessão {session} ativada para mensagem {msg_id}")
        sleep(1)

    if len(active_sessions) >= max_active_sessions:
        print(f"⚠️ Limite de sessões atingido. Desativando todas...")
        for s in active_sessions:
            print(f"❌ Sessão {s} desativada")
        cache["active_sessions_list"] = []

    print(f"📤 Enviando com {session}: {msg_id} - {message[:40]}...")

def run_dynamic_sender():
    messages = cache["messages_queue"]
    with Thread(max_workers=cpu_count()) as pool:
        pool.map(lambda item: process_message(*item), messages.items())

# ==== Endpoint ====
@app.post("/send")
async def send_messages_api(payload: MessagesPayload):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="Lista de mensagens vazia.")

    cache["messages_queue"] = {}
    cache["active_sessions_list"] = []

    with Thread(max_workers=cpu_count()) as pool:
        pool.map(enqueue_message, payload.messages)

    run_dynamic_sender()

    return {
        "status": "Mensagens processadas",
        "total": len(payload.messages)
    }

# ==== Execução ====
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
