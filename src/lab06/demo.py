from models import CityBus, IntercityBus 

# Импортируем только коллекцию и TypeVar'ы с ограничениями на протоколы
from container import TypedCollection, D, F

def main():
    print("=== ЗАДАНИЕ НА 3: Базовая Generic-коллекция ===")
    # 1. Создаем строго типизированную коллекцию только для городских автобусов
    city_fleet: TypedCollection[CityBus] = TypedCollection()
    
    # Создаем объекты по твоим новым конструкторам
    bus1 = CityBus("10A", 40, has_wifi=True, standing_places=15)
    bus2 = CityBus("22B", 30, has_wifi=False, standing_places=10)
    
    city_fleet.add(bus1)
    city_fleet.add(bus2)

    # ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ ТИПОВ:
    #city_fleet.add("Это просто строка")

    print("Все элементы коллекции city_fleet:")
    for b in city_fleet.get_all():
        print(f" - Маршрут: {b.route_number}, Мест: {b._capacity}")


    print("\n=== ЗАДАНИЕ НА 4: Методы find, filter, map ===")
    # 1. Метод find
    found_bus = city_fleet.find(lambda b: b._capacity > 35)
    print(f"Найден автобус вместимостью > 35: {found_bus.route_number if found_bus else 'Не найден'}")
    
    not_found = city_fleet.find(lambda b: b._capacity > 100)
    print(f"Найден автобус вместимостью > 100: {not_found}")

    # 2. Метод filter
    small_buses = city_fleet.filter(lambda b: b._capacity <= 35)
    print(f"Автобусы с вместимостью <= 35: {[b.route_number for b in small_buses]}")

    # 3. Метод map (смена типа)
    # Было TypedCollection[CityBus], стало list[str] (список строк)
    routes: list[str] = city_fleet.map(lambda b: b.route_number)
    print(f"Список маршрутов (list[str]): {routes}")
    
    # Было TypedCollection[CityBus], стало list[float] (список чисел)
    fares: list[float] = city_fleet.map(lambda b: b.calculate_fare())
    print(f"Список стоимостей проезда (list[float]): {fares}")


    print("\n=== ЗАДАНИЕ НА 5: Структурная типизация (Protocol) ===")
    
    # Сценарий 1: Коллекция объектов, поддерживающих Displayable
    print("--- Сценарий 1: TypedCollection[D] ---")
    # Передаем D (которое ограничено протоколом Displayable)
    displayable_fleet: TypedCollection[D] = TypedCollection()
    
    # Добавляем объекты РАЗНЫХ классов. 
    # Никто из них не наследует Displayable, но у всех есть метод display().
    displayable_fleet.add(CityBus("101", 40, has_wifi=True, standing_places=20))
    displayable_fleet.add(IntercityBus("999", 50, distance=500.0, has_ac=True))
    
    for item in displayable_fleet.get_all():
        # IDE знает, что вызывать .display() — безопасно
        print(item.display())

    # Сценарий 2: Коллекция объектов, поддерживающих FareCalculable
    print("\n--- Сценарий 2: TypedCollection[F] ---")
    # Передаем F (которое ограничено протоколом FareCalculable)
    fare_fleet: TypedCollection[F] = TypedCollection()
    
    fare_fleet.add(CityBus("101", 40, has_wifi=True, standing_places=20))
    fare_fleet.add(IntercityBus("999", 50, distance=500.0, has_ac=True))

    for item in fare_fleet.get_all():
        # IDE знает, что вызывать .calculate_fare() — безопасно
        print(f"Рассчитанная стоимость для маршрута {item.route_number}: {item.calculate_fare():.2f} руб.")

if __name__ == "__main__":
    main()