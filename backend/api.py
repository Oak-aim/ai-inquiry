from fastapi import FastAPI

app = FastAPI()

@app.post("/ask")
def ask(data: dict):
    text = data.get("text", "")

    return {
        "message": f"受け取った: {text}"
    }