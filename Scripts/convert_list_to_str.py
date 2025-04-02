def lista_a_str(val: any) -> str:
    """
    Convierte una lista en un string. Si el valor no es una lista, retorna su valor original.

    Parameters
    ----------
    val : any
        El valor a evaluar. Si es una lista, se convertirá en un string; de lo contrario, se devolverá tal cual.

    Returns
    -------
    str
        Si el valor es una lista, retorna un string. De lo contrario, devuelve el valor original sin modificar.

    Ejemplo de uso:
    ---------------
        lista_a_str([1, 2, 3]) -> '[1, 2, 3]'
        lista_a_str("texto") -> 'texto'
    """
    return str(val) if isinstance(val, list) else val