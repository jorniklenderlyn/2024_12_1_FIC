import os


os.environ['OPENBLAS_NUM_THREADS'] = '1'


from fastapi import FastAPI, Request, UploadFile, HTTPException, status, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import pandas as pd
import aiofiles
import datetime
import uvicorn
import sqlite3


from misc.predictor import get_prediction
from misc.convert import process_tab


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_user_ids(connection):
    ids = pd.read_sql_query("SELECT id FROM user", connection)
    return ids['id'].to_list() 


def get_user_info(user_id, connection):
    info = pd.read_sql_query(f"SELECT * FROM user WHERE id = {user_id}", connection)
    info = info.to_dict()
    res = dict()
    for k in info:
        res[k] = info[k][0]
    return res


def get_user_tables(user_id, connection):
    if user_id == -1:
        df_post = pd.read_sql_query("SELECT * FROM post", connection)
        df_photo = pd.read_sql_query("SELECT * FROM photo", connection)
        df_group_table = pd.read_sql_query("SELECT * FROM group_table", connection)
        df_friend = pd.read_sql_query("SELECT * FROM friend", connection)
        df_biography = pd.read_sql_query("SELECT * FROM biography", connection)
        df_user = pd.read_sql_query("SELECT * FROM user", connection)
    else:
        df_post = pd.read_sql_query(f"SELECT * FROM post WHERE user_id = {user_id}", connection)
        df_photo = pd.read_sql_query(f"SELECT * FROM photo WHERE user_id = {user_id}", connection)
        df_group_table = pd.read_sql_query(f"SELECT * FROM group_table WHERE user_id = {user_id}", connection)
        df_friend = pd.read_sql_query(f"SELECT * FROM friend WHERE user_id = {user_id}", connection)
        df_biography = pd.read_sql_query(f"SELECT * FROM biography WHERE user_id = {user_id}", connection)
        df_user = pd.read_sql_query(f"SELECT * FROM user WHERE id = {user_id}", connection)
    return {"post": df_post, "photo": df_photo, "group_table": df_group_table, "friend": df_friend, "biography": df_biography, "user": df_user}


def get_users_with_type(path_to_db) -> pd.DataFrame:
    connection = sqlite3.connect(path_to_db)
    # user_ids = get_user_ids(connection)
    tables = get_user_tables(-1, connection)
    connection.close()

    X = process_tab(df_post=tables["post"], df_user=tables["user"], df_photo=tables["photo"], df_friend=tables["friend"], df_group_table=tables["group_table"])
    # X.to_csv("X.csv")
    Y_ = get_prediction(X)

    df_user = tables["user"]
    df_user["predict"] = Y_
    # return X
    return df_user


@app.get("/get-result/", response_class=HTMLResponse)
async def get_result(request: Request, db_name: str='db.sqlite'):
    path_to_db = os.path.join(os.getcwd(), 'temp', db_name)

    if not os.path.exists(path_to_db):
        return "data does not exist!"
    
    result = get_users_with_type(path_to_db)
    # res = get_user_with_type(path_to_db)
    columns_ = result.columns.to_list()
    columns_[0] = 'db_id'
    result.columns = columns_

    columns = result.columns
    data = result.to_numpy()

    # for r in res:
    #     row = []
    #     for k in r:
    #         row.append(r[k])
    #     data.append(row)
    try:
        os.remove(path_to_db)
    except:
        print("Error, when deleting temp file!")
        
    return templates.TemplateResponse(
        'table2.html',
        {'request': request, 'columns': columns, 'data': data}
    )
    # return 'hello, world!'


@app.post("/get-result/")
async def create_file(file: UploadFile):
    time_stamp = datetime.datetime.now().microsecond
    filename = f'db{time_stamp}.db'
    contents = await file.read()
    async with aiofiles.open(os.path.join(os.getcwd(), 'temp', filename), 'wb') as f:
        await f.write(contents)

    path_to_db = os.path.join(os.getcwd(), 'temp', filename)
    result = get_users_with_type(path_to_db)
    result = result[['id', 'vk_id', 'predict']]
    columns_ = result.columns.to_list()
    columns_[0] = 'db_id'
    result.columns = columns_

    data = result.to_dict()

    try:
        os.remove(os.path.join(os.getcwd(), 'temp', filename))
    except:
        print("Error, when deleting temp file!")
    
    return {"predict": data}


@app.post('/upload')
async def upload(file: UploadFile):
    time_stamp = datetime.datetime.now().microsecond
    filename = f'db{time_stamp}.db'
    try:
        contents = await file.read()
        async with aiofiles.open(os.path.join(os.getcwd(), 'temp', filename), 'wb') as f:
            await f.write(contents)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error uploading the file',
        )
    finally:
        await file.close()

    return RedirectResponse(url=f"/get-result?db_name={filename}", status_code=status.HTTP_302_FOUND)
    # return {'message': f'Successfuly uploaded {filename}', 'time': time_stamp}


@app.get('/', response_class=HTMLResponse)
async def main():
    with open("static/index.html", encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
    # nathing()
    # df = pd.read_csv('X.csv')[['id','age','friend_count','Extroversion','Neuroticism','Agreeableness','Conscientiousness','Openness','average_likes','count_groups','count_images','total_posts','created_posts','ratio_post','frequency','contained_emoji','min_diff','max_diff','count_question_mark','count_exclamation_mark','average_post_len','average_sentence_len','average_used_ya']]
    # print(get_prediction(df))
    # print(df[['id','age','friend_count','Extroversion','Neuroticism','Agreeableness','Conscientiousness','Openness','average_likes','count_groups','count_images','total_posts','created_posts','ratio_post','frequency','contained_emoji','min_diff','max_diff','count_question_mark','count_exclamation_mark','average_post_len','average_sentence_len','average_used_ya']])