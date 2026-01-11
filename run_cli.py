'''
Запуск Genshin Impact Tracker с текстовым интерфейсом

Этот файл является точкой входа для запуска программы с CLI.
''' 

import sys
import os

# Добавляем директорию проекта в путь, чтобы можно было импортировать модули
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main as cli_main
    
    if __name__ == "__main__":
        print("Запуск Genshin Impact Tracker (текстовый режим)...")
        print("Для выхода выберите соответствующий пункт меню")
        print("=" * 50)
        
        cli_main()
        
        print("\nПрограмма завершена. Спасибо за использование!")
        
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что файл main.py существует.")
    sys.exit(1)
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)