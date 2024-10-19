import requests
import json

file = open('X:\\Projects\\Новая папка\\tests\\data\\db_short4.sqlite', "rb").read()
res = requests.post('http://127.0.0.1:8000/get-result/', files={'file': file})

with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(res.json(), f)
print(res.json)
print(res)