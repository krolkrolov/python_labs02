# Модуль консольного интерфейса CLI, отвечает за ввод и вывод данных.

import os
from app import BusParkApp
from models import CityBus, IntercityBus
from exceptions import ItemNotFoundError, DuplicateItemError

class BusConsoleApp:

    def _clear_screen(self) -> None:
        """очищает экран терминала"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _ask_yes_no(self, question: str) -> bool:
        """вспомогательный метод для получения четкого ответа y/n"""
        attempts = 0
        while True:
            ans = input(f"{question} (y/n): ").strip().lower()
            if ans == 'y': return True
            if ans == 'n': return False
            
            attempts += 1
            if attempts == 3:
                print("Ошибка: кажется, пользователь фанат Геншина. Попробуй еще раз, Сокровище моё.")
            elif attempts > 5:
                print("Ошибка: Я буду спрашивать вечно. Мы в Главе 1: Вечный ввод. Введите y или n!")
            else:
                print("Ошибка: некорректный ввод. Только 'y' или 'n'.")

    def __init__(self, app: BusParkApp) -> None:
        self.app = app

    def _print_menu(self) -> None:
        """печать главного меню."""
        print("\n--- УПРАВЛЕНИЕ АВТОБУСНЫМ ПАРКОМ ---")
        print("1. Показать все автобусы")
        print("2. Добавить городской автобус")
        print("3. Добавить междугородний автобус")
        print("4. Найти автобус по маршруту")
        print("5. Фильтровать по вместимости")
        print("6. Сортировать список")
        print("7. Удалить автобус")
        print("0. Сохранить и выйти")

    def _show_buses(self, buses=None) -> None:
        """выводит список автобусов и ждет нажатия Enter перед возвратом в меню"""
        target_list = buses if buses is not None else self.app.get_all()
        
        if not target_list:
            print("\n[!] Список пуст.")
        else:
            print("\n{:<10} | {:<12} | {:<6} | {:<12} | {:<15} | {:<20}".format(
                "Маршрут", "Тип", "Мест", "Доп. инфо", "Стоимость", "Особенности"
            ))
            print("-" * 85)

            for b in target_list:
                b_type = "City" if isinstance(b, CityBus) else "Intercity"

                if isinstance(b, CityBus):
                    extra_info = f"Ст.мест: {b.standing_places}"
                elif isinstance(b, IntercityBus):
                    extra_info = f"{b.distance} км"
                else:
                    extra_info = "-"
                
                fare = f"{b.calculate_fare():.2f} руб."

                print("{:<10} | {:<12} | {:<6} | {:<12} | {:<15} | {:<20}".format(
                    b.route_number, b_type, b._capacity, extra_info, fare, b.display()
                ))
        
        print("\n" + "=" * 85)
        input("Нажмите [Enter], чтобы вернуться в главное меню...")

    def run(self) -> None:
        """основной цикл работы CLI."""
        while True:
            self._clear_screen()
            self._print_menu()
            try:
                choice = input("\nВыберите пункт: ")
                if choice == "1":
                    self._show_buses()
                elif choice == "2":
                    self._add_city_bus_ui()
                elif choice == "3":
                    self._add_intercity_bus_ui()
                elif choice == "4":
                    self._find_bus_ui()
                elif choice == "5":
                    self._filter_ui()
                elif choice == "6":
                    self._sort_ui()
                elif choice == "7":
                    self._remove_bus_ui()
                elif choice == "300":
                    print("\n[!] Отсортировать автобусы по трактористам? PS На защите не использовать")
                    input("\nНажмите Enter...")
                elif choice == "67":
                    print("\n[!] жесть../")
                    input("\nНажмите Enter...")
                elif choice == "0":
                    self.app.save_data()
                    print("Данные сохранены. До свидания!")
                    break
                else:
                    print("Ошибка: неверный пункт меню.")
                    input("Нажмите Enter, чтобы продолжить...")
            except Exception as e:
                print(f"Критическая ошибка: {e}")
                input("Нажмите Enter для продолжения...")

    def _add_city_bus_ui(self) -> None:
        try:
            route = input("Введите номер маршрута: ")
            cap = int(input("Вместимость: "))
            wifi = self._ask_yes_no("Есть Wi-Fi?")
            stands = int(input("Кол-во стоячих мест: "))
            fare = float(input("Введите стоимость билета (руб): "))
            
            self.app.add_city_bus(route, cap, wifi, stands, fare)
            
            print("[+] Городской автобус успешно добавлен.")
            input("\nНажмите Enter...")
        except ValueError as e:
            if "invalid literal" in str(e) or "could not convert" in str(e):
                print("\n[!] Ошибка: Ну сказано же - ВВЕДИТЕ ЧИСЛО!")
            else:
                print(f"\n[!] Ошибка: {e}")
            input("\nНажмите Enter...")
        except DuplicateItemError as e:
            print(f"\nОшибка: {e}")
            input("\nНажмите Enter...")

    def _add_intercity_bus_ui(self) -> None:
        try:
            route = input("Введите номер маршрута: ")
            cap = int(input("Вместимость: "))
            dist = float(input("Дистанция (км): "))
            ac = self._ask_yes_no("Есть кондиционер?")
            rate = float(input("Введите тариф (руб/км): "))
            
            self.app.add_intercity_bus(route, cap, dist, ac, rate)
            
            print("[+] Междугородний автобус успешно добавлен.")
            input("\nНажмите Enter...")
        except ValueError as e:
            if "invalid literal" in str(e) or "could not convert" in str(e):
                print("\n[!] Ошибка -_-: некорректный ввод чисел.")
            else:
                print(f"\n[!] Ошибка: {e}")
            input("\nНажмите Enter...")
        except DuplicateItemError as e:
            print(f"\nОшибка: {e}")
            input("\nНажмите Enter...")

    def _find_bus_ui(self) -> None:
        route = input("Введите маршрут для поиска: ")
        bus = self.app.find_bus(route)
        if bus:
            self._show_buses([bus]) 
        else:
            print("[!] Автобус не найден.")
            input("Нажмите Enter...")

    def _filter_ui(self) -> None:
        try:
            min_cap = int(input("Показать автобусы с вместимостью от: "))
            filtered = self.app.filter_by_capacity(min_cap)
            self._show_buses(filtered) 
        except ValueError as e:
            if "invalid literal" in str(e):
                print("Ошибка: введите целое число.")
            else:
                # cюда прилетит ошибка из апликации, если ввели <= 0
                print(f"\n[?] {e}")
                input("\nНажмите Enter, чтобы вернуться в реальный мир...")

    def _sort_ui(self) -> None:
        print("\nСортировать по: 1-Маршруту, 2-Местам, 3-Цене")
        try:
            strategy = int(input("Ваш выбор: "))
            sorted_list = self.app.sort_buses(strategy)
            self._show_buses(sorted_list)
        except ValueError as e:
             if "invalid literal" in str(e):
                print("Ошибка: введите число.")
             else:
                print(f"Ошибка: {e}")
             input("\nНажмите Enter...")

    def _remove_bus_ui(self) -> None:
        route = input("Введите маршрут для удаления: ")

        # логика UI: спросить подтверждение
        if not self._ask_yes_no(f"Вы уверены, что хотите удалить маршрут {route}?"):
            print("[*] Удаление отменено.")
            input("\nНажмите Enter...")
            return

        try:
            self.app.remove_bus(route)
            print(f"[x] Маршрут {route} удален.")
            input("\nНажмите Enter...")
        except ValueError as e:
            print(f"\n[!] Критическая ошибка: {e}")
            input("\nНажмите Enter для очистки кармы...")
        except ItemNotFoundError as e:
            print(f"Ошибка: {e}")
            input("\nНажмите Enter...")