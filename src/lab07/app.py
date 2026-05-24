# модуль бизнес логики. управляет коллекцией и связывает интерфейс с данными.


from typing import List, Optional, Callable
from container import TypedCollection
from models import Bus
from exceptions import ItemNotFoundError, DuplicateItemError
import storage as storage

class BusParkApp:
    def __init__(self, filepath: str = "buses.json") -> None:
        """иниц. приложения и автозагрузка данных."""
        self.filepath: str = filepath
        self.collection: TypedCollection[Bus] = TypedCollection()
        self._load_data()

    def _load_data(self) -> None:
        """внутренний метод: загружает данные из хранилища в коллекцию."""
        loaded_buses = storage.load(self.filepath)
        for bus in loaded_buses:
            self.collection.add(bus)

    def save_data(self) -> None:
        """сохраняет текущую коллекцию в файл."""
        storage.save(self.collection.get_all(), self.filepath)

    def add_bus(self, bus: Bus) -> None:
        """добавляет автобус. если маршрут уже есть то вызывает ошибку."""
        existing = self.find_bus(bus.route_number)
        if existing:
            raise DuplicateItemError(f"Автобус с маршрутом {bus.route_number} уже существует!")
        self.collection.add(bus)

    def remove_bus(self, route_number: str) -> None:
        """удаляет автобус по номеру маршрута."""
        bus = self.find_bus(route_number)
        if not bus:
            raise ItemNotFoundError(f"Маршрут {route_number} не найден.")
        self.collection.remove(bus)

    def get_all(self) -> List[Bus]:
        """возвращает все автобусы."""
        return self.collection.get_all()

    def find_bus(self, route_number: str) -> Optional[Bus]:
        """ищет автобус по номеру маршрута + пасхалка."""
        if route_number == "67":
            print("\n[!] серьёзно? 676767676767")
        if route_number == "52":
            print("\n[!] --__--")
        return self.collection.find(lambda b: b.route_number == route_number)

    def filter_by_capacity(self, min_capacity: int) -> List[Bus]:
        """фильтрует автобусы по минимальной вместимости."""
        return self.collection.filter(lambda b: b._capacity >= min_capacity)

    def sort_buses(self, strategy_num: int) -> List[Bus]:
        """сортирует автобусы в зависимости от выбранной стратегии."""
        buses = self.get_all()
        if strategy_num == 1:
            # по маршруту
            return sorted(buses, key=lambda b: b.route_number)
        elif strategy_num == 2:
            # по вместимости
            return sorted(buses, key=lambda b: b._capacity)
        elif strategy_num == 3:
            # по стоимости проезда (метод из протокола FareCalculable)
            return sorted(buses, key=lambda b: b.calculate_fare())
        return buses