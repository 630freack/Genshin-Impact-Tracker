'''
Genshin Impact Tracker - Программа для отслеживания предметов в игре

Эта программа позволяет:
- Добавлять предметы с координатами
- Отмечать их как полученные
- Просматривать и фильтровать по регионам
- Сохранять данные в JSON
- Использовать графический интерфейс

Автор: Пользователь
Версия: 1.0
''' 

import json
import os
from datetime import datetime

# Основной класс для работы с предметами

class ItemTracker:
    """
    Класс для управления предметами в Genshin Impact.
    Хранит список предметов и предоставляет методы для их управления.
    """
    
    def __init__(self, data_file="data/items.json"):
        """
        Инициализация трекера.
        Загружает данные из файла при запуске.
        
        Параметры:
            data_file (str): Путь к файлу с данными
        """
        self.data_file = data_file
        self.items = []  # Список для хранения предметов
        self.regions = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Natlan", "Snezhnaya"]  # Известные регионы
        self.load_data()  # Загружаем данные при создании объекта
    
    def add_item(self, name, region, x, y, item_type="Другое"):
        """
        Добавляет новый предмет в список.
        
        Параметры:
            name (str): Название предмета
            region (str): Регион на карте
            x (float): Координата X
            y (float): Координата Y
            item_type (str): Тип предмета (сундук, ресурс и т.д.)
            
        Возвращает:
            bool: True, если предмет успешно добавлен
        """
        # Проверяем, существует ли уже такой предмет
        for item in self.items:
            if (item['name'].lower() == name.lower() and 
                item['region'].lower() == region.lower() and 
                abs(item['x'] - x) < 0.1 and 
                abs(item['y'] - y) < 0.1):
                print(f"Предупреждение: Похожий предмет уже существует: {item['name']} в {item['region']}")
                return False
        
        # Создаем новый предмет
        new_item = {
            'name': name,
            'region': region,
            'x': x,
            'y': y,
            'type': item_type,
            'collected': False,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'notes': ""
        }
        
        self.items.append(new_item)
        print(f"Предмет '{name}' добавлен в регион {region}")
        return True
    
    def mark_collected(self, index, collected=True, notes=""):
        """
        Отмечает предмет как полученный или не полученный.
        
        Параметры:
            index (int): Индекс предмета в списке
            collected (bool): Статус получения
            notes (str): Дополнительные заметки
            
        Возвращает:
            bool: True, если успешно обновлено
        """
        if 0 <= index < len(self.items):
            self.items[index]['collected'] = collected
            if notes:
                self.items[index]['notes'] = notes
            status = "получен" if collected else "не получен"
            print(f"Предмет '{self.items[index]['name']}' отмечен как {status}")
            return True
        else:
            print("Ошибка: Неверный индекс предмета")
            return False
    
    def get_all_items(self):
        """Возвращает все предметы."""
        return self.items
    
    def get_items_by_region(self, region):
        """
        Возвращает предметы по региону.
        
        Параметры:
            region (str): Название региона
            
        Возвращает:
            list: Список предметов в указанном регионе
        """
        return [item for item in self.items if item['region'].lower() == region.lower()]
    
    def get_collected_stats(self):
        """Возвращает статистику по собранным предметам."""
        total = len(self.items)
        collected = sum(1 for item in self.items if item['collected'])
        return {
            'total': total,
            'collected': collected,
            'remaining': total - collected,
            'percentage': (collected / total * 100) if total > 0 else 0
        }
    
    def save_data(self):
        """
        Сохраняет данные в JSON файл.
        
        Возвращает:
            bool: True, если успешно сохранено
        """
        try:
            # Создаем директорию, если она не существует
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Подготавливаем данные для сохранения
            data = {
                'metadata': {
                    'save_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_items': len(self.items)
                },
                'items': self.items
            }
            
            # Сохраняем в файл с форматированием
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Данные успешно сохранены в {self.data_file}")
            return True
            
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            return False
    
    def load_data(self):
        """
        Загружает данные из JSON файла.
        
        Возвращает:
            bool: True, если успешно загружено
        """
        if not os.path.exists(self.data_file):
            print(f"Файл данных не найден: {self.data_file}")
            print("Будет создан новый файл при сохранении.")
            self.items = []
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Проверяем структуру данных
            if 'items' in data:
                self.items = data['items']
                print(f"Загружено {len(self.items)} предметов из {self.data_file}")
                return True
            else:
                print("Неверный формат файла данных")
                self.items = []
                return False
                
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            self.items = []
            return False


def main():
    """Основная функция с текстовым меню."""
    tracker = ItemTracker()
    
    while True:
        print("\n" + "="*50)
        print("      Genshin Impact Tracker - Меню")
        print("="*50)
        print("1. Добавить предмет")
        print("2. Просмотреть все предметы")
        print("3. Просмотреть предметы по региону")
        print("4. Отметить предмет как полученный")
        print("5. Показать статистику")
        print("6. Сохранить данные")
        print("7. Выйти")
        
        choice = input("\nВыберите действие (1-7): ").strip()
        
        if choice == '1':
            # Добавление нового предмета
            print("\nДоступные регионы:")
            for i, region in enumerate(tracker.regions, 1):
                print(f"{i}. {region}")
            
            try:
                region_num = int(input("\nВыберите номер региона: "))
                if 1 <= region_num <= len(tracker.regions):
                    region = tracker.regions[region_num - 1]
                else:
                    print("Неверный номер региона")
                    continue
                
                name = input("Введите название предмета: ").strip()
                if not name:
                    print("Название не может быть пустым")
                    continue
                
                item_types = ["Сундук", "Ресурс", "Задание", "Артефакт", "Оружие", "Другое"]
                print("\nТипы предметов:")
                for i, itype in enumerate(item_types, 1):
                    print(f"{i}. {itype}")
                
                type_num = int(input("\nВыберите тип предмета: "))
                if 1 <= type_num <= len(item_types):
                    item_type = item_types[type_num - 1]
                else:
                    item_type = "Другое"
                
                x = float(input("Введите координату X: "))
                y = float(input("Введите координату Y: "))
                
                tracker.add_item(name, region, x, y, item_type)
                
            except ValueError:
                print("Ошибка: Введите корректные числовые значения для координат")
            except Exception as e:
                print(f"Ошибка при добавлении предмета: {e}")
        
        elif choice == '2':
            # Просмотр всех предметов
            items = tracker.get_all_items()
            if not items:
                print("\nСписок предметов пуст.")
            else:
                print(f"\nВсего предметов: {len(items)}")
                print("\n" + "-"*80)
                for i, item in enumerate(items):
                    status = "✓ Получен" if item['collected'] else "○ Не собран"
                    notes_info = f" | Примечания: {item['notes']}" if item['notes'] else ""
                    print(f"{i:2}. [{status}] {item['name']}")
                    print(f"     Регион: {item['region']} | Тип: {item['type']}")
                    print(f"     Координаты: X={item['x']:.1f}, Y={item['y']:.1f} | Добавлен: {item['date_added']}{notes_info}")
                    print("-"*80)
        
        elif choice == '3':
            # Фильтрация по региону
            print("\nДоступные регионы:")
            for i, region in enumerate(tracker.regions, 1):
                region_items = tracker.get_items_by_region(region)
                count = len(region_items)
                collected_count = sum(1 for item in region_items if item['collected'])
                print(f"{i}. {region} ({collected_count}/{count})")
            
            try:
                region_num = int(input("\nВыберите номер региона для просмотра: "))
                if 1 <= region_num <= len(tracker.regions):
                    region = tracker.regions[region_num - 1]
                    items = tracker.get_items_by_region(region)
                    
                    if not items:
                        print(f"\nВ регионе {region} нет предметов.")
                    else:
                        print(f"\nПредметы в регионе {region}: {len(items)}")
                        print("\n" + "-"*80)
                        for i, item in enumerate(items):
                            status = "✓ Получен" if item['collected'] else "○ Не собран"
                            notes_info = f" | Примечания: {item['notes']}" if item['notes'] else ""
                            item_idx = tracker.items.index(item)  # Находим реальный индекс
                            print(f"{item_idx:2}. [{status}] {item['name']}")
                            print(f"     Тип: {item['type']}")
                            print(f"     Координаты: X={item['x']:.1f}, Y={item['y']:.1f} | Добавлен: {item['date_added']}{notes_info}")
                            print("-"*80)
                else:
                    print("Неверный номер региона")
            
            except ValueError:
                print("Введите корректный номер")
        
        elif choice == '4':
            # Отметить как полученный
            items = tracker.get_all_items()
            if not items:
                print("\nСписок предметов пуст.")
            else:
                print(f"\nВсего предметов: {len(items)}")
                print("Для отметки как полученного введите индекс предмета.")
                print("Чтобы отметить как несобранный, введите индекс с минусом (например, -5)")
                
                try:
                    index_input = input("Введите индекс: ").strip()
                    if not index_input:
                        continue
                        
                    index = int(index_input)
                    
                    if index == 0:
                        print("Индекс не может быть 0")
                        continue
                    
                    # Определяем индекс и статус
                    if index > 0:
                        item_index = index - 1  # Преобразуем к нулю-based
                        collected = True
                        status_text = "получен"
                    else:
                        item_index = abs(index) - 1
                        collected = False
                        status_text = "не собран"
                    
                    if 0 <= item_index < len(items):
                        notes = input(f"Введите примечания (Enter для пропуска): ").strip()
                        tracker.mark_collected(item_index, collected, notes)
                    else:
                        print("Неверный индекс предмета")
                        
                except ValueError:
                    print("Введите корректный номер")
        
        elif choice == '5':
            # Статистика
            stats = tracker.get_collected_stats()
            print("\n" + "="*40)
            print("           СТАТИСТИКА")
            print("="*40)
            print(f"Всего предметов: {stats['total']}")
            print(f"Собрано: {stats['collected']}")
            print(f"Осталось: {stats['remaining']}")
            print(f"Процент собранного: {stats['percentage']:.1f}%")
            
            # Статистика по регионам
            print("\nПо регионам:")
            for region in tracker.regions:
                region_items = tracker.get_items_by_region(region)
                if region_items:  # Показываем только регионы с предметами
                    collected = sum(1 for item in region_items if item['collected'])
                    percentage = (collected / len(region_items) * 100) if region_items else 0
                    print(f"  {region}: {collected}/{len(region_items)} ({percentage:.1f}%)")
        
        elif choice == '6':
            # Сохранение
            tracker.save_data()
        
        elif choice == '7':
            # Выход
            # Спрашиваем, нужно ли сохранить
            if tracker.items:  # Есть несохраненные данные
                stats = tracker.get_collected_stats()
                print(f"\nТекущая статистика:")
                print(f"Собрано: {stats['collected']}/{stats['total']} ({stats['percentage']:.1f}%)")
                
                save_before_exit = input("\nСохранить данные перед выходом? (y/n): ").strip().lower()
                if save_before_exit in ['y', 'yes', 'да', 'д']:
                    tracker.save_data()
            
            print("Спасибо за использование Genshin Impact Tracker!")
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, введите число от 1 до 7.")

if __name__ == "__main__":
    main()