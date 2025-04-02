import os
from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Obtener la ruta absoluta del directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Cargar datos y modelos necesarios
def load_data():
    data_dir = os.path.join(BASE_DIR, 'Data')
    return {
        "movies": pd.read_parquet(os.path.join(data_dir, "movies_dataset_etl.parquet")),
        "credits_cast": pd.read_parquet(os.path.join(data_dir, "cast_desanidado.parquet")),
        "credits_crew": pd.read_parquet(os.path.join(data_dir, "crew_desanidado.parquet")),
        "modelo": pd.read_parquet(os.path.join(data_dir, "modelo_dataset.parquet")),
        "vectorizer": joblib.load(os.path.join(data_dir, "vectorizer.pkl")),
        "matriz_reducida": joblib.load(os.path.join(data_dir, "matriz_reducida.pkl"))
    }

data = load_data()

# Diccionarios para mapeo
MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

DIAS = {
    "lunes": 0, "martes": 1, "miercoles": 2, "jueves": 3,
    "viernes": 4, "sabado": 5, "domingo": 6
}

# Función auxiliar para verificar entradas
def validate_input(input_value, valid_dict, tipo):
    input_value = input_value.lower()
    if input_value not in valid_dict:
        raise HTTPException(status_code=400, detail=f"{tipo.capitalize()} no válido. Por favor, introduce un {tipo} en español válido.")
    return valid_dict[input_value]

# Rutas
@app.get("/")
async def root():
    return {"message": "/docs/ para ver la documentación de la API."}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    numero_mes = validate_input(mes, MESES, "mes")
    cantidad = data["movies"][data["movies"]['release_date'].dt.month == numero_mes].shape[0]
    return {"cantidad": f"{cantidad} películas fueron estrenadas en {mes.capitalize()}."}

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    numero_dia = validate_input(dia, DIAS, "día")
    cantidad = data["movies"][data["movies"]['release_date'].dt.dayofweek == numero_dia].shape[0]
    return {"cantidad": f"{cantidad} películas fueron estrenadas los días {dia.capitalize()}."}

@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    pelicula = data["movies"][data["movies"]['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró la película '{titulo}'.")
    anio = pelicula['release_year'].iloc[0]
    score = pelicula['popularity'].iloc[0]
    return {"titulo": titulo, "año": anio, "popularidad": score}

@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    pelicula = data["movies"][data["movies"]['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró la película '{titulo}'.")
    votos = pelicula['vote_count'].iloc[0]
    if votos < 2000:
        return {"message": "La película tiene menos de 2000 votos."}
    promedio = pelicula['vote_average'].iloc[0]
    return {"titulo": titulo, "votos": votos, "promedio": promedio}

@app.get("/obtener_actor/{actor}")
async def get_actor(actor: str):
    actor_films = data["credits_cast"][data["credits_cast"]['name'].str.lower() == actor.lower()]
    if actor_films.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró al actor '{actor}'.")
    ids_peliculas = actor_films['id_df'].unique()
    peliculas = data["movies"][data["movies"]['id'].isin(ids_peliculas)]
    retorno = round(peliculas['return'].sum(), 2)
    promedio = round(peliculas['return'].mean(), 2)
    return {"actor": actor, "cantidad_peliculas": len(ids_peliculas), "retorno_total": retorno, "promedio_retorno": promedio}

@app.get("/obetener_director/{director}")
async def get_director(director: str):
    director_films = data["credits_crew"][data["credits_crew"]['name'].str.lower() == director.lower()]
    if director_films.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró al director '{director}'.")
    ids_peliculas = director_films['id_df'].unique()
    peliculas = data["movies"][data["movies"]['id'].isin(ids_peliculas)]
    retorno = round(peliculas['return'].sum(), 2)
    listado_peliculas = [
        {
            "titulo": row['title'],
            "fecha_estreno": row['release_year'],
            "costo": row['budget'],
            "ganancia": row['revenue'],
            "retorno": row['return']
        }
        for _, row in peliculas.iterrows()
    ]
    return {"director": director, "retorno_total": retorno, "peliculas": listado_peliculas}

@app.get("/recomendacion/{titulo}")
async def recomendacion(titulo: str):
    titulo = titulo.lower()
    idx = data["modelo"].index[data["modelo"]['title'].str.lower() == titulo].tolist()
    if not idx:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    idx = idx[0]
    sim_scores = cosine_similarity(data["matriz_reducida"][idx].reshape(1, -1), data["matriz_reducida"])
    sim_scores = sorted(list(enumerate(sim_scores[0])), key=lambda x: x[1], reverse=True)[1:6]
    indices = [i[0] for i in sim_scores]
    recomendaciones = data["modelo"]['title'].iloc[indices].tolist()
    return {"titulo": titulo, "recomendaciones": recomendaciones}