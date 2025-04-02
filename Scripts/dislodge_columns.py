import pandas as pd
from pandas import DataFrame

def desanidar_columna(
    df: DataFrame,
    columna: str,
    nombre_nueva_tabla: str,
    indice_increment: int = 0
) -> DataFrame:
    """
    Desanida una columna de un DataFrame y genera un ID único que relaciona
    la tabla original con el DataFrame desanidado.

    Antes de aplicar esta función, asegúrate de transformar los datos de la columna
    usando `convert_list_dict()` o una función similar, y verifica que el tipo de dato
    de la columna sea `list` o `dict`.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame original que contiene la columna a desanidar.
    columna : str
        Nombre de la columna en el DataFrame a desanidar. Debe contener listas o diccionarios.
    nombre_nueva_tabla : str
        Nombre de la tabla resultante con los datos desanidados.
    indice_increment : int, opcional
        Valor a sumar al índice para crear IDs únicos (por defecto es 0).

    Returns
    -------
    pandas.DataFrame
        Nuevo DataFrame desanidado con un ID único para relacionar las tablas.

    Ejemplo de uso:
    ---------------
        nueva_tabla = desanidar_columna(df, 'genres', 'genres_desanidado')
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")

    # Crear un ID único en el DataFrame original
    df[f'{columna}_id'] = df.index + indice_increment

    # Explode para desanidar la columna que contiene listas o diccionarios
    df_exploded = df.explode(columna)

    # Normalizar los datos de la columna desanidada
    try:
        nombre_nueva_tabla = pd.json_normalize(df_exploded[columna])
    except ValueError as e:
        raise ValueError(f"Error al normalizar la columna '{columna}'. Verifica que los datos sean válidos.\n{e}")

    # Asignar el ID único para relacionar las tablas
    nombre_nueva_tabla[f'{columna}_id'] = df_exploded[f'{columna}_id'].values

    return nombre_nueva_tabla