# ФИЦ Хакатон 2024, кейс - "Оценка уровня экспертности по резюме"

```
python 3.11.4
pip install -r rquirements.txt
python app.py
```
Получение классификации через request
```python
import requests
import json


# Отправка файла
file = open(<filename>, "rb").read()
res = requests.post('http://127.0.0.1:8000/predict/', files={'file': file})
# Отправка json
with open(<filename>, 'r', encoding='utf-8') as f:
    data = json.load(f)
res = requests.post('http://127.0.0.1:8000/predict/', json=data)
```