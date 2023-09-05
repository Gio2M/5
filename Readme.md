# Proyecto de Análisis de Reseñas y Sistema de Recomendación

Este proyecto se enfoca en el análisis de reseñas de usuarios y en la implementación de un sistema de recomendación basado en algoritmos de filtrado colaborativo. El objetivo principal es proporcionar información valiosa a los usuarios y ayudarles a descubrir nuevos juegos o aplicaciones que podrían interesarles.

## Tabla de Contenidos

- [Archivos de Datos](#archivos-de-datos)
- [Funciones de los Endpoints](#funciones-de-los-endpoints)
- [Configuración del Sistema de Recomendación](#configuración-del-sistema-de-recomendación)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Autor](#autor)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Agradecimientos](#agradecimientos)

## Archivos de Datos

En este proyecto, trabajamos con tres archivos CSV que contienen información relevante:

1. `reviews_nlp.csv`: Este archivo contiene las reseñas de usuarios, incluyendo detalles como la fecha de publicación, el usuario, el ID del artículo y la recomendación.

2. `games.csv`: Este archivo proporciona información sobre los juegos o aplicaciones, incluyendo su fecha de lanzamiento, desarrollador y otros detalles importantes.

3. `df_train_filtrado.csv`: Este archivo es utilizado para entrenar el sistema de recomendación y contiene datos de usuarios, ítems y recomendaciones.

Asegúrate de que estos archivos estén ubicados en el directorio `Data/Datos_csv` para que el código pueda acceder a ellos correctamente.

## Funciones de los Endpoints

Hemos implementado una serie de endpoints que proporcionan información y funcionalidad útiles a los usuarios:

- `/countreviews/{Fecha_inicio}/{Fecha_fin}`: Este endpoint cuenta la cantidad de usuarios únicos que realizaron reseñas en un período de tiempo específico y calcula el porcentaje de recomendación en función de las reseñas.

- `/sentiment_analysis/{Anio}`: Realiza un análisis de sentimiento en las reseñas para un año de lanzamiento específico y muestra la cantidad de reseñas por categoría de sentimiento.

- `/developers_por_letra/{letra}`: Devuelve una lista de desarrolladores cuyos nombres comienzan con una letra específica.

- `/developer_juegos_gratis/{Nombre}`: Proporciona información sobre juegos gratuitos lanzados por una empresa desarrolladora específica, incluyendo el porcentaje de juegos gratuitos en función de los años.

- `/lista_user_id`: Devuelve una lista de valores únicos de identificadores de usuario.

- `/similar_user/{user_id}`: Encuentra usuarios similares al usuario especificado y recomienda juegos que otros usuarios similares han disfrutado.

## Configuración del Sistema de Recomendación

Hemos utilizado la biblioteca Surprise para implementar el sistema de recomendación. El proceso de entrenamiento se realiza de la siguiente manera:

1. Configuramos el lector y la escala de calificación para nuestros datos.

2. Cargamos los datos del DataFrame `df_train_filtrado`, que contiene información sobre usuarios, ítems y recomendaciones.

3. Dividimos los datos en conjuntos de entrenamiento y prueba.

4. Creamos un modelo KNN (K-Nearest Neighbors) basado en similitud de usuarios.

5. Entrenamos el modelo en el conjunto de entrenamiento.

6. Implementamos una función que encuentra juegos recomendados para un usuario específico.

## Ejecución del Proyecto

Para ejecutar este proyecto, debes seguir los siguientes pasos:

1. Asegúrate de tener instaladas todas las bibliotecas necesarias. Puedes usar `pip install -r requirements.txt` para instalar las dependencias.

2. Ubica los archivos CSV en la carpeta `Data/Datos_csv` o ajusta las rutas de archivo en el código según sea necesario.

3. Ejecuta la aplicación FastAPI utilizando el comando `uvicorn main:app --reload`. La aplicación se ejecutará en `http://localhost:8000`.

4. Accede a los endpoints mencionados anteriormente en tu navegador o utilizando una herramienta como Postman.

5. Explora los resultados y la funcionalidad proporcionada por el sistema de recomendación y el análisis de reseñas.

¡Disfruta explorando y analizando los datos y recomendaciones! Si tienes alguna pregunta o problema, no dudes en ponerte en contacto con nosotros.

## Autor

Gio M

## Contacto
gio75388gmail.com

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Si deseas colaborar, no dudes en abrir un problema o enviar una solicitud de extracción.

## Licencia

Este proyecto se encuentra bajo la Licencia MIT