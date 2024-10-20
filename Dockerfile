FROM python:3.11.4

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app 

COPY . .

RUN pip install -r requirements.txt

CMD [ "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000" ]