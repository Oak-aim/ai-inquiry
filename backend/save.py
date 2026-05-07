import os
import json
from datetime import datetime

FILE_PATH = "data/inquiries.json"

def save_inquiry(data):
    os.makedirs("data", exist_ok=True)

    inquiry_data = {
        "name": data["name"],
        "category": data["category"],
        "priority": data["priority"],
        "question": data["question"],
        "time": datetime.now().isoformat()
    }

    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(inquiry_data, ensure_ascii=False) + "\n")

def load_inquiries():
    inquiries = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        inquiries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

    return inquiries