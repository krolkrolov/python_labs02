# python_labs02/src/lab01/demo.py
from model import Bus

def main():
    print("=== Сценарий 1: Успешное создание и магические методы ===")
    bus1 = Bus("45А", 50)
    bus2 = Bus("45А", 50)
    bus3 = Bus("12", 30)

    print("Вывод через __str__:", bus1)
    print("Вывод через __repr__:", repr(bus1))
    print(f"bus1 == bus2: {bus1 == bus2}") # True, маршрут и вместимость совпадают
    print(f"bus1 == bus3: {bus1 == bus3}") # False

    print("\nАтрибут класса (Доступ через класс):", Bus.MAX_SPEED_LIMIT)
    print("Атрибут класса (Доступ через экземпляр):", bus1.MAX_SPEED_LIMIT)

    print("\n=== Сценарий 2: Логические состояния и бизнес-методы ===")
    # Изменение свойства через setter
    bus1.route_number = "45B"
    print(f"Маршрут изменен на: {bus1.route_number}")

    # Попытка посадить пассажиров в парке (поведение, зависящее от состояния)
    try:
        bus1.board_passengers(10)
    except RuntimeError as e:
        print("ОЖИДАЕМАЯ ОШИБКА (состояние):", e)

    # Меняем состояние: выводим на маршрут
    bus1.start_route()
    
    # Теперь посадка разрешена
    bus1.board_passengers(20)
    print(bus1)
    
    # Завершаем маршрут (сброс состояния и пассажиров)
    bus1.finish_route()
    print(bus1)

    print("\n=== Сценарий 3: Валидация данных ===")
    
    try:
        bad_bus = Bus("", 50) # Пустой маршрут
    except ValueError as e:
        print("ОЖИДАЕМАЯ ОШИБКА (пустой маршрут):", e)

    try:
        bus3.start_route()
        bus3.board_passengers(40) # 40 больше, чем вместимость (30)
    except ValueError as e:
        print("ОЖИДАЕМАЯ ОШИБКА (переполнение):", e)

if __name__ == "__main__":
    main()