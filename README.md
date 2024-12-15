# ФИЦ Хакатон 2024, кейс - "Оценка уровня экспертности по резюме"

Необходимо разработать систему оценки уровня эксперта по резюме.

Оценка должна должна учитывать:

    - Рейтинг организаций, в которых работал кандидат
    - Годы релевантного опыта
    - Компания, куда собеседуется кандидат
    - Грейд внутри компании, где работал кандидат

## Установка и запуск проекта
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
## Основной функционал проекта
Проект представляет из себя API интефейс общения с моделью предсказания уровня эксперта по входному тексту резюме.

## Технологии и инструменты
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## Команда проекта
![Душенев Даниил](https://github.com/daniil-dushenev) - ML-engineer, разработка пайплайна обучения и инференса модели

![Сергеев Даниил](https://github.com/DaniilSergeev17) - ML-engineer, разработка пайплайна обучения, предобработка текста

![Гречин Егор](https://github.com/whoissleep) - ML-engineer, разработка пайплайна обучения, предобработка текста

![Кайков Дмитрий](https://github.com/jorniklenderlyn) - Backend, разработка сервиса API для общения с моделью


## Структура проекта
TODO: расписать

## Заключение
TODO: написать

## Лицензия MIT

