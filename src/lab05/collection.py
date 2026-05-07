from models import Bus
from interfaces import IPrintable, IComparable

class BusFleet:
    def __init__(self, name: str, buses=None):
        self.name = name
        # Если список не передан, создаем пустой
        self._buses: list[Bus] = buses if buses is not None else []

    def add(self, bus: Bus):
        self._buses.append(bus)
    
    # Из лабы 4

    def get_printable_entities(self) -> list[IPrintable]:
        """возвращает только те, которые реализуют контракт IPrintable"""
        return [obj for obj in self._buses if isinstance(obj, IPrintable)]

    def get_comparable_entities(self) -> list[IComparable]:
        """возвращает только те, которые реализуют контракт IComparable"""
        return [obj for obj in self._buses if isinstance(obj, IComparable)]

    # ЗАДАНИЕ НА 4 И 5: Функциональные методы коллекции

    def filter_by(self, predicate) -> 'BusFleet':
        """
        фильтрует коллекцию, используя встроенную функцию filter().
        возвращает новую коллекцию, чтобы не мутировать исходную.
        """
        filtered_buses = list(filter(predicate, self._buses))
        return BusFleet(f"{self.name} (Filtered)", filtered_buses)

    def sort_by(self, key_func, reverse=False) -> 'BusFleet':
        """
        сортирует коллекцию, используя встроенную функцию sorted().
        """
        sorted_buses = sorted(self._buses, key=key_func, reverse=reverse)
        return BusFleet(f"{self.name} (Sorted)", sorted_buses)

    def apply(self, func) -> 'BusFleet':
        """
        применяет функцию ко всем элементам с помощью map().
        поддерживает как модификацию объектов, так и их преобразование в другие типы.
        """
        applied_buses = list(map(func, self._buses))
        return BusFleet(f"{self.name} (Applied)", applied_buses)

    # Магические методы для удобства
    
    def __iter__(self):
        return iter(self._buses)

    def __len__(self):
        return len(self._buses)