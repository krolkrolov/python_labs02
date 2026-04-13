from base import Bus

class BusFleet:
    def __init__(self, name: str):
        self.name = name
        self._items = []  # Внутри контейнера хранить список объектов

    # Базовые методы

    def add(self, bus: Bus):
        """Добавление объекта с проверкой типа и ограничением на дубликаты."""
        # Проверка типа добавляемых объектов
        if not isinstance(bus, Bus):
            raise TypeError("В парк можно добавлять только объекты класса Bus.")
        
        # Ограничение на добавление (нельзя добавить дубликат маршрута)
        if any(item.route_number == bus.route_number for item in self._items):
            raise ValueError(f"Ошибка: Автобус с маршрутом {bus.route_number} уже числится в парке.")
        
        self._items.append(bus)

    def remove(self, bus: Bus):
        """Удаление объекта."""
        if bus in self._items:
            self._items.remove(bus)
        else:
            raise ValueError("Такого автобуса нет в парке.")

    def get_all(self) -> list:
        """Вернуть список всех объектов."""
        return self._items

    # Поиск и магические методы

    def find_by_route(self, route_number: str) -> Bus:
        """Поиск по одному из атрибутов."""
        for bus in self._items:
            if bus.route_number == route_number:
                return bus
        return None

    def __len__(self) -> int:
        """Поддержка len(collection)."""
        return len(self._items)

    def __iter__(self):
        """Поддержка цикла for item in collection."""
        return iter(self._items)

    # Индексация, сортировка и фильтрация

    def __getitem__(self, index: int) -> Bus:
        """Поддержка индексации collection[0]."""
        return self._items[index]

    def remove_at(self, index: int):
        """Удаление по индексу."""
        if 0 <= index < len(self._items):
            removed_bus = self._items.pop(index)
            return removed_bus
        raise IndexError("Ошибка: Индекс вне диапазона коллекции./")

    def sort_by_capacity(self, reverse: bool = False):
        """Сортировка объектов по вместимости."""
        self._items.sort(key=lambda bus: bus.capacity, reverse=reverse)

    def get_active_fleet(self) -> 'BusFleet':
        """
        Логическая операция: возвращает НОВУЮ коллекцию 
        только с теми автобусами, которые сейчас на маршруте.
        """
        active_fleet = BusFleet(f"{self.name} (На линии)")
        for bus in self._items:
            if bus.is_on_route:
                active_fleet.add(bus)
        return active_fleet

    def __str__(self) -> str:
        return f"Автобусный парк '{self.name}' | Всего автобусов: {len(self)}"