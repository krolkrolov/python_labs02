from models import CityBus, IntercityBus
from collection import BusFleet
from strategies import (
    by_route, by_capacity, by_fare_and_capacity,
    is_city_bus, is_profitable, make_capacity_filter,
    StatusUpdateStrategy, DictTransformStrategy
)

def print_fleet(fleet, title=""):
    print(f"\n--- {title} ---")
    for item in fleet:
        # Проверяем, является ли объект словарем (после DictTransformStrategy)
        if isinstance(item, dict):
            print(item)
        else:
            status = getattr(item, 'status', 'В парке')
            print(f"[{item.__class__.__name__}] Маршрут: {item.route_number} | Мест: {item._capacity} | Статус: {status}")

def main():
    # 1. Создание коллекции объектов (минимум 5 штук)
    fleet = BusFleet("Центральное депо")
    fleet.add(CityBus("10A", capacity=40, has_wifi=True, standing_places=20))
    fleet.add(IntercityBus("M-100", capacity=45, distance=300, has_ac=True))
    fleet.add(CityBus("5", capacity=120, has_wifi=False, standing_places=60)) # Гармошка
    fleet.add(IntercityBus("M-200", capacity=30, distance=800, has_ac=True))
    fleet.add(CityBus("77", capacity=25, has_wifi=True, standing_places=10))  # Маршрутка

    print_fleet(fleet, "ИСХОДНЫЙ АВТОПАРК")

    # ДЕМОНСТРАЦИЯ ЗАДАНИЙ НА 3 И 4 (Изолированные вызовы и lambda
    
    # Сортировка 3 разными стратегиями
    print_fleet(fleet.sort_by(by_route), "СОРТИРОВКА: По маршруту (by_route)")
    print_fleet(fleet.sort_by(by_fare_and_capacity), "СОРТИРОВКА: По тарифу и местам")
    # Сортировка через LAMBDA (Задание 4)
    print_fleet(fleet.sort_by(lambda x: x._capacity, reverse=True), "СОРТИРОВКА (lambda): По убыванию мест")

    # Сравнение lambda и именованной функции (Задание 4)
    res_named = fleet.filter_by(is_city_bus)
    res_lambda = fleet.filter_by(lambda b: isinstance(b, CityBus))
    assert len(res_named) == len(res_lambda), "Результаты фильтрации совпадают"

    # СЦЕНАРИЙ 1: Полная цепочка filter → sort → apply (Задание 5)
    print("\n\n" + "="*50)
    print("СЦЕНАРИЙ 1: ЦЕПОЧКА ВЫЗОВОВ (Chaining)")
    
    # Фабрика функций создает фильтр для автобусов от 40 мест
    high_capacity_filter = make_capacity_filter(40)
    
    # Применяем цепочку
    processed_fleet = (fleet
                       .filter_by(high_capacity_filter)        # 1. Оставляем только вместительные
                       .sort_by(by_capacity, reverse=True)     # 2. Сортируем от больших к меньшим
                       .apply(StatusUpdateStrategy("НА РЕЙСЕ"))) # 3. Меняем им всем статус

    print_fleet(processed_fleet, "РЕЗУЛЬТАТ ЦЕПОЧКИ (Мест >= 40, Сортировка, Статус 'НА РЕЙСЕ')")


    # СЦЕНАРИЙ 2: Замена стратегии без изменения коллекции
    print("\n\n" + "="*50)
    print("СЦЕНАРИЙ 2: ЗАМЕНА СТРАТЕГИИ ПРЕОБРАЗОВАНИЯ (map)")
    
    # 1-я стратегия: обновляем статус
    active_buses = fleet.apply(StatusUpdateStrategy("ОЖИДАНИЕ"))
    print_fleet(active_buses, "СТРАТЕГИЯ 1 (Обновление статуса)")

    # 2-я стратегия: превращаем объекты в словари (для JSON) без изменения метода apply!
    dict_buses = fleet.apply(DictTransformStrategy())
    print_fleet(dict_buses, "СТРАТЕГИЯ 2 (Преобразование в словари)")


    # СЦЕНАРИЙ 3: Демонстрация Callable-объекта с состоянием
    print("\n\n" + "="*50)
    print("СЦЕНАРИЙ 3: CALLABLE-ОБЪЕКТ")
    
    # Создаем стратегию "Техобслуживание"
    maintenance_strategy = StatusUpdateStrategy("В РЕМОНТЕ")
    
    # Мы можем вызвать объект maintenance_strategy так же, как обычную функцию
    broken_bus = fleet._buses[0]
    maintenance_strategy(broken_bus) # Вызывается магический метод __call__
    
    print(f"Статус автобуса {broken_bus.route_number} изменен через callable-объект на: {broken_bus.status}")

if __name__ == "__main__":
    main()