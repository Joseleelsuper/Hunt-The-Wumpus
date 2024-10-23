def manhattan_distance(x1: int, y1: int, x2: int, y2: int):
    """
    Calcula la distancia de Manhattan entre dos puntos.

    Args:
        x1 (int): Coordenada x del primer punto.
        y1 (int): Coordenada y del primer punto.
        x2 (int): Coordenada x del segundo punto.
        y2 (int): Coordenada y del segundo punto.

    Returns:
        int: Distancia de Manhattan entre los dos puntos.
    """
    return abs(x1 - x2) + abs(y1 - y2)


def get_move_direction(from_pos: tuple, to_pos: tuple):
    """
    Devuelve la dirección de un movimiento entre dos posiciones.

    Args:
        from_pos (tuple): Posición de origen (x, y).
        to_pos (tuple): Posición de destino (x, y).

    Returns:
        str: Dirección del movimiento
    """
    dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
    if dx == -1:
        return "up"
    elif dx == 1:
        return "down"
    elif dy == -1:
        return "left"
    elif dy == 1:
        return "right"

def get_agent_moves():
    """
    Devuelve las direcciones en las que el agente puede moverse.

    Returns:
        list: Lista de direcciones pos
    """
    return ["up", "down", "left", "right"]