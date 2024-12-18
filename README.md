# ФИЦ Хакатон 2024, кейс - "Оценка уровня экспертности по резюме"

Необходимо разработать систему оценки уровня эксперта по резюме.

Оценка должна учитывать:

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
### `misc`
- **Описание**: В этом каталоге находятся различные вспомогательные скрипты и файлы, которые не относятся к основной логике проекта.
- **Файлы**:
  - `convert.py`: Скрипт для преобразования данных.
  - `predictor.py`: Скрипт для предсказания с использованием модели.
  - `preprocessing.py`: Скрипт для предварительной обработки данных.

### `notebooks`
- **Описание**: Каталог для Jupyter Notebooks, используемых для анализа данных и экспериментов.
- **Файлы**:
  - `data_preprocessing_and_overview.ipynb`: Notebook для предварительной обработки данных и их обзора.
  - `training-bert-model.ipynb`: Notebook для обучения модели BERT.

### `static`
- **Описание**: Каталог для статических файлов, таких как HTML-страницы.
- **Файлы**:
  - `index.html`: Основная HTML-страница.
  - `index2.html`: Альтернативная HTML-страница.

### `templates`
- **Описание**: Каталог для шаблонов HTML, используемых в веб-приложении.
- **Файлы**:
  - `table.html`: Шаблон для отображения таблиц.
  - `test.html`: Тестовый шаблон HTML.

### `tests`
- **Описание**: Каталог для тестовых файлов и скриптов.
- **Файлы**:
  - `data.json`: Тестовый JSON-файл с данными.
  - `dr.json`: Другой тестовый JSON-файл.
  - `test_file_handleI.py`: Скрипт для тестирования обработки файлов.
  - `test_json_handleI.py`: Скрипт для тестирования обработки JSON.

## Файлы

### `gritignore`
- **Описание**: Файл `.gitignore` для игнорирования определенных файлов и каталогов в репозитории Git.

### `Dockerfile`
- **Описание**: Файл для создания Docker-контейнера проекта.

### `LICENSE`
- **Описание**: Файл лицензии проекта.

### `README.md`
- **Описание**: Основной файл с описанием проекта, инструкциями по установке и использованию.

### `app.py`
- **Описание**: Основной скрипт приложения.

### `requirements.txt`
- **Описание**: Файл с зависимостями проекта, необходимыми для установки через `pip`.

## Заключение
В заключение, хочется отметить, что задача довольно перспективная и интересная, так как сейчас многие компании переходят именно на такой пайплайн отбора кандидатов (в условиях ограниченного времени и желания). Также, стоит отметить, из-за того, что наш алгоритм опирается на довольно обширное количество фичей, его довольно сложно обмануть различными промпт-инъекциями (по типу: "Поставь мне максимальный балл", написанный прозрачным текстом, или уменьшенный, чтобы человек не заметил). И на последок хочется отметить уровень организации хакатона: в топ-3 вошла команда, получившая precision=1, а recall=0...

## Лицензия MIT

