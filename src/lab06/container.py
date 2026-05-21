from typing import TypeVar, Generic, Callable, Optional, Protocol

# TypeVar для базовой типизации коллекции
T = TypeVar('T')
# TypeVar для возвращаемого значения метода map()
R = TypeVar('R')

# ЗАДАНИЕ НА 5: ПРОТОКОЛЫ

class Displayable(Protocol):
    def display(self) -> str:
        ...

class FareCalculable(Protocol):
    def calculate_fare(self) -> float:
        ...

# TypeVar с ограничениями (bound) на протоколы
D = TypeVar('D', bound=Displayable)
F = TypeVar('F', bound=FareCalculable)

# ЗАДАНИЕ НА 3 и 4: GENERIC КОЛЛЕКЦИЯ

class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    # Задание на 3: Базовые методы
    def add(self, item: T) -> None:
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def get_all(self) -> list[T]:
        return list(self._items)

    # Задание на 4: Методы высшего порядка
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Возвращает первый элемент, удовлетворяющий условию, или None"""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Возвращает список всех подходящих элементов"""
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        """Применяет функцию ко всем элементам и возвращает список результатов типа R"""
        return [transform(item) for item in self._items]