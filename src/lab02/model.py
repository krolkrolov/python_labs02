from validate import validate_route_number, validate_capacity, validate_passengers

class Bus:
    # Атрибут класса (один на всех) - требование на 4
    MAX_SPEED_LIMIT = 90  

    def __init__(self, route_number: str, capacity: int):
        # Конструктор с базовой проверкой через вызов сеттеров или напрямую
        self._route_number = validate_route_number(route_number)
        self._capacity = validate_capacity(capacity)
        self._passengers = 0          # Изначально автобус пуст
        self._is_on_route = False     # Состояние: находится ли автобус на маршруте (требование на 5)

    # --- Свойства (Properties) для инкапсуляции ---
    
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

    # --- Бизнес-методы и изменение состояния (Требование на 5) ---

    def start_route(self):
        """Переводит автобус в состояние 'на маршруте'."""
        if self._is_on_route:
            print(f"Автобус {self._route_number} уже на маршруте!")
            return
        self._is_on_route = True
        print(f"Автобус {self._route_number} выехал на маршрут.")

    def finish_route(self):
        """Завершает маршрут и высаживает всех пассажиров."""
        self._is_on_route = False
        self._passengers = 0
        print(f"Автобус {self._route_number} вернулся в парк. Все пассажиры вышли.")

    def board_passengers(self, count: int):
        """
        Бизнес-метод посадки пассажиров.
        Поведение зависит от состояния: нельзя сажать людей, если автобус в парке.
        """
        if not self._is_on_route:
            raise RuntimeError(f"Нельзя посадить пассажиров: автобус {self._route_number} не на маршруте (в парке).")
        
        new_total = self._passengers + count
        # Проверяем вместимость с помощью функции из validate.py
        self._passengers = validate_passengers(new_total, self._capacity)
        print(f"Посажено {count} чел. Всего в автобусе: {self._passengers}/{self._capacity}.")

    # --- Магические методы ---

    def __str__(self) -> str:
        """Пользовательский вывод (красивая f-строка)."""
        status = "в пути" if self._is_on_route else "в парке"
        return f" Автобус №{self._route_number} | Вместимость: {self._capacity} | Сейчас: {status} ({self._passengers} пасс.)"

    def __repr__(self) -> str:
        """Вывод для разработчика."""
        return f"Bus(route_number='{self._route_number}', capacity={self._capacity}, passengers={self._passengers}, is_on_route={self._is_on_route})"

    def __eq__(self, other) -> bool:
        """Сравнение двух объектов автобусов."""
        if not isinstance(other, Bus):
            return NotImplemented
        return self._route_number == other.route_number and self._capacity == other.capacity