import requests
import random
from concurrent.futures import ThreadPoolExecutor
from sample_messages import messages_list
from os import cpu_count

API_URL = "http://localhost:8000/send"
BATCH_SIZE = 500  # Dividir em lotes
SESSIONS = [
    "c14f2a88eae14a8fa9b7d7766ab8493a",
    "a93e70de7b8c4f19b8e92a4d6a7e432f",
    "f0d2d7aa3c8b43b8aaf4a45bdff1d497",
    "e1c22f36ed4744b3a9bc3e4b891dc761",
    "b912f0c71e224d7e9a328ca0cfd723a3",
    "d9c56b1d7e2e4aa0a0c12fb840b71c0e",
    "3c1adf8a5db84a2084f8b289ba7b3b19",
    "86d7048c927b44948b4c7e0d3d91803e",
    "7e3e29e462db4ce38b7df9b7f7acfa2e",
    "1f9a75c57dc645ed921ced2f4017e7b2"
]

def build_payload(messages):
    """Monta o payload com sessão aleatória para cada mensagem"""
    return [
        {
            "session_id": random.choice(SESSIONS),
            "message": msg
        }
        for msg in messages
    ]

def split_batches(messages, batch_size):
    return [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]

def post_batch(batch, index):
    payload = {"messages": build_payload(batch)}
    print(f"📤 Enviando lote {index} com {len(batch)} mensagens...")

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Lote {index} enviado com sucesso.")
        else:
            print(f"❌ Erro no lote {index}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Erro de conexão no lote {index}: {str(e)}")

def send_all_batches():
    batches = split_batches(messages_list, BATCH_SIZE)

    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        for i, batch in enumerate(batches, 1):
            executor.submit(post_batch, batch, i)

if __name__ == "__main__":
    send_all_batches()
