from base import Bus

# Первый наследник: Городской
class CityBus(Bus):
    def __init__(self, route_number, capacity, has_wifi, standing_places):
        super().__init__(route_number, capacity) 
        #2 НОВЫХ АТРИБУТА
        self.has_wifi = has_wifi          # 1-й атрибут
        self.standing_places = standing_places  # 2-й атрибут 

    #ПЕРЕОПРЕДЕЛЕННЫЙ МЕТОД
    def calculate_fare(self): 
        return 40.0

    #НОВЫЙ МЕТОД
    def announce_stop(self, stop): 
        print(f"Остановка: {stop}")

    def __str__(self):
        base_info = super().__str__()
        wifi = "с Wi-Fi" if self.has_wifi else "без Wi-Fi"
        return f"{base_info} | {wifi} | Мест стоя: {self.standing_places}"

# Второй наследник: Межгород
class IntercityBus(Bus):
    def __init__(self, route_number, capacity, distance, has_ac):
        super().__init__(route_number, capacity)
        #2 НОВЫХ АТРИБУТА
        self.distance = distance          # 1-й атрибут
        self.has_ac = has_ac              # 2-й атрибут

    #ПЕРЕОПРЕДЕЛЕННЫЙ МЕТОД
    def calculate_fare(self): 
        return self.distance * 3.5

    #НОВЫЙ МЕТОД
    def reserve_seat(self, seat_number): # Добавили новый метод
        print(f"Место {seat_number} забронировано")

    def __str__(self):
        base_info = super().__str__()
        ac = "с кондеем" if self.has_ac else "без кондея"
        return f"{base_info} | {self.distance}км | {ac}"