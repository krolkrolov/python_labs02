from interfaces import IPrintable, IComparable
from abc import ABC, abstractmethod

class Bus(IPrintable, IComparable, ABC):
    # 1. аннотируем параметры конструктора и указываем, что он возвращает None
    def __init__(self, route_number: str, capacity: int) -> None:
        # 2. аннотируем атрибуты прямо внутри __init__
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

    # 3. добавлен метод для соответствия протоколу Displayable
    def display(self) -> str:
        # тк классы наследники уже обязаны реализовать IPrintable,
        # мы просто вызываем их реализацию
        return self.get_detailed_info()

class CityBus(Bus):
    
    def __init__(self, route_number: str, capacity: int, has_wifi: bool, standing_places: int, base_fare: float) -> None:
        super().__init__(route_number, capacity)
        self.has_wifi = has_wifi
        self.standing_places = standing_places
        self.base_fare = base_fare # сохранение введенной цены

    def calculate_fare(self) -> float: 
        return self.base_fare # возвращаем то, что ввел пользователь

    def get_detailed_info(self) -> str:
        wifi = "Есть" if self.has_wifi else "Нет"
        return f"[CITY] Маршрут: {self.route_number} | Мест: {self._capacity} | Wi-Fi: {wifi}"

class IntercityBus(Bus):
    
    def __init__(self, route_number: str, capacity: int, distance: float, has_ac: bool, price_per_km: float) -> None:
        super().__init__(route_number, capacity)
        self.distance = distance
        self.has_ac = has_ac
        self.price_per_km = price_per_km # сохранение ужаснейшего тарифа

    def calculate_fare(self) -> float: 
        '''расчет стоимости - налоги, инфляция и слезы иишки не учтены.'''
        return self.distance * self.price_per_km # сставим горожаней на счётчик

    def get_detailed_info(self) -> str:
        ac = "Есть" if self.has_ac else "Нет"
        return f"[INTERCITY] Маршрут: {self.route_number} | Дистанция: {self.distance}км | Кондиционер: {ac}"

    def get_comparison_value(self) -> float:
        return float(self.distance)