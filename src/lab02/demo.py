from model import Bus
from collection import BusFleet

def main():
    print("--- Сценарий 1: Базовые операции, итерация и ограничения ---")
    fleet = BusFleet("Центральный")
    
    # Создание объектов из ЛР-1
    bus1 = Bus("45А", 50)
    bus2 = Bus("12", 30)
    bus3 = Bus("101", 120)

    # Добавление (add)
    fleet.add(bus1)
    fleet.add(bus2)
    fleet.add(bus3)

    print(fleet)
    
    # Демонстрация __iter__
    for bus in fleet:
        print("  -", bus)

    # Проверка ограничений (TypeCheck и Дубликаты)
    try:
        fleet.add("Это просто строка, а не автобус")
    except TypeError as e:
        print(f"ОЖИДАЕМАЯ ОШИБКА (Тип): {e}")

    try:
        fleet.add(Bus("45А", 60)) # Автобус с таким маршрутом уже есть
    except ValueError as e:
        print(f"ОЖИДАЕМАЯ ОШИБКА (Дубликат): {e}")


    print("\n--- Сценарий 2: Индексация, поиск и удаление ---")
    # Демонстрация __getitem__
    print(f"Первый автобус в парке (fleet[0]): {fleet[0].route_number}")
    
    # Демонстрация поиска
    found_bus = fleet.find_by_route("12")
    print(f"Найден автобус по маршруту '12': Вместимость {found_bus.capacity}")

    # Демонстрация удаления по индексу (remove_at)
    removed = fleet.remove_at(1) # Удаляем "12"
    print(f"Удален автобус по индексу 1: {removed.route_number}")
    print(f"Осталось автобусов (len): {len(fleet)}")


    print("\n--- Сценарий 3: Сортировка и фильтрация (Новая коллекция) ---")
    # Добавим еще один автобус для наглядности
    fleet.add(Bus("77", 15))
    
    print("До сортировки:")
    for b in fleet: print(f"  - Маршрут {b.route_number} ({b.capacity} мест)")

    fleet.sort_by_capacity() # Сортируем по вместимости

    print("После сортировки по вместимости:")
    for b in fleet: print(f"  - Маршрут {b.route_number} ({b.capacity} мест)")

    # Меняем состояние объектов (выводим на маршрут)
    print("\nОтправляем часть автобусов на маршрут...")
    fleet[0].start_route() # Самый маленький поехал
    fleet[2].start_route() # Самый большой поехал

    # Фильтрация (возвращает новую коллекцию BusFleet)
    active_fleet = fleet.get_active_fleet()
    print(f"\nНовая коллекция: {active_fleet}")
    for bus in active_fleet:
        print("  -", bus)

if __name__ == "__main__":
    main()