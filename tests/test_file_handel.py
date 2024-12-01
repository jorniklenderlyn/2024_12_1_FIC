import requests
import json


file = open('dr.json', "rb").read()
res = requests.post('http://127.0.0.1:8000/predict/', files={'file': file})

with open('data2.json', 'w', encoding="utf-8") as f:
    json.dump(res.json(), f)
print(res.json())
print(res)