import re

def normalizar_texto(text: str) -> str:
    """
    Normaliza un texto convirtiéndolo a minúsculas, eliminando caracteres especiales
    y reemplazando múltiples espacios por uno solo.

    Parameters
    ----------
    text : str
        Texto a normalizar.

    Returns
    -------
    str
        Texto normalizado.
    
    Ejemplo de uso:
    ---------------
        normalizar_texto("¡Hola mundo!  Este es un   ejemplo.") -> "hola mundo este es un ejemplo"
    """
    if not isinstance(text, str):
        raise ValueError("El parámetro 'text' debe ser de tipo str.")

    # Convertir a minúsculas y eliminar caracteres no deseados
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar caracteres especiales
    text = re.sub(r'\s+', ' ', text)     # Reemplazar múltiples espacios por uno

    return text.strip()  # Eliminar espacios iniciales y finales