#исключения для предметной области.

class ItemNotFoundError(Exception):
    """исключение: объект не найден в коллекции."""
    pass

class DuplicateItemError(Exception):
    """Когда два автобуса пытаются занять один маршрут (Должен остаться только один)."""
    pass