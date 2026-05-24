#модуль консольного интерфейса CLI, отвечает за ввод и вывод данных.

import os

from app import BusParkApp
from models import CityBus, IntercityBus
from exceptions import ItemNotFoundError, DuplicateItemError

class BusConsoleApp:

    def _clear_screen(self) -> None:
        """Очищает экран терминала."""
        # для винды это 'cls', для calla - 'clear'
        os.system('cls' if os.name == 'nt' else 'clear')

    def _ask_yes_no(self, question: str) -> bool:
        """Вспомогательный метод для получения четкого ответа y/n."""
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
        """выводит список автобусов и ждет нажатия ентер перед возвратом в меню."""
        target_list = buses if buses is not None else self.app.get_all()
        
        if not target_list:
            print("\n[!] Список пуст.")
        else:
            # Шапка таблицы
            print("\n{:<10} | {:<12} | {:<6} | {:<12} | {:<15} | {:<20}".format(
                "Маршрут", "Тип", "Мест", "Доп. инфо", "Стоимость", "Особенности"
            ))
            print("-" * 85)

            for b in target_list:
                b_type = "City" if isinstance(b, CityBus) else "Intercity"

                # формирование колонки "Доп. инфо"
                if isinstance(b, CityBus):
                    extra_info = f"Ст.мест: {b.standing_places}"
                elif isinstance(b, IntercityBus):
                    extra_info = f"{b.distance} км"
                else:
                    extra_info = "-"
                
                # расчет стоимости (из ЛР6)
                fare = f"{b.calculate_fare():.2f} руб."

                print("{:<10} | {:<12} | {:<6} | {:<12} | {:<15} | {:<20}".format(
                    b.route_number, b_type, b._capacity, extra_info, fare, b.display()
                ))
        
        print("\n" + "=" * 85)
        input("Нажмите [Enter], чтобы вернуться в главное меню...")

    def run(self) -> None:
        """основной цикл работы CLI."""
        while True:
            self._clear_screen() # очистка всего старое барахла перед показом меню
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
                    input("Нажмите Enter, чтобы продолжить...") # пауза, чтобы успеть прочитать ошибку
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
            
            new_bus = CityBus(route, cap, wifi, stands, fare)
            self.app.add_bus(new_bus)
            print("[+] Городской автобус успешно добавлен.")
            input("\nНажмите Enter...")
        except ValueError:
            print("\n[!] Ошибка: Ну сказано же - ВВЕДИТЕ ЧИСЛО!")
            print("Попробуем заново))")
            input("\nНажмите Enter...")
        except DuplicateItemError as e:
            print(f"Ошибка: {e}")
            input("\nНажмите Enter...")

    def _add_intercity_bus_ui(self) -> None:
        try:
            route = input("Введите номер маршрута: ")
            cap = int(input("Вместимость: "))
            dist = float(input("Дистанция (км): "))
            ac = self._ask_yes_no("Есть кондиционер?")
            rate = float(input("Введите тариф (руб/км): "))
            
            new_bus = IntercityBus(route, cap, dist, ac, rate)
            self.app.add_bus(new_bus)
            print("[+] Междугородний автобус успешно добавлен.")
            input("\nНажмите Enter...")
        except ValueError:
            print("Ошибка -_-: некорректный ввод чисел.")
            input("\nНажмите Enter...")
        except DuplicateItemError as e:
            print(f"Ошибка: {e}")
            input("\nНажмите Enter...")

    def _find_bus_ui(self) -> None:
        route = input("Введите маршрут для поиска: ")
        bus = self.app.find_bus(route)
        if bus:
            # передача ОДНОГО найденного автобуса в красивый метод
            self._show_buses([bus]) 
        else:
            print("[!] Автобус не найден.")
            input("Нажмите Enter...")

    def _filter_ui(self) -> None:
        try:
            min_cap = int(input("Показать автобусы с вместимостью от: "))
            
            if min_cap <= 0:
                print("\n[?] Автобус с нулевой вместимостью? не-не")
                input("\nНажмите Enter, чтобы вернуться в реальный мир...")
                return
                
            filtered = self.app.filter_by_capacity(min_cap)
            self._show_buses(filtered) 
        except ValueError:
            print("Ошибка: введите целое число.")

    def _sort_ui(self) -> None:
        print("\nСортировать по: 1-Маршруту, 2-Местам, 3-Цене")
        try:
            strategy = int(input("Ваш выбор: "))
            sorted_list = self.app.sort_buses(strategy)
            # передаем отсортированный список в метод вывода
            self._show_buses(sorted_list)
        except ValueError:
            print("Ошибка: введите число.")

    def _remove_bus_ui(self) -> None:
        route = input("Введите маршрут для удаления: ")

        if route.lower() in ["скибиди", "сигма", "черемша"]:
            print("\n[!] Критическая ошибка: Обнаружен запредельный уровень кринжа. Удаление заблокировано РНК.")
            input("\nНажмите Enter для очистки кармы...")
            return

        # запуск бесконечного цикла, пока пользователь не введет корректный символ
        while True:
            confirm = input(f"Вы уверены, что хотите удалить маршрут {route}? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    self.app.remove_bus(route)
                    print(f"[x] Маршрут {route} удален.")
                    break # выход из цикла, тк действие выполнено
                except ItemNotFoundError as e:
                    print(f"Ошибка: {e}")
                    break # выход из цикла, тк объекта и так нет
            elif confirm == 'n':
                print("[*] Удаление отменено.")
                break # выход из цикла, отменив операцию
            else:
                # если введено чёто другое - ггворим что пользователь геншин импактер, цикл идет на следующий круг
                print("Ошибка: некорректный ввод. Пожалуйста, введите только 'y' (да) или 'n' (нет).")