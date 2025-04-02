import pandas as pd

def add_weight(row, columna, weight=3):
    """
    Concatena el texto de una columna hacia 'overview',
    multiplicando su contenido para darles más peso.

    Parameters:
    ----------
    row (pandas.Series): Fila de DataFrame con las columnas a procesar.
    columna (str): Nombre de la columna cuyo contenido se ponderará.
    weight (int): Número de veces que el texto se repetirá para aumentar su peso.

    Returns:
    ----------
    str: Texto combinado y ponderado.

    Ejemplo de uso:
    ---------------
        df['overview'] = df.apply(lambda row: add_weight(row, 'combined_companies', weight=3), axis=1)
    """
    # Verificar si 'overview' y la columna específica contienen datos válidos
    overview = row.get('overview', "")
    texto = row.get(columna, "")

    if pd.isna(texto) or not texto.strip():
        # Si el texto está vacío o es NaN, devuelve únicamente el 'overview'
        return overview

    # Ponderar el texto repitiéndolo 'weight' veces
    weighted_text = ' '.join([texto.strip()] * weight)

    # Concatenar el 'overview' con el texto ponderado
    return f"{overview.strip()} {weighted_text}"