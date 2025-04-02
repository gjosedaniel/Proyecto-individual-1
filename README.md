# Proyecto: API de Recomendación de Películas

## Descripción
Este repositorio contiene el desarrollo de una API diseñada para integrarse con servicios de streaming, ofreciendo funcionalidades como la recomendación de películas y la obtención de información sobre actores y directores, junto con la cantidad de películas en las que han participado.

El proyecto emplea un enfoque integral de **Data Engineering** y **Data Science**, combinando un modelo de Machine Learning que recomienda películas basándose en la similitud entre ellas. Para ello, se utilizan técnicas de procesamiento de lenguaje natural (NLP), específicamente la similitud del coseno, y un exhaustivo análisis estadístico mediante librerías avanzadas de Python.

### **Objetivo Principal**
Desplegar un sistema eficiente de recomendaciones en la plataforma **Render**, optimizado para su funcionamiento en el plan gratuito. Este sistema está diseñado para procesar y analizar grandes volúmenes de datos de forma efectiva, brindando recomendaciones personalizadas y actualizadas en tiempo real.

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Instalación y Requisitos](#instalación-y-requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Uso y Ejecución](#uso-y-ejecución)
5. [Datos y Fuentes](#datos-y-fuentes)
6. [Metodología](#metodología)
7. [Creación de las Funciones en la API](#creación-de-las-funciones-en-la-api)
8. [Despliegue](#despliegue)
9. [Resultados](#resultados-y-links-al-proyecto)
10. [Autor](#autor)

---

## **Instalación y Requisitos**

Para ejecutar este proyecto, necesitas tener instalado:

- **Python 3.11**.
- **Datasets en formato CSV sin procesar**:
  - [`movies_dataset.csv`](#).
  - [`credits.csv`](#).
- Librerías necesarias (consultar `requirements.txt`).

### **Pasos de Instalación**

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git

2. Navega al directorio del proyecto:

cd tu_proyecto

3. Crea un entorno virtual (recomendado):

python -m venv tu_entorno

4. Activa el entorno virtual:

    - En Windows:

    `tu_entorno\Scripts\activate`

    - En macOS/Linux:
    
    `source tu_entorno/bin/activate`

5. Crea un archivo  y excluye archivos innecesarios:

touch .gitignore

Dentro de  agrega:

### Ignorar la carpeta de datos crudos
Datasets/

### Ignorar el entorno virtual
tu_entorno/

6. Instala las dependencias:

pip install -r requirements.txt

# Estructura del Proyecto
## La estructura del proyecto es la siguiente:

├── app/
│   └── main.py    # Archivo principal de la API.
├── data/
│   ├── raw/       # Archivos de datos sin procesar.
│   ├── processed/ # Datos procesados listos para consumir.
├── notebooks/
│   ├── etl_movies_dataset.ipynb
│   ├── etl_credits.ipynb
│   ├── eda.ipynb
│   ├── model_test.ipynb
├── scripts/
│   ├── convert_csv_to_parquet.py
│   ├── convert_str_to_list.py
│   ├── desanidar_columnas.py
├── requirements.txt # Dependencias del proyecto.
├── README.md        # Documentación del proyecto.
└── runtime.txt      # Versión de Python para Render.

# Uso y Ejecución

1. Coloca los archivos de datos crudos en el directorio Datasets/:
    - movies_dataset.csv
    - credits.csv

2. Ejecuta el notebook /etl_movies_dataset.ipynb:
    - Convierte el archivo CSV a formato Parquet.
    - Aplica transformaciones y guarda los datos en Data/.

3. Ejecuta el notebook etl_credits.ipynb:
    - Realiza las mismas acciones para el archivo credits.csv y guarda los resultados en Data/.

4. Ejecuta el notebook eda.ipynb:
    - Analiza los datos y los prepara para el modelo de recomendación.

5. Ejecuta el notebook model.ipynb:
    - Entrena el modelo de recomendación y guarda el modelo entrenado en formato .plk.

6. Inicia la API utilizando:

uvicorn app.main:app --host 0.0.0.0 --port 10000

## Datos y Fuentes
- Datasets: Los datos se encuentran en la carpeta **Datasets** y necesitan ser procesados.

## Metodología

### Optimización de Recursos

- Conversión de CSV a Parquet para mejorar el rendimiento.
- Eliminación de valores nulos, duplicados y columnas no relevantes.

### Análisis Exploratorio de Datos (EDA)

- Relleno de valores faltantes con la mediana.
- Visualización de datos mediante gráficos.
- Transformación logarítmica para manejar outliers.

### Modelado del Sistema de Recomendación

- TF-IDF para vectorizar texto.
- Reducción dimensional con TruncatedSVD.
- Similitud del coseno para generar recomendaciones.

## Creación de las Funciones en la API

### Ejemplo de rutas en Main.py:

/recomendaciones/{titulo}: Recomienda películas similares al título ingresado.
/votos_titulo/{titulo}: Devuelve los votos recibidos y el promedio de calificaciones.

Las funciones consultan los DataFrames procesados y devuelven respuestas en formato JSON.

## Despliegue

### Pasos en Render:
1. Crea una cuenta en Render y conecta tu repositorio.
2. Define el comando de inicio.

uvicorn app.main:app --host 0.0.0.0 --port 10000

3. Consulta la documentación oficial para mayor asistencia.

## Autor
Proyecto desarrollado por José Daniel Giménez. ¡Espero tus comentarios y sugerencias!