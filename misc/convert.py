import pandas as pd
import re
import sqlite3
import torch
from tqdm import tqdm


def contains_emoji(text):
    if text == None:
        return False
    # Регулярное выражение для поиска эмодзи
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Эмоциональные смайлы
        "\U0001F300-\U0001F5FF"  # Символы и пиктограммы
        "\U0001F680-\U0001F6FF"  # Транспорт и символы
        "\U0001F700-\U0001F77F"  # Дополнительные символы
        "\U0001F780-\U0001F7FF"  # Символы и пиктограммы (доп.)
        "\U0001F800-\U0001F8FF"  # Дополнительные эмодзи
        "\U0001F900-\U0001F9FF"  # Символы и эмодзи (доп.)
        "\U0001FA00-\U0001FA6F"  # Символы спорта и предметов
        "\U0001FA70-\U0001FAFF"  # Символы и объекты"
        "\u2600-\u26FF\u2700-\u27BF"  # Разные символы (например, ☀, ✈)
        "]+", flags=re.UNICODE
    )
    return bool(emoji_pattern.search(text))


def preprocess_photo(df_photo, df_user: pd.DataFrame):
    like_count = df_photo[['user_id','like_count']]
    df_avg_likes = like_count.groupby('user_id')['like_count'].mean().reset_index()
    df_avg_likes.columns = ['id', 'average_likes']
    df_avg_likes['average_likes'] = df_avg_likes['average_likes'].round()
    df_user = df_user.merge(df_avg_likes, on ='id', how='left')
    return df_user


def preprocess_friends(df_friend,df_user):
    friend_counts = df_friend.groupby('user_id')['id'].nunique().reset_index()
    friend_counts.columns = ['user_id', 'friend_count']
    friend_counts.rename(columns={'user_id': 'id'}, inplace=True)
    df_user = df_user.merge(friend_counts, on='id', how='left')
    df_user.friend_count = df_user.friend_count.fillna(0)
    return df_user


def preprocess_groups(df_group_table, df_user):
    count_groups = df_group_table.groupby('user_id')['id'].nunique().reset_index()
    count_groups.columns = ['user_id', 'count_groups']
    count_groups.rename(columns={'user_id': 'id'}, inplace=True)
    df_user = df_user.merge(count_groups, on='id', how='left')
    df_user.count_groups = df_user.count_groups.fillna(0)
    return df_user


def preprocess_images(df_photo, df_user):
    count_images = df_photo.groupby('user_id')['id'].nunique().reset_index()
    count_images.columns = ['user_id', 'count_images']
    count_images.rename(columns={'user_id': 'id'}, inplace=True)
    df_user = df_user.merge(count_images, on='id', how='left')
    df_user.count_images = df_user.count_images.fillna(0)
    return df_user


def get_avg(string):
    s = list(map(len, re.split(r"[\.\?!]", string)))
    return sum(s) / len(s)


def get_ya_num(string):
    string = "," + string + ','
    s = re.findall(r"[\W ][Яя][ \W]", string)
    # if len(s) > 7:
    #     print(s, string)
    return len(s)


def get_features_suite1(df_post):
    df_total_posts = df_post.groupby('user_id')['text'].count().reset_index()
    df_total_posts.columns = ['user_id', 'total_posts']
    df_creator_posts = df_post[df_post['isowner'] == 1].groupby('user_id')['text'].count().reset_index()
    df_creator_posts.columns = ['user_id', 'created_posts']
    df_result = df_total_posts.merge(df_creator_posts, on='user_id', how='left').fillna(0)
    df_result['ratio_post'] = df_result['total_posts'] / df_result['created_posts']
    return df_result


def get_features_suite2(df_post):

    df_post['frequency'] = df_post['date'].astype('int64') / 86400000
    df_post['contained_emoji'] = df_post['text'].apply(lambda x: contains_emoji(x))

    df_res = df_post.groupby(['user_id']).agg({'frequency': lambda x: (x.max() - x.min()) / (x.count() - 1), 'contained_emoji': 'max'})
    df_post["chtoto"] = df_post.sort_values("frequency").groupby(['user_id'])["frequency"].diff()
    df_res["min_diff"] = df_post.sort_values("frequency").groupby("user_id")["chtoto"].min()
    df_res["max_diff"] = df_post.sort_values("frequency").groupby("user_id")["chtoto"].max()
    df_res["count_question_mark"] = df_post.query('isowner == 1').groupby("user_id").agg({'text': lambda x: x.apply(lambda x: None if x is None 
                                                                                                    else x.count('?')).sum()})
    
    df_res["count_exclamation_mark"] = df_post.query('isowner == 1').groupby("user_id").agg({'text': lambda x: x.apply(lambda x: None if x is None 
                                                                                                  else x.count('!')).sum()})
    df_res["average_post_len"] = df_post.query('isowner == 1').groupby("user_id").agg({"text": lambda x : x.apply(lambda x: 0 if x is None else len(x)).mean()})

    def get_avg(string):
        s = list(map(len, re.split(r"[\.\?!]", string)))
        return sum(s) / len(s)

    df_res['average_sentence_len'] = df_post.query('isowner == 1').groupby("user_id").agg({"text": lambda x : x.apply(lambda x: 0 if x is None else get_avg(x)).mean()})

    def get_ya_num(string):
        string = "," + string + ','
        s = re.findall(r"[\W ][Яя][ \W]", string)
        # if len(s) > 7:
        #     print(s, string)
        return len(s)

    df_res['average_used_ya'] = df_post.query('isowner == 1').groupby("user_id").agg({"text": lambda x : x.apply(lambda x: 0 if x is None else get_ya_num(x)).mean()})
    
    return df_res


def preproccesing_post(df_post,df_user):
    post_df = get_features_suite1(df_post).merge(get_features_suite2(df_post),on='user_id',how ='left')
    post_df.rename(columns={'user_id': 'id'}, inplace=True)
    df_user = df_user.merge(post_df,on ='id',how ='left')
    return df_user


def preproccesing_img2txt(df_photo, df_user):
    if df_photo.shape[0] == 0:
        df_user[['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']] = None
        return df_user

    data  = df_photo[['user_id','igm2txt']]
    from transformers import BertTokenizer, BertForSequenceClassification

    tokenizer = BertTokenizer.from_pretrained("Minej/bert-base-personality")
    model = BertForSequenceClassification.from_pretrained("Minej/bert-base-personality")
    model.eval()

    quantized_model = torch.quantization.quantize_dynamic(
        model, 
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    
    def personality_detection(text, user_id):
        inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        predictions = outputs.logits.squeeze().detach().cpu().numpy()
        label_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
        result = {label_names[i]: predictions[i] for i in range(len(label_names))}
        result['user_id'] = user_id
    
        return result

    results = []
    for user_id, text in tqdm(data.values):
        result = personality_detection(text, user_id)
        results.append(result)
    df_results = pd.DataFrame(results)
    df_avg = df_results.groupby('user_id').mean().reset_index()
    df_avg.rename(columns={'user_id': 'id'}, inplace=True)
    df_user = df_user.merge(df_avg, on='id', how='left')
    return df_user


def process_tab(df_post, df_user, df_photo, df_friend, df_group_table):
    df_user = preprocess_photo(df_photo, df_user)
    df_user = preproccesing_img2txt(df_photo,df_user) #сделай люто проверки на проверку если фоток нема то добавь 5 столбцов из функции и ебаш наны
    df_user = preproccesing_post(df_post,df_user)
    df_user = preprocess_friends(df_friend, df_user)
    df_user = preprocess_groups(df_group_table, df_user)
    df_user = preprocess_images(df_photo, df_user)
    tagging_info = df_user[['id','age','friend_count','Extroversion','Neuroticism','Agreeableness','Conscientiousness','Openness','average_likes','count_groups','count_images','total_posts','created_posts','ratio_post','frequency','contained_emoji','min_diff','max_diff','count_question_mark','count_exclamation_mark','average_post_len','average_sentence_len','average_used_ya']]
    # tagging_info = df_user[['id','age','friend_count','average_likes','count_groups','count_images','total_posts','created_posts','ratio_post','frequency','contained_emoji','min_diff','max_diff','count_question_mark','count_exclamation_mark','average_post_len','average_sentence_len','average_used_ya']]
    return tagging_info

# def nathing():
#     cnx = sqlite3.connect(path_to_db)
#     df_post = pd.read_sql_query("SELECT * FROM post", cnx)
#     df_user = pd.read_sql_query("SELECT * FROM user",cnx)
#     df_photo = pd.read_sql_query("SELECT * FROM photo",cnx)
#     df_friend = pd.read_sql_query("SELECT * FROM friend",cnx)   

def process_tab2(path_to_db):
    cnx = sqlite3.connect(path_to_db)
    df_post = pd.read_sql_query("SELECT * FROM post", cnx)
    df_user = pd.read_sql_query("SELECT * FROM user",cnx)
    df_photo = pd.read_sql_query("SELECT * FROM photo",cnx)
    df_friend = pd.read_sql_query("SELECT * FROM friend",cnx)
    df_user = preprocess_photo(df_photo,df_user)
    df_user = preproccesing_img2txt(df_photo,df_user) #сделай люто проверки на проверку если фоток нема то добавь 5 столбцов из функции и ебаш наны
    df_user = preproccesing_post(df_post,df_user)
    df_user = preprocess_friends(df_friend, df_user)
    tagging_info = df_user[['id','age','friend_count','Extroversion','Neuroticism','Agreeableness','Conscientiousness','Openness','average_likes','count_groups','count_images','total_posts','created_posts','ratio_post','frequency','contained_emoji','min_diff','max_diff','count_question_mark','count_exclamation_mark','average_post_len','average_sentence_len','average_used_ya']]
    return tagging_info