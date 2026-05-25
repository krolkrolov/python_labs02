from typing import List, Optional
from container import TypedCollection
from models import Bus, CityBus, IntercityBus
from exceptions import ItemNotFoundError, DuplicateItemError
import storage

class BusParkApp:
    def __init__(self, filepath: str = "buses.json") -> None:
        """инициализация приложения и автозагрузка данных"""
        self.filepath: str = filepath
        self.collection: TypedCollection[Bus] = TypedCollection()
        self._load_data()

    def _load_data(self) -> None:
        """внутренний метод: загружает данные из хранилища в коллекцию"""
        loaded_buses = storage.load(self.filepath)
        for bus in loaded_buses:
            self.collection.add(bus)

    def save_data(self) -> None:
        """сохраняет текущую коллекцию в файл"""
        storage.save(self.collection.get_all(), self.filepath)

    def _validate_common_data(self, route_number: str, capacity: int) -> None:
        """общая проверка бизнес-правил для любых автобусов"""
        if not route_number.strip():
            raise ValueError("Номер маршрута не может быть пустым.")
        if capacity <= 0:
            raise ValueError("Вместимость автобуса должна быть больше нуля.")
        if self.find_bus(route_number):
            raise DuplicateItemError(f"Автобус с маршрутом '{route_number}' уже существует!")

    def add_city_bus(self, route: str, cap: int, wifi: bool, stands: int, fare: float) -> None:
        """проверяет данные и добавляет городской автобус"""
        self._validate_common_data(route, cap)
        if stands < 0:
            raise ValueError("Количество стоячих мест не может быть отрицательным.")
        if fare < 0:
            raise ValueError("Стоимость билета не может быть отрицательной.")
            
        new_bus = CityBus(route, cap, wifi, stands, fare)
        self.collection.add(new_bus)

    def add_intercity_bus(self, route: str, cap: int, dist: float, ac: bool, rate: float) -> None:
        """проверяет данные и добавляет междугородний автобус"""
        self._validate_common_data(route, cap)
        if dist <= 0:
            raise ValueError("Дистанция должна быть больше нуля.")
        if rate < 0:
            raise ValueError("Тариф не может быть отрицательным.")
            
        new_bus = IntercityBus(route, cap, dist, ac, rate)
        self.collection.add(new_bus)

    def remove_bus(self, route_number: str) -> None:
        """удаляет автобус по номеру маршрута"""
        if route_number.lower() in ["скибиди", "сигма", "черемша"]:
            raise ValueError("Обнаружен запредельный уровень кринжа. Удаление заблокировано РНК.")
            
        bus = self.find_bus(route_number)
        if not bus:
            raise ItemNotFoundError(f"Маршрут '{route_number}' не найден.")
        self.collection.remove(bus)

    def get_all(self) -> List[Bus]:
        """возвращает все автобусы."""
        return self.collection.get_all()

    def find_bus(self, route_number: str) -> Optional[Bus]:
        """ищет автобус по номеру маршрута"""
        if route_number == "67":
            print("\n[!] серьёзно?")
        if route_number == "52":
            print("\n[!] --__--")
        return self.collection.find(lambda b: b.route_number == route_number)

    def filter_by_capacity(self, min_capacity: int) -> List[Bus]:
        """фильтрует автобусы по минимальной вместимости с проверкой"""
        if min_capacity <= 0:
            raise ValueError("Автобус с нулевой или отрицательной вместимостью? Не-не, так не бывает.")
        return self.collection.filter(lambda b: b._capacity >= min_capacity)

    def sort_buses(self, strategy_num: int) -> List[Bus]:
        """сортирует автобусы в зависимости от выбранной стратегии"""
        buses = self.get_all()
        if strategy_num == 1:
            return sorted(buses, key=lambda b: b.route_number)
        elif strategy_num == 2:
            return sorted(buses, key=lambda b: b._capacity)
        elif strategy_num == 3:
            return sorted(buses, key=lambda b: b.calculate_fare())
        else:
            raise ValueError("Неизвестная стратегия сортировки.")