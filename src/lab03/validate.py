def validate_route_number(route_number: str) -> str:
    if not isinstance(route_number, str):
        raise TypeError("Номер маршрута должен быть строкой.")
    if not route_number.strip():
        raise ValueError("Номер маршрута не может быть пустым.")
    return route_number.strip()

def validate_capacity(capacity: int) -> int:
    if not isinstance(capacity, int):
        raise TypeError("Вместимость должна быть целым числом.")
    if capacity <= 0:
        raise ValueError("Вместимость автобуса должна быть больше 0.")
    return capacity

def validate_passengers(passengers: int, capacity: int) -> int:
    if not isinstance(passengers, int):
        raise TypeError("Количество пассажиров должно быть целым числом.")
    if passengers < 0:
        raise ValueError("Количество пассажиров не может быть отрицательным.")
    if passengers > capacity:
        raise ValueError(f"Слишком много пассажиров! Максимальная вместимость: {capacity}.")
    return passengers