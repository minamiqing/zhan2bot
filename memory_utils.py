import json
from datetime import datetime

MEMORY_FILE = 'memory.json'

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"user_id": "123", "memories": []}

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_memory(content, type_="一般"):
    data = load_memory()
    data['memories'].append({
        "type": type_,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    })
    save_memory(data)
