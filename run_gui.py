'''
Запуск Genshin Impact Tracker с графическим интерфейсом

Этот файл является точкой входа для запуска программы с GUI.
''' 

import sys
import os

# Добавляем директорию проекта в путь, чтобы можно было импортировать модули
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.genshin_gui import main as gui_main
    
    if __name__ == "__main__":
        print("Запуск Genshin Impact Tracker...")
        print("Для выхода закройте окно или нажмите Ctrl+C")
        print("=" * 50)
        
        gui_main()
        
        print("\nПрограмма завершена. Спасибо за использование!")
        
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все файлы находятся в правильных директориях.")
    sys.exit(1)
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)