from abc import ABC, abstractmethod

# интерфейс 1: для объектов которые можно детально вывести в консоль
class IPrintable(ABC):
    @abstractmethod
    def get_detailed_info(self) -> str:
        """должен вернуть строку с полным описанием объекта"""
        pass

# интерфейс 2: для объектов которые можно сравнивать (например, по весу или значимости)
class IComparable(ABC):
    @abstractmethod
    def get_comparison_value(self) -> float:
        """должен вернуть числовое значение для сравнения объектов"""
        pass