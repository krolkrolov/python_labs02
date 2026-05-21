from interfaces import IPrintable, IComparable
from abc import ABC, abstractmethod

class Bus(IPrintable, IComparable, ABC):
    # 1. Аннотируем параметры конструктора и указываем, что он возвращает None
    def __init__(self, route_number: str, capacity: int) -> None:
        # 2. Аннотируем атрибуты прямо внутри __init__
        self._route_number: str = route_number
        self._capacity: int = capacity
        self.status: str = "в парке"

    @property
    def route_number(self) -> str: 
        return self._route_number

    @abstractmethod
    def calculate_fare(self) -> float:
        pass

    def get_comparison_value(self) -> float:
        return float(self._capacity)

    # 3. Добавлен метод для соответствия протоколу Displayable (Задание на 5)
    def display(self) -> str:
        # Так как классы-наследники уже обязаны реализовать IPrintable,
        # мы просто вызываем их реализацию
        return self.get_detailed_info()

class CityBus(Bus):
    # Указываем типы для новых параметров (bool для wifi, int для стоячих мест)
    def __init__(self, route_number: str, capacity: int, has_wifi: bool, standing_places: int) -> None:
        super().__init__(route_number, capacity)
        self.has_wifi: bool = has_wifi
        self.standing_places: int = standing_places

    # Аннотируем возвращаемое значение
    def calculate_fare(self) -> float: 
        return 40.0

    def get_detailed_info(self) -> str:
        wifi = "Есть" if self.has_wifi else "Нет"
        return f"[CITY] Маршрут: {self.route_number} | Мест: {self._capacity} | Wi-Fi: {wifi}"

class IntercityBus(Bus):
    # Указываем тип distance как float (так как дистанция может быть дробной)
    def __init__(self, route_number: str, capacity: int, distance: float, has_ac: bool) -> None:
        super().__init__(route_number, capacity)
        self.distance: float = distance
        self.has_ac: bool = has_ac

    def calculate_fare(self) -> float: 
        return self.distance * 3.5

    def get_detailed_info(self) -> str:
        ac = "Есть" if self.has_ac else "Нет"
        return f"[INTERCITY] Маршрут: {self.route_number} | Дистанция: {self.distance}км | Кондиционер: {ac}"

    def get_comparison_value(self) -> float:
        return float(self.distance)