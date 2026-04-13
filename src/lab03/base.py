from validate import validate_route_number, validate_capacity, validate_passengers

class Bus:
    # Атрибут класса (один на всех)
    MAX_SPEED_LIMIT = 90  

    def __init__(self, route_number: str, capacity: int):
        # Конструктор с полной инициализацией
        self._route_number = validate_route_number(route_number)
        self._capacity = validate_capacity(capacity)
        self._passengers = 0          
        self._is_on_route = False     

    #Свойства (Properties)
    
    @property
    def route_number(self) -> str:
        return self._route_number

    @route_number.setter
    def route_number(self, value: str):
        self._route_number = validate_route_number(value)

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def passengers(self) -> int:
        return self._passengers

    @property
    def is_on_route(self) -> bool:
        return self._is_on_route

    #Интерфейс для ЛР-3

    def calculate_fare(self) -> float:
        """Общий метод для полиморфизма (базовая цена)."""
        return 50.0

    #Бизнес-логика

    def start_route(self):
        if self._is_on_route:
            print(f"Автобус {self._route_number} уже на маршруте!")
            return
        self._is_on_route = True
        print(f"Автобус {self._route_number} выехал на маршрут.")

    def finish_route(self):
        self._is_on_route = False
        self._passengers = 0
        print(f"Автобус {self._route_number} вернулся в парк.")

    #Магические методы

    def __str__(self) -> str:
        """Красивый вывод. Переопределяется в наследниках."""
        status = "в пути" if self._is_on_route else "в парке"
        return f"Автобус №{self._route_number} | Статус: {status}"

    def __repr__(self) -> str:
        return f"Bus(route='{self._route_number}', cap={self._capacity})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Bus):
            return NotImplemented
        return self._route_number == other.route_number and self._capacity == other.capacity