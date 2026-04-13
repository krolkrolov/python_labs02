from collection import BusFleet
from models import CityBus, IntercityBus

def main():
    fleet = BusFleet("Мой Парк")
    
    # Создаем объекты с новыми атрибутами
    b1 = CityBus("45", 50, has_wifi=True, standing_places=30)
    b2 = IntercityBus("100", 40, distance=200, has_ac=True)
    
    fleet.add(b1)
    fleet.add(b2)
    
    print("=== 1) Полиморфизм и новые атрибуты (__str__) ===")
    for bus in fleet:
        # Здесь сработает новый __str__ из models.py
        print(f"{bus} -> Цена: {bus.calculate_fare()} руб.")
        
    print("\n=== 2) Проверка специфических методов (isinstance) ===")
    for bus in fleet:
        if isinstance(bus, CityBus):
            bus.announce_stop("Центральная площадь")
        if isinstance(bus, IntercityBus):
            bus.reserve_seat(15)

    # Сценарий 3: Фильтрация по типу (Требование на 5)
    print("\n=== 3) Фильтрация коллекции (Только Городские) ===")
    # Генерируем новый список, оставляя только CityBus
    city_only = [b for b in fleet if isinstance(b, CityBus)]
    
    for cb in city_only:
        print(f"Выборка: {cb.route_number} (Мест: {cb.standing_places})")

if __name__ == "__main__":
    main()