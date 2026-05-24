import json
import os
from typing import List, Dict, Any

# импортируем классы
from models import Bus, CityBus, IntercityBus

def save(buses: List[Bus], filepath: str) -> None:
    """сохраняет список автобусов в JSON файл."""
    data = []
    for bus in buses:
        if isinstance(bus, CityBus):
            data.append({
                "type": "CityBus",
                "route_number": bus.route_number,
                "capacity": bus._capacity,
                "has_wifi": bus.has_wifi,
                "standing_places": bus.standing_places,
                "base_fare": bus.base_fare  # брутально сохраняем цену билета
            })
        elif isinstance(bus, IntercityBus):
            data.append({
                "type": "IntercityBus",
                "route_number": bus.route_number,
                "capacity": bus._capacity,
                "distance": bus.distance,
                "has_ac": bus.has_ac,
                "price_per_km": bus.price_per_km  # сохраняем мужчинский тариф
            })
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(filepath: str) -> List[Bus]:
    """загружает автобусы из JSON файла, возвращает список объектов."""
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data: List[Dict[str, Any]] = json.load(f)
        except json.JSONDecodeError:
            return []
            
    buses = []
    for item in data:
        if item["type"] == "CityBus":
            # передаем base_fare из файла в конструктор класса
            buses.append(CityBus(
                item["route_number"], item["capacity"], 
                item["has_wifi"], item["standing_places"],
                item.get("base_fare", 40.0) # get с дефолтом, чтобы не упало на старых данных
            ))
        elif item["type"] == "IntercityBus":
            # передаем price_per_km из файла в конструктор класса
            buses.append(IntercityBus(
                item["route_number"], item["capacity"], 
                item["distance"], item["has_ac"],
                item.get("price_per_km", 3.5) # get с дефолтом 3.5
            ))
    return buses