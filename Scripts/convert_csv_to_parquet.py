import pandas as pd

# Asegúrate de tener instaladas las librerías necesarias del archivo requirements.txt.
def convertir_csv_a_parquet(
    csv_path: str,
    parquet_path: str,
    columns_to_drop: list = None,
    dtype_conversion: dict = None,
    fillna_values: dict = None
) -> None:
    """
    Convierte un archivo CSV a formato Parquet, permitiendo eliminar columnas,
    especificar tipos de datos y rellenar valores nulos.

    Parameters:
    -----------
    csv_path : str
        Ruta del archivo CSV.
    parquet_path : str
        Ruta donde se guardará el archivo Parquet.
    columns_to_drop : list, opcional
        Lista de columnas a eliminar del dataset.
    dtype_conversion : dict, opcional
        Diccionario para convertir tipos de datos: {columna: tipo}.
    fillna_values : dict, opcional
        Diccionario para rellenar valores nulos: {columna: valor}.
    
    Returns:
    --------
    None
    """
    # Leer el archivo CSV
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: El archivo '{csv_path}' no se encontró.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo '{csv_path}' está vacío.")
        return

    # Eliminar columnas si se especifica
    if columns_to_drop:
        missing_columns = [col for col in columns_to_drop if col not in df.columns]
        if missing_columns:
            print(f"Advertencia: Las columnas {missing_columns} no existen en el DataFrame.")
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    # Rellenar valores nulos si se especifica
    if fillna_values:
        for column, value in fillna_values.items():
            if column in df.columns:
                df[column].fillna(value=value, inplace=True)

    # Convertir tipos de datos si se especifica
    if dtype_conversion:
        for column, dtype in dtype_conversion.items():
            if column in df.columns:
                try:
                    df[column] = df[column].astype(dtype)
                except (ValueError, TypeError):
                    print(f"Advertencia: No se pudo convertir la columna '{column}' al tipo '{dtype}'.")
                    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Guardar como Parquet
    try:
        df.to_parquet(parquet_path, engine='pyarrow', compression='snappy', index=False)
        print(f"Archivo convertido correctamente y guardado en: {parquet_path}")
    except Exception as e:
        print(f"Error al guardar el archivo Parquet: {e}")