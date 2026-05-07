import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/inquiries.json")  # プロジェクトルートからの相対パス


def load_inquiries():
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_inquiry(name, question, category, priority, answer):
    inquiries = load_inquiries()
    new_id = len(inquiries) + 1
    item = {
        "id": new_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "question": question,
        "category": category,
        "priority": priority,
        "answer": answer,
    }
    inquiries.append(item)

    DATA_PATH.parent.mkdir(exist_ok=True)

    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(inquiries, f, ensure_ascii=False, indent=2)
    return item