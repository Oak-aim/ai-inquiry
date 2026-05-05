import os
import json
from datetime import datetime

def save_inquiry(text):
    os.makedirs("data", exist_ok=True)

    data = {
        "text": text,
        "time": datetime.now().isoformat()
    }

    file_path = "data/inquiries.json"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")