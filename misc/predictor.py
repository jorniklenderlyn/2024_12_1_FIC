import pandas as pd
import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
from torch.utils.data import Dataset


def create_template_string(row):
        return f"Куда собеседуется кандидат: {row['position']}, Ключевые навыки кандидата: {row['key_skills']}, Опыт работы кандидата: {row['work_experience']}, Зарплатные ожидания: {row['salary']}, Компания куда собеседуется кандидат: {row['client_name']}"


def tokenize_data(tokenizer, data, max_length=2048):
        return tokenizer(data, truncation=True, padding=True, max_length=max_length, return_tensors="pt")


def get_prediction(input_df: pd.DataFrame) -> list:
    # return pd.DataFrame([i for i in range(input_df.shape[0])])
    # Применяем функцию к каждой строке датафрейма
    input_df['template_string'] = input_df.apply(create_template_string, axis=1)

    # Обработка целевой переменной
    target = input_df['grade_proof']
    tag2id = {elem: i for i, elem in enumerate(target.unique())}
    id2tag = {i: elem for i, elem in enumerate(target.unique())}
    target = target.apply(lambda x: tag2id[x])

    # TODO: сделаешь подгрузку модели хз откуда с HF или с файла
    # model_id = "sergeyzh/rubert-tiny-turbo"    
    model = AutoModelForSequenceClassification.from_pretrained('danilka200300/results3')
    tokenizer = AutoTokenizer.from_pretrained('sergeyzh/rubert-tiny-turbo')

    # токенизируешь
    tokenized_data = tokenize_data(tokenizer, input_df['template_string'].tolist())

    # предсказываешь, возвращай результат в виде списка лейблов уже округленных
    model.eval()
    label2text = {
         0: "Не прошел",
         1: "Прошел"
    }
    with torch.no_grad():
        outputs = model(**tokenized_data)
        predictions = torch.argmax(outputs.logits, dim=1).tolist()
        predictions = [label2text[pred] for pred in predictions]
    
    return predictions  
