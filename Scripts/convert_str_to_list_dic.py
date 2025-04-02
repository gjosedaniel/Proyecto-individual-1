import pandas as pd
import ast

def convert_list_dict(value: any) -> dict | list | None:
    """
    Convierte posibles diccionarios o listas de diccionarios en formato str a su forma real (dict o list).
    Si el valor es NaN, devuelve None. Si el valor ya es un diccionario o lista, lo devuelve sin cambios.

    Parameters
    ----------
    value : any
        El valor a verificar y convertir. Puede ser str, dict, list o NaN.

    Returns
    -------
    dict | list | None
        dict o list si la conversión es exitosa, None si el valor ya era NaN,
        o el valor original si no necesita conversión.

    Ejemplo de uso:
    ---------------
        convert_list_dict("{'id': 1, 'name': 'example'}") -> {'id': 1, 'name': 'example'}
        convert_list_dict("[{'id': 1, 'name': 'example'}, {'id': 2, 'name': 'test'}]") -> [{'id': 1, 'name': 'example'}, {'id': 2, 'name': 'test'}]
        convert_list_dict(None) -> None
    """
    if pd.isna(value):  # Verificar si es NaN
        return None

    if isinstance(value, str): 
        try:
            # Reemplazar 'Null' por 'None' para que sea un valor válido en Python
            cleaned_value = value.replace('Null', 'None')

            # Convertir el str a su forma correspondiente (dict o list)
            return ast.literal_eval(cleaned_value)
        except (ValueError, SyntaxError) as e:
            # Mostrar un mensaje de advertencia para depuración
            print(f"Advertencia: No se pudo convertir el valor: {value}\nError: {e}")
            return value  # Devolver el valor original en caso de error

    return value  # Si ya es un dict o list, devolverlo sin cambios