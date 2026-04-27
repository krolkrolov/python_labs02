from models import Bus
from interfaces import IPrintable, IComparable

class BusFleet:
    def __init__(self, name: str):
        self.name = name
        self._buses: list[Bus] = []

    def add(self, bus: Bus):
        """Добавление любого автобуса в парк"""
        self._buses.append(bus)

    # НА 5: Фильтрация по интерфейсу

    def get_printable_entities(self) -> list[IPrintable]:
        """возвращает только те, которые реализуют контракт IPrintable"""
        return [obj for obj in self._buses if isinstance(obj, IPrintable)]

    def get_comparable_entities(self) -> list[IComparable]:
        """возвращает только те, которые реализуют контракт IComparable"""
        return [obj for obj in self._buses if isinstance(obj, IComparable)]

    # НА 5: архитектурное поведение через интерфейс

    def sort_by_interface_value(self):
        """
        Универсальная сортировка. 
        не важно, CityBus или IntercityBus.
        работаем только с контрактом IComparable.
        """
        # получаем список тех, кто умеет сравниваться
        comparable_items = self.get_comparable_entities()
        
        # сортируем список, используя метод интерфейса
        # reverse=True чтобы в топе были самые мощные (по местам или км)
        comparable_items.sort(key=lambda x: x.get_comparison_value(), reverse=True)
        return comparable_items

    def __iter__(self):
        return iter(self._buses)