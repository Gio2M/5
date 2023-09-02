import pandas as pd

"""Se indican los archivos con los que se va a trabajar
"""

# Se especifican las rutas de los archivos CSV conque se van a trabajar
file_path = 'Data/Datos_csv/reviews_nlp.csv'
file_path1 = 'Data/Datos_csv/games.csv'

# Se leen los archivos CSV y crean los DataFrame
reviews_nlp = pd.read_csv(file_path, parse_dates= ['posted'])
games = pd.read_csv(file_path1, parse_dates= ['release_date'])


"""
Se crean las funciones para los endpoints
"""


def countreviews(start_date, end_date):
    # Filtrar las filas del DataFrame entre las fechas dadas
    filtered_reviews = reviews_nlp[(reviews_nlp['posted'] >= start_date) & (reviews_nlp['posted'] <= end_date)]
    
    # Contar la cantidad de usuarios únicos que realizaron reviews en el período dado
    unique_users_count = filtered_reviews['user_id'].nunique()
    
    # Calcular el porcentaje de recomendación basado en la columna "recommend"
    recommend_percentage = (filtered_reviews['recommend'].sum() / len(filtered_reviews)) * 100
    
    return unique_users_count, recommend_percentage

# Definir las fechas de inicio y fin en formato "YYYY-MM-DD"
start_date = '2015-1-1'
end_date = '2015-12-30'

# Llamar a la función para obtener los resultados
users_count, recommend_percentage = countreviews(start_date, end_date)

# Imprimir los resultados
print(f"Cantidad de usuarios que realizaron reviews entre {start_date} y {end_date}: {users_count}")
print(f"Porcentaje de recomendación en base a recommend: {recommend_percentage:.2f}%")



def sentiment_analysis(date_str):
    # Convierte la cadena de fecha de entrada a un objeto datetime
    target_date = pd.to_datetime(date_str)
    
    # Filtra las reseñas que coincidan con el año objetivo
    filtered_reviews = reviews_nlp[reviews_nlp['posted'].dt.year == target_date.year]
    
    # Realiza el conteo de las categorías de sentimiento
    sentiment_counts = filtered_reviews['sentiment_analysis'].value_counts()
    
    # Crea una lista con los recuentos de categorías
    result_list = f'Negative = {sentiment_counts.get(0, 0)}, Neutral = {sentiment_counts.get(1, 0)}, Positive = {sentiment_counts.get(2, 0)}'
    
    return result_list

# Ejemplo de uso: Obtener el análisis de sentimientos para el año 2018
result = sentiment_analysis('2011-12-30')
print(result)



def developers_por_letra(letra):

    # Filtrar los desarrolladores cuyos nombres comienzan con la letra especificada
    filtered_developers = games[games['developer'].str.startswith(letra, na=False)]['developer'].unique()
    
    return list(filtered_developers)

# # Ejemplo de uso: Obtener desarrolladores cuyos nombres comienzan con la letra 'A'
# letra = 'b'
# developers_con_A = developers_por_letra(letra)

# print(f'Desarrolladores cuyos nombres comienzan con la letra "{letra}":')
# for developer in developers_con_A:
#     print(developer)



def developer(empresa_desarrolladora: str):
    # Filtra el DataFrame para obtener solo las filas de la empresa desarrolladora especificada
    developer_df = games[games['developer'] == empresa_desarrolladora]
    
    # Agrupa por año y cuenta la cantidad de juegos lanzados en cada año
    games_by_year = developer_df.groupby(developer_df['release_date'].dt.year)['id'].count()
    
    # Cuenta la cantidad de juegos gratuitos lanzados en cada año
    free_games_by_year = developer_df[developer_df['price'] == 'Free To Play'].groupby(developer_df['release_date'].dt.year)['id'].count()
    
    # Calcula el porcentaje de juegos gratuitos por año
    percentage_free_by_year = (free_games_by_year / games_by_year * 100).fillna(0)
    
    return percentage_free_by_year
    # #Imprime el resultado
    # print(f'{empresa_desarrolladora}\n')
    # print('Año\tContenido Contenido Free')
    # for year, percentage in percentage_free_by_year.items():
    #     total_games = games_by_year.get(year, 0)
    #     print(f'{year}\t{total_games}\t{percentage:.1f}%')

    # # Llama a la función con el nombre de la empresa desarrolladora que deseas analizar
    # developer('Ubisoft')



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
    return developer(Nombre_Devpr)



class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

@app.get("/libros/{id}")
def mostrar_libros(id: int):
    return {"data": id}

@app.post("/libros")
def insertar_libro(obra:Libro):
    return {"mensaje":f"libro {obra.titulo} insertado"}