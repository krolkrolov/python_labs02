#. главный файл запуска приложения



from app import BusParkApp
from cli import BusConsoleApp

def main():
    """основа"""
    app = BusParkApp(filepath="buses.json")
    ui = BusConsoleApp(app)
    
    try:
        ui.run()
    finally:
        print("\n" + "="*40)
        print("  System: Процесс завершен.")
        print("  Status: Код работает я не знаю почему.")
        print("  Director: Александр В")
        print("  Post-credits scene: Автобусы уехали в закат...")
        print("="*40)

if __name__ == "__main__":
    main()