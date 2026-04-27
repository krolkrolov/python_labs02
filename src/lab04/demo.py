from models import CityBus, IntercityBus
from collection import BusFleet
from interfaces import IPrintable, IComparable

# НА 4: универсальная функция, работающая через интерфейс 
def generate_global_report(items: list[IPrintable]):
    """
    этой функции вс] равно какие классы ей передали. 
    главное, чтобы они соблюдали контракт IPrintable.
    """
    print(f"{' СВОДНЫЙ ОТЧЕТ АВТОПАРКА ':=^50}")
    for item in items:
        # полиморфизм: каждый объект печатается по-своему
        print(item.get_detailed_info())
    print("=" * 50)

def main():
    # 1. подготовка данных
    fleet = BusFleet("Main Depot")
    
    # городские: важна вместимость
    b1 = CityBus("A-10", capacity=100, has_wifi=True, standing_places=50)
    b3 = CityBus("A-20", capacity=30, has_wifi=False, standing_places=5)
    
    # междугородние: важна дистанция
    b2 = IntercityBus("Route-777", capacity=45, distance=500, has_ac=True)
    b4 = IntercityBus("Route-101", capacity=50, distance=150, has_ac=False)

    for bus in [b1, b2, b3, b4]:
        fleet.add(bus)

    # 1 сценарий: Полиморфизм через интерфейс 
    # фильтруем коллекцию и отдаем результат в универсальный отчет
    print("\n[Сценарий 1: Универсальный отчет]")
    printable_items = fleet.get_printable_entities()
    generate_global_report(printable_items)

    # 2 сценарий: проверка контрактов (isinstance)
    print("\n[Сценарий 2: Проверка реализации нескольких интерфейсов]")
    test_obj = b2
    print(f"Объект {test_obj.route_number}:")
    # проверяем, подписал ли объект конкретные контракты
    if isinstance(test_obj, IPrintable):
        print(" Реализует IPrintable (можно выводить в отчёт)")
    if isinstance(test_obj, IComparable):
        print(" Реализует IComparable (можно сравнивать)")

    # 3 сценарий: Архитектурное поведение (Сортировка)
    # здесь мы показываем, что коллекция умеет использовать методы интерфейса
    print("\n[Сценарий 3: Сортировка парка по приоритету (IComparable)]")
    print("Приоритет: для города - вместимость, для межгорода - дистанция.")
    
    sorted_list = fleet.sort_by_interface_value()
    
    for i, item in enumerate(sorted_list, 1):
        # приводим к IComparable для чистоты кода
        obj: IComparable = item 
        print(f"{i}. Маршрут {item.route_number} | Ценность: {obj.get_comparison_value()}")

if __name__ == "__main__":
    main()