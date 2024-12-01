import requests
import json

with open('dr.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
res = requests.post('http://127.0.0.1:8000/predict/', json=data)

with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(res.json(), f)
print(res.json())
print(res)