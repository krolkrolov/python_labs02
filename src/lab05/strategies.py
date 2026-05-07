"""
Модуль этот
содержит функции высшего порядка, лямбды и callable-объекты (паттерн Стратегия)
для обработки объектов автобусов.
"""

from models import CityBus, IntercityBus

# 1) СТРАТЕГИИ СОРТИРОВКИ на 3

def by_route(bus):
    """Стратегия: сортировка по номеру маршрута (алфавитный порядок)"""
    return bus.route_number

def by_capacity(bus):
    """Стратегия: сортировка по вместимости (числовой атрибут)"""
    return bus._capacity

def by_fare_and_capacity(bus):
    """Стратегия: сортировка по стоимости, а при равенстве — по вместимости"""
    return (bus.calculate_fare(), bus._capacity)


# 2) СТРАТЕГИИ ФИЛЬТРАЦИИ на 3

def is_city_bus(bus):
    """Фильтр: пропускает только городские автобусы"""
    return isinstance(bus, CityBus)

def is_profitable(bus):
    """Фильтр: пропускает автобусы, где тариф выше 100"""
    return bus.calculate_fare() > 100


# 3) ФАБРИКА ФУНКЦИЙ на 4

def make_capacity_filter(min_capacity: int):
    """
    фабрика функций. Создает и возвращает функцию-фильтр
    с заранее заданным параметром минимальной вместимости (замыкание).
    """
    def filter_fn(bus):
        return bus._capacity >= min_capacity
    return filter_fn


# 4) CALLABLE-ОБЪЕКТЫ/ПАТТЕРН СТРАТЕГИЯ на 5

class StatusUpdateStrategy:
    """
    паттерн Стратегия. Callable-объект, обновляющий статус автобуса.
    взаимозаменяем с любой другой функцией преобразования.
    """
    def __init__(self, new_status: str):
        self.new_status = new_status

    def __call__(self, bus):
        # Добавляем или обновляем атрибут status у автобуса
        bus.status = self.new_status
        return bus

class DictTransformStrategy:
    """
    стратегия: превращает объект автобуса в словарь (для выгрузки в JSON/API).
    """
    def __call__(self, bus):
        return {
            "route": bus.route_number,
            "fare": bus.calculate_fare(),
            "type": bus.__class__.__name__
        }