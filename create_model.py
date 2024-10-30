import sqlite3
import pandas as pd
from surprise import Dataset, NormalPredictor, Reader
from surprise.model_selection import train_test_split

def make_recommendation(path):
    conn = sqlite3.connect(path)

    # Выполняем запрос и загружаем данные в DataFrame
    query = """
    SELECT 
        username, 
        article_title,
        SUM(CASE 
                WHEN action = 'like' THEN 1.0
                WHEN action = 'view' THEN 0.5
                ELSE 0 
            END) AS interaction_score
    FROM 
        log
    GROUP BY 
        username, 
        article_title;
    """
    df = pd.read_sql_query(query, conn)

    conn.close()

    # Фильтруем строки, оставляя только ссылки
    df = df[df['article_title'].str.contains(r'^https?://', na=False)]
    df = df.rename(columns={"username": "userID", "article_title": "itemID", "interaction_score": "rating"})

    # Указываем шкалу рейтинга (например, от 0.5 до 5) для библиотеки surprise
    reader = Reader(rating_scale=(0.5, 5))

    # Загружаем данные в формате, подходящем для surprise
    data = Dataset.load_from_df(df[["userID", "itemID", "rating"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2)

    model = NormalPredictor()
    model.fit(trainset)

    # Получаем уникальных пользователей и статьи
    users = df['userID'].unique()
    items = df['itemID'].unique()

    # Создаем список предсказаний
    recommendations = []

    # Для каждого пользователя предсказываем рейтинг для каждой статьи
    for user in users:
        for item in items:
            est_rating = model.predict(user, item).est
            recommendations.append((user, item, est_rating))

    recommendations_df = pd.DataFrame(recommendations, columns=['userID', 'itemID', 'estimated_rating'])
    
    # Получаем рекомендации для каждого пользователя
    top_recommendations = recommendations_df.sort_values(by=['userID', 'estimated_rating'], ascending=[True, False])

    return top_recommendations