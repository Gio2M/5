import pandas as pd

"""Se indican los archivos con los que se va a trabajar
"""

# Se especifican las rutas de los archivos CSV conque se van a trabajar
file_path = 'Data/Datos_csv/reviews_nlp.csv'
file_path1 = 'Data/Datos_csv/games.csv'
file_path2 = 'Data/Datos_csv/df_train_filtrado.csv'


# Se leen los archivos CSV y crean los DataFrame
reviews = pd.read_csv(file_path, parse_dates= ['posted'])
games = pd.read_csv(file_path1, parse_dates= ['release_date'])
df_train_filtrado = pd.read_csv(file_path2)




"""
Se crean las funciones para los endpoints
"""


def countreviews(start_date, end_date):
    # Filtrar las filas del DataFrame entre las fechas dadas
    filtered_reviews = reviews[(reviews['posted'] >= start_date) & (reviews['posted'] <= end_date)]
    
    # Contar la cantidad de usuarios únicos que realizaron reviews en el período dado
    unique_users_count = filtered_reviews['user_id'].nunique()
    
    # Calcular el porcentaje de recomendación basado en la columna "recommend"
    recommend_percentage = (filtered_reviews['recommend'].sum() / len(filtered_reviews)) * 100
    
    # Crear un diccionario con los resultados
    results = {
        f"Cantidad de usuarios que realizaron reviews entre {start_date} y {end_date}: {unique_users_count}. "
        f"Porcentaje de recomendación en base a recommend: {recommend_percentage:.2f} %"
    }
    return results



def sentiment_analysis(date_str):
    # Convierte la cadena de fecha de entrada a un objeto datetime
    target_date = pd.to_datetime(date_str)
    
    # Filtra las reseñas que coincidan con el año objetivo
    filtered_reviews = reviews[reviews['posted'].dt.year == target_date.year]
    
    # Realiza el conteo de las categorías de sentimiento
    sentiment_counts = filtered_reviews['sentiment_analysis'].value_counts()
    
    # Crea una lista con los recuentos de categorías
    result_list = f'Negative = {sentiment_counts.get(0, 0)}, Neutral = {sentiment_counts.get(1, 0)}, Positive = {sentiment_counts.get(2, 0)}'
    
     # Crear un diccionario con los resultados
    results1 = {
        f"Para el año de lanazamiento {date_str} se registraron las siguientes reseñas por categoria: {result_list}" 
    }    
    return results1



def developers_por_letra(letra):

    # Filtrar los desarrolladores cuyos nombres comienzan con la letra especificada
    filtered_developers = games[games['developer'].str.startswith(letra, na=False)]['developer'].unique()
    
    return list(filtered_developers)



def developer_juegos_gratis(empresa_desarrolladora: str):
    # Filtra el DataFrame para obtener solo las filas de la empresa desarrolladora especificada
    developer_df = games[games['developer'] == empresa_desarrolladora]
    
    # Agrupa por año y cuenta la cantidad de juegos lanzados en cada año
    games_by_year = developer_df.groupby(developer_df['release_date'].dt.year)['item_id'].count()
    
    # Cuenta la cantidad de juegos gratuitos lanzados en cada año
    free_games_by_year = developer_df[developer_df['price'] == 'Free To Play'].groupby(developer_df['release_date'].dt.year)['item_id'].count()
    
    # Calcula el porcentaje de juegos gratuitos por año
    percentage_free_by_year = (free_games_by_year / games_by_year * 100).fillna(0)

     # Crear un diccionario con los resultados
    results2 = {
        empresa_desarrolladora: {f'{year}': {
                 'total_games': float(games_by_year.get(year, 0)),
             'percentage_free': round(percentage, 1)
            }
            for year, percentage in percentage_free_by_year.items()
        }
    }
    
    return results2



def user_id():
    # Suponiendo que 'reviews' es tu DataFrame
    valores_unicos_user_id = df_train_filtrado['user_id'].unique().tolist()

    # Imprime la lista de valores únicos de 'user_id'
    return valores_unicos_user_id


"""
Definimos y entrenamos el sistema de recomendacion
"""

from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
#from surprise.model_selection import KFold
from surprise import accuracy
from surprise import KNNBasic #, KNNWithMeans, KNNBaseline
#import joblib
#from surprise import SVD

# Cargar el modelo
#algo = joblib.load('modelo_surprise.pkl')

# Configura el lector y la escala de calificación (ajusta esto según tus datos)
reader = Reader(rating_scale=(0, 1))

# Carga los datos
data = Dataset.load_from_df(df_train_filtrado[['user_id', 'item_id', 'recommend']], reader)

# Divide los datos en conjuntos de entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2)

# Crea el modelo KNN (K-Nearest Neighbors) para encontrar usuarios similares
sim_options = {'name': 'pearson', 'user_based': True}
algo = KNNBasic(sim_options=sim_options)

# Entrena el modelo en el conjunto de entrenamiento
algo.fit(trainset)

# # Supongamos que tenemos un usuario de interés con user_id = 'tu_usuario'
# def similar_user(tu_usuario: str):

#     # Encuentra los usuarios más similares al usuario de interés
#     similar_users = algo.get_neighbors(algo.trainset.to_inner_uid(tu_usuario), k=10)

#     # Filtra las reseñas de los usuarios similares
#     reviews_similares = reviews[reviews['user_id'].isin([algo.trainset.to_raw_uid(uid) for uid in similar_users])]

#     # Filtra las reseñas de juegos que han sido recomendados (recommend=True)
#     juegos_recomendados = reviews_similares[reviews_similares['recommend']]

#     # Obtén la lista de juegos recomendados por usuarios similares
#     juegos_recomendados_lista = juegos_recomendados['item_id'].unique()

#     # Inicializa una lista vacía para almacenar los juegos encontrados
#     juegos_encontrados = []

#     # Itera a través de la lista de juegos recomendados
#     for juego_id in juegos_recomendados_lista:
#         # Busca el juego en el DataFrame games
#         juego = games[games['item_id'] == juego_id]
        
#         # Si se encuentra el juego, agrégalo a la lista de juegos encontrados
#         if not juego.empty:
#             juegos_encontrados.append(juego[['item_id', 'app_name']])  # Agrega solo las columnas "item_id" y "app_name" del juego encontrado

#         # Si ya hemos encontrado 5 juegos, detén el bucle
#         if len(juegos_encontrados) == 5:
#             break

#     # Convierte la lista de juegos encontrados en un DataFrame
#     juegos_encontrados_df = pd.concat(juegos_encontrados, ignore_index=True)

#     # Imprime el DataFrame de juegos encontrados con las columnas "item_id" y "app_name"
#     juegos_encontrados = juegos_encontrados_df[['item_id', 'app_name']].to_dict(orient='records')
#     return juegos_encontrados




from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/countreviews/{Fecha}")
def conteo_reviews(Fecha_inicio,Fecha_fin: str):
    return countreviews(Fecha_inicio,Fecha_fin)

@app.get("/sentiment_analysis/{Anio}")
def Analisis_sentimiento(Año: str):
    return sentiment_analysis(Año)

@app.get("/developers_por_letra/{letra}")
def Letra_inicial(Inicial: str):
    return developers_por_letra(Inicial)

@app.get("/developer_juegos_gratis/{Nombre}")
def Juegos_gratis_developer(Nombre_Devpr: str):
    return developer_juegos_gratis(Nombre_Devpr)

@app.get("/lista_user_id")
def lista_users():
    return user_id()

@app.get("/similar_user/{user_id}")
def usuario_similar(user_id: str):
    return similar_user(user_id)
