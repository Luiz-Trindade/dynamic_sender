from os import cpu_count
from concurrent.futures import ThreadPoolExecutor as Thread
from uuid import uuid4
from datetime import datetime
from typing import Dict, List
import random
from time import sleep
import threading
from sample_messages_10k import messages_list

max_active_sessions = 5

whatsapp_sessions: Dict[str, bool] = {
    "c14f2a88eae14a8fa9b7d7766ab8493a": False,
    "a93e70de7b8c4f19b8e92a4d6a7e432f": False,
    "f0d2d7aa3c8b43b8aaf4a45bdff1d497": False,
    "e1c22f36ed4744b3a9bc3e4b891dc761": False,
    "b912f0c71e224d7e9a328ca0cfd723a3": False,
    "d9c56b1d7e2e4aa0a0c12fb840b71c0e": False,
    "3c1adf8a5db84a2084f8b289ba7b3b19": False,
    "86d7048c927b44948b4c7e0d3d91803e": False,
    "7e3e29e462db4ce38b7df9b7f7acfa2e": False,
    "1f9a75c57dc645ed921ced2f4017e7b2": False
}

active_sessions_list: List[str] = []
messages_queue: Dict[str, Dict[str, str]] = {}

#lock = threading.Lock()

def send_message(msg: str):
    random_id = uuid4().hex
    session = random.choice(list(whatsapp_sessions.keys()))
    timestamp = datetime.now().isoformat()
    messages_queue[random_id] = {
        "session"   : session,
        "message"   : msg,
        "timestamp" : timestamp
    }

def send_messages():
    with Thread(cpu_count()) as pool:
        pool.map(send_message, messages_list)

def process_message(msg_id: str, data: Dict[str, str]):
    session = data["session"]
    message = data["message"]
    timestamp = datetime.now().isoformat()

    #with lock:
    if not whatsapp_sessions[session]:
        whatsapp_sessions[session] = True
        active_sessions_list.append(session)
        print(f"[{timestamp}] ✅ Sessão {session} ativada para mensagem {msg_id}")
        sleep(1)

    if len(active_sessions_list) >= max_active_sessions:
        print(f"[{timestamp}] ⚠️ Limite de sessões atingido. Desativando todas...")
        for s in active_sessions_list:
            whatsapp_sessions[s] = False
            print(f"[{timestamp}] ❌ Sessão {s} desativada")
        active_sessions_list.clear()

    # Simula o envio da mensagem (com tempo)
    print(f"[{timestamp}] 📤 Enviando com {session}: {msg_id} - {message[:40]}...")

def run_dynamic_sender():
    with Thread(cpu_count()) as pool:
        pool.map(lambda item: process_message(*item), messages_queue.items())

def main():
    send_messages()
    run_dynamic_sender()

if __name__ == "__main__":
    main()
