from interfaces import IPrintable, IComparable
from abc import ABC, abstractmethod

# базовый класс теперь тоже абстрактный (ABC)
class Bus(IPrintable, IComparable, ABC):
    def __init__(self, route_number: str, capacity: int):
        self._route_number = route_number
        self._capacity = capacity
        self.status = "в парке"

    @property
    def route_number(self): return self._route_number

    # абстрактный метод из 3 лабы остается
    @abstractmethod
    def calculate_fare(self) -> float:
        pass

    # реализация IComparable: по умолчанию сравниваем по вместимости
    def get_comparison_value(self) -> float:
        return float(self._capacity)

class CityBus(Bus):
    def __init__(self, route_number, capacity, has_wifi, standing_places):
        super().__init__(route_number, capacity)
        self.has_wifi = has_wifi
        self.standing_places = standing_places

    def calculate_fare(self): return 40.0

    # Реализация IPrintable
    def get_detailed_info(self) -> str:
        wifi = "Есть" if self.has_wifi else "Нет"
        return f"[CITY] Маршрут: {self.route_number} | Мест: {self._capacity} | Wi-Fi: {wifi}"

class IntercityBus(Bus):
    def __init__(self, route_number, capacity, distance, has_ac):
        super().__init__(route_number, capacity)
        self.distance = distance
        self.has_ac = has_ac

    def calculate_fare(self): return self.distance * 3.5

    # реализация IPrintable
    def get_detailed_info(self) -> str:
        ac = "Есть" if self.has_ac else "Нет"
        return f"[INTERCITY] Маршрут: {self.route_number} | Дистанция: {self.distance}км | Кондиционер: {ac}"

    # переопределяю сравнение: межгород важнее по дистанции, а не по местам
    def get_comparison_value(self) -> float:
        return float(self.distance)