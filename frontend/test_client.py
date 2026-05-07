import requests

res = requests.get("http://localhost:8001/")

print(res.status_code)
print(res.text)