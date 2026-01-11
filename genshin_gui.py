'''
Genshin Impact Tracker - Графический интерфейс

Этот модуль создает графический интерфейс для трекера предметов.
Использует библиотеку tkinter - стандартную для Python.
''' 

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
from main import ItemTracker  # Импортируем основной класс


class GenshinTrackerGUI:
    """
    Класс, создающий графический интерфейс для трекера предметов Genshin Impact.
    Использует tkinter для создания окон и элементов управления.
    """
    
    def __init__(self, root):
        """
        Инициализация графического интерфейса.
        
        Параметры:
            root: Основное окно tkinter
        """
        self.root = root
        self.tracker = ItemTracker()  # Создаем экземпляр трекера
        self.setup_window()  # Настраиваем окно
        self.create_widgets()  # Создаем элементы интерфейса
        self.refresh_items()  # Обновляем список предметов

    def setup_window(self):
        """Настраивает основные параметры окна."""
        self.root.title("Genshin Impact Tracker")
        self.root.geometry("1000x700")  # Размер окна
        self.root.minsize(800, 600)  # Минимальный размер
        
        # Центрируем окно на экране
        self.center_window()
        
        # Настраиваем сетку для адаптивности
        self.root.grid_rowconfigure(1, weight=1)  # Ряд с таблицей растягивается
        self.root.grid_columnconfigure(0, weight=1)
        
        # Устанавливаем иконку (если есть)
        # try:
        #     self.root.iconbitmap("icon.ico")  # Раскомментируйте, если добавите иконку
        # except:
        #     pass
        
        # Привязываем событие закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        """Центрирует окно на экране."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Создает и размещает все элементы интерфейса."""
        # Создаем верхнюю панель с кнопками
        self.create_top_frame()
        
        # Создаем таблицу для отображения предметов
        self.create_treeview()
        
        # Создаем нижнюю панель с информацией
        self.create_bottom_frame()

    def create_top_frame(self):
        """Создает верхнюю панель с кнопками управления."""
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.grid_columnconfigure(5, weight=1)  # Растягиваем пустой столбец
        
        # Выбор региона
        ttk.Label(top_frame, text="Фильтр по региону:").grid(row=0, column=0, padx=5, pady=5)
        
        self.region_var = tk.StringVar(value="Все регионы")
        regions = ["Все регионы"] + self.tracker.regions
        self.region_combo = ttk.Combobox(
            top_frame, 
            textvariable=self.region_var, 
            values=regions, 
            state="readonly",
            width=15
        )
        self.region_combo.grid(row=0, column=1, padx=5, pady=5)
        self.region_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_items())
        
        # Кнопка обновления
        ttk.Button(
            top_frame, 
            text="🔄 Обновить", 
            command=self.refresh_items
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Кнопки действий
        ttk.Button(
            top_frame, 
            text="➕ Добавить", 
            command=self.open_add_item_window
        ).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(
            top_frame, 
            text="✏️ Редактировать", 
            command=self.open_edit_item_window
        ).grid(row=0, column=4, padx=5, pady=5)
        
        # Пустой столбец для растяжки
        top_frame.grid_columnconfigure(5, weight=1)
        
        # Кнопка сохранения
        ttk.Button(
            top_frame, 
            text="💾 Сохранить", 
            command=self.save_data
        ).grid(row=0, column=6, padx=5, pady=5)

    def create_treeview(self):
        """Создает таблицу для отображения списка предметов."""
        # Создаем фрейм для таблицы
        tree_frame = ttk.Frame(self.root, padding="10")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Создаем таблицу (Treeview)
        columns = ("#", "Статус", "Название", "Регион", "Тип", "X", "Y", "Добавлен", "Примечания", "Действия")
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show="headings", 
            selectmode="browse"
        )
        
        # Настраиваем заголовки столбцов
        self.tree.heading("#", text="#", anchor="center")
        self.tree.heading("Статус", text="Статус", anchor="center")
        self.tree.heading("Название", text="Название", anchor="w")
        self.tree.heading("Регион", text="Регион", anchor="center")
        self.tree.heading("Тип", text="Тип", anchor="center")
        self.tree.heading("X", text="X", anchor="center")
        self.tree.heading("Y", text="Y", anchor="center")
        self.tree.heading("Добавлен", text="Добавлен", anchor="center")
        self.tree.heading("Примечания", text="Примечания", anchor="w")
        self.tree.heading("Действия", text="Действия", anchor="center")
        
        # Настраиваем ширину столбцов
        self.tree.column("#", width=30, anchor="center", stretch=False)
        self.tree.column("Статус", width=60, anchor="center", stretch=False)
        self.tree.column("Название", width=150, anchor="w", stretch=True)
        self.tree.column("Регион", width=100, anchor="center", stretch=False)
        self.tree.column("Тип", width=100, anchor="center", stretch=False)
        self.tree.column("X", width=60, anchor="center", stretch=False)
        self.tree.column("Y", width=60, anchor="center", stretch=False)
        self.tree.column("Добавлен", width=120, anchor="center", stretch=False)
        self.tree.column("Примечания", width=150, anchor="w", stretch=True)
        self.tree.column("Действия", width=100, anchor="center", stretch=False)
        
        # Добавляем прокрутку
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Размещаем таблицу и скроллбары
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Привязываем двойной клик к редактированию
        self.tree.bind("<Double-1>", lambda e: self.open_edit_item_window())
        
        # Создаем фрейм для кнопок действий
        self.action_buttons_frame = ttk.Frame(tree_frame)
        self.action_buttons_frame.grid(row=0, column=2, sticky="ns")
        
        # Кнопка для выполнения/отмены выполнения предмета
        self.toggle_button = ttk.Button(
            self.action_buttons_frame, 
            text="Выполнено", 
            command=self.toggle_item_status
        )
        self.toggle_button.pack(pady=5)

    def create_bottom_frame(self):
        """Создает нижнюю панель с общей информацией."""
        bottom_frame = ttk.LabelFrame(self.root, text="Статистика", padding="10")
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        # Создаем метки для статистики
        self.stats_labels = {}
        stats_config = [
            ("Всего предметов: ", "total"),
            ("Собрано: ", "collected"),
            ("Осталось: ", "remaining"),
            ("Процент: ", "percentage")
        ]
        
        for i, (text, key) in enumerate(stats_config):
            ttk.Label(bottom_frame, text=text).grid(row=0, column=i*2, padx=(0, 5))
            self.stats_labels[key] = ttk.Label(bottom_frame, text="0")
            self.stats_labels[key].grid(row=0, column=i*2+1, padx=(0, 15))
        
        # Кнопка выхода
        ttk.Button(
            bottom_frame, 
            text="Выход", 
            command=self.on_closing
        ).grid(row=0, column=8, padx=20)

    def refresh_items(self):
        """Обновляет список предметов в таблице."""
        # Очищаем текущие данные
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем данные для отображения
        selected_region = self.region_var.get()
        if selected_region == "Все регионы":
            items = self.tracker.get_all_items()
        else:
            items = self.tracker.get_items_by_region(selected_region)
        
        # Добавляем предметы в таблицу
        for i, item in enumerate(items):
            # Определяем значок статуса
            status = "✓" if item['collected'] else "○"
            status_color = "green" if item['collected'] else "red"
            
            # Добавляем строку в таблицу
            item_id = self.tree.insert("", "end", values=(
                i + 1,
                status,
                item['name'],
                item['region'],
                item['type'],
                f"{item['x']:.1f}",
                f"{item['y']:.1f}",
                item['date_added'],
                item['notes'],
                ""
            ))
            
            # Устанавливаем цвет текста в зависимости от статуса
            if item['collected']:
                self.tree.item(item_id, tags=("collected",))
            
            # Сохраняем идентификатор предмета и его данные для последующего использования
            self.tree.item(item_id, tags=("collected" if item['collected'] else "uncollected",))
        
        # Настраиваем теги для цветового выделения
        self.tree.tag_configure("collected", foreground="green")
        
        # Обновляем статистику
        self.update_stats()

    def update_stats(self):
        """Обновляет отображение статистики."""
        stats = self.tracker.get_collected_stats()
        self.stats_labels['total'].config(text=str(stats['total']))
        self.stats_labels['collected'].config(text=str(stats['collected']))
        self.stats_labels['remaining'].config(text=str(stats['remaining']))
        self.stats_labels['percentage'].config(text=f"{stats['percentage']:.1f}%")
        
        # Обновляем текст кнопки в зависимости от общего статуса
        if stats['collected'] == stats['total'] and stats['total'] > 0:
            self.toggle_button.config(text="Все выполнено")
        elif stats['collected'] == 0:
            self.toggle_button.config(text="Выполнить все")
        else:
            self.toggle_button.config(text="Выполнено")

    def open_add_item_window(self):
        """Открывает окно для добавления нового предмета."""
        AddEditItemWindow(self.root, self.tracker, self, mode="add")

    def open_edit_item_window(self):
        """Открывает окно для редактирования существующего предмета."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Сначала выберите предмет для редактирования!")
            return
        
        # Получаем индекс выбранного предмета
        item_id = selected_items[0]
        item_index = self.tree.index(item_id)
        
        # Получаем отфильтрованный список в зависимости от региона
        selected_region = self.region_var.get()
        if selected_region == "Все регионы":
            items = self.tracker.get_all_items()
        else:
            items = self.tracker.get_items_by_region(selected_region)
        
        if 0 <= item_index < len(items):
            AddEditItemWindow(self.root, self.tracker, self, mode="edit", item=items[item_index])
        else:
            messagebox.showerror("Ошибка", "Не удалось найти выбранный предмет.")

    def save_data(self):
        """Сохраняет данные и показывает результат."""
        if self.tracker.save_data():
            messagebox.showinfo("Успех", "Данные успешно сохранены!")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные!")

    def on_closing(self):
        """Обрабатывает закрытие окна."""
        if self.tracker.items:  # Есть несохраненные данные
            stats = self.tracker.get_collected_stats()
            message = f"У вас {stats['collected']}/{stats['total']} предметов собрано.\n\nСохранить данные перед выходом?"
            
            result = messagebox.askyesnocancel(
                "Выход", 
                message,
                default=messagebox.YES
            )
            
            if result is True:  # Да - сохранить
                self.save_data()
                self.root.destroy()
            elif result is False:  # Нет - выйти без сохранения
                self.root.destroy()
            # Если Cancel - ничего не делаем (остаемся в программе)
        else:
            self.root.destroy()
            
    def toggle_item_status(self):
        """Переключает статус выбранного предмета между выполнено/не выполнено."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Сначала выберите предмет для изменения статуса!")
            return
        
        # Получаем идентификатор выбранного предмета
        item_id = selected_items[0]
        item_values = self.tree.item(item_id)['values']
        
        # Получаем отфильтрованный список в зависимости от региона
        selected_region = self.region_var.get()
        if selected_region == "Все регионы":
            items = self.tracker.get_all_items()
        else:
            items = self.tracker.get_items_by_region(selected_region)
        
        # Находим индекс предмета в списке
        item_index = self.tree.index(item_id)
        
        if 0 <= item_index < len(items):
            # Получаем текущий статус
            current_collected = items[item_index]['collected']
            
            # Меняем статус
            items[item_index]['collected'] = not current_collected
            
            # Обновляем значок статуса
            new_status = "✓" if not current_collected else "○"
            self.tree.item(item_id, values=(
                item_values[0],  # #
                new_status,     # Статус
                item_values[2], # Название
                item_values[3], # Регион
                item_values[4], # Тип
                item_values[5], # X
                item_values[6], # Y
                item_values[7], # Добавлен
                item_values[8], # Примечания
                ""              # Действия
            ))
            
            # Обновляем цвет текста
            if not current_collected:
                self.tree.item(item_id, tags=("collected",))
            else:
                self.tree.item(item_id, tags=("uncollected",))
            
            # Обновляем статистику
            self.update_stats()
            
            # Меняем текст кнопки в зависимости от общего статуса
            stats = self.tracker.get_collected_stats()
            if stats['collected'] == stats['total'] and stats['total'] > 0:
                self.toggle_button.config(text="Все выполнено")
            elif stats['collected'] == 0:
                self.toggle_button.config(text="Выполнить все")
            else:
                self.toggle_button.config(text="Выполнено")
            
            # Показываем сообщение о результате
            action = "помечен как выполненный" if not current_collected else "снят с выполнения"
            messagebox.showinfo("Успех", f"Предмет '{items[item_index]['name']}' {action}!")
        else:
            messagebox.showerror("Ошибка", "Не удалось найти выбранный предмет.")


class AddEditItemWindow:
    """
    Окно для добавления или редактирования предмета.
    Показывается как отдельное модальное окно.
    """
    
    def __init__(self, parent, tracker, main_window, mode="add", item=None):
        """
        Инициализация окна добавления/редактирования.
        
        Параметры:
            parent: Родительское окно
            tracker: Экземпляр ItemTracker
            main_window: Ссылка на главное окно для обновления
            mode: "add" или "edit"
            item: Данные предмета при редактировании
        """
        self.parent = parent
        self.tracker = tracker
        self.main_window = main_window
        self.mode = mode
        self.item = item
        
        # Создаем новое окно
        self.window = tk.Toplevel(parent)
        self.window.title("Добавить предмет" if mode == "add" else "Редактировать предмет")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.transient(parent)  # Делаем окно зависимым от родителя
        self.window.grab_set()  # Делаем модальным
        
        # Центрируем относительно родительского окна
        self.center_window()
        
        # Создаем элементы интерфейса
        self.create_widgets()
        
        # Если режим редактирования, заполняем поля
        if mode == "edit" and item:
            self.fill_fields()

    def center_window(self):
        """Центрирует окно относительно родительского."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Создает элементы интерфейса для окна добавления/редактирования."""
        # Основной фрейм с отступами
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Форма ввода
        row = 0
        
        # Название
        ttk.Label(main_frame, text="Название: *", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            main_frame, 
            textvariable=self.name_var,
            font=("TkDefaultFont", 10)
        )
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        # Регион
        ttk.Label(main_frame, text="Регион: *", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.region_var = tk.StringVar()
        self.region_combo = ttk.Combobox(
            main_frame,
            textvariable=self.region_var,
            values=self.tracker.regions,
            state="readonly",
            font=("TkDefaultFont", 10)
        )
        self.region_combo.pack(fill="x", pady=(0, 15))
        
        # Тип предмета
        ttk.Label(main_frame, text="Тип предмета: *", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.type_var = tk.StringVar()
        item_types = ["Сундук", "Ресурс", "Задание", "Артефакт", "Оружие", "Другое"]
        self.type_combo = ttk.Combobox(
            main_frame,
            textvariable=self.type_var,
            values=item_types,
            state="readonly",
            font=("TkDefaultFont", 10)
        )
        self.type_combo.pack(fill="x", pady=(0, 15))
        
        # Координаты
        coord_frame = ttk.LabelFrame(main_frame, text="Координаты на карте", padding="15")
        coord_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(coord_frame, text="X:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="e", padx=(0, 10))
        self.x_var = tk.StringVar()
        ttk.Entry(
            coord_frame,
            textvariable=self.x_var,
            width=10,
            font=("TkDefaultFont", 10)
        ).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(coord_frame, text="Y:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, sticky="e", padx=(0, 10))
        self.y_var = tk.StringVar()
        ttk.Entry(
            coord_frame,
            textvariable=self.y_var,
            width=10,
            font=("TkDefaultFont", 10)
        ).grid(row=0, column=3)
        
        # Статус (только для редактирования)
        if self.mode == "edit" and self.item:
            status_frame = ttk.LabelFrame(main_frame, text="Статус", padding="15")
            status_frame.pack(fill="x", pady=(0, 15))
            
            self.collected_var = tk.BooleanVar(value=self.item['collected'])
            ttk.Checkbutton(
                status_frame,
                text="Предмет получен",
                variable=self.collected_var,
                font=("TkDefaultFont", 10)
            ).pack(anchor="w")
        
        # Примечания
        ttk.Label(main_frame, text="Примечания:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.notes_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            font=("TkDefaultFont", 10)
        )
        self.notes_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.window.destroy
        ).pack(side="right", padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_item
        ).pack(side="right")
        
        # Устанавливаем фокус на поле названия
        self.name_entry.focus()
        
        # Привязываем Enter к сохранению
        self.window.bind("<Return>", lambda e: self.save_item())
        
        # Привязываем Escape к отмене
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def fill_fields(self):
        """Заполняет поля данными редактируемого предмета."""
        self.name_var.set(self.item['name'])
        self.region_var.set(self.item['region'])
        self.type_var.set(self.item['type'])
        self.x_var.set(str(self.item['x']))
        self.y_var.set(str(self.item['y']))
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(1.0, self.item['notes'])

    def save_item(self):
        """Сохраняет введенные данные."""
        # Собираем данные
        name = self.name_var.get().strip()
        region = self.region_var.get().strip()
        item_type = self.type_var.get().strip()
        
        # Валидация обязательных полей
        if not name:
            messagebox.showerror("Ошибка", "Введите название предмета!")
            self.name_entry.focus()
            return
            
        if not region:
            messagebox.showerror("Ошибка", "Выберите регион!")
            self.region_combo.focus()
            return
            
        if not item_type:
            messagebox.showerror("Ошибка", "Выберите тип предмета!")
            self.type_combo.focus()
            return

        # Валидация координат
        try:
            x = float(self.x_var.get().strip())
            if not (-1000 <= x <= 1000):
                raise ValueError("X вне допустимого диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную координату X (-1000 до 1000)!")
            return

        try:
            y = float(self.y_var.get().strip())
            if not (-1000 <= y <= 1000):
                raise ValueError("Y вне допустимого диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную координату Y (-1000 до 1000)!")
            return

        # Примечания
        notes = self.notes_text.get(1.0, tk.END).strip()

        if self.mode == "add":
            # Добавляем новый предмет
            success = self.tracker.add_item(name, region, x, y, item_type)
            if success:
                messagebox.showinfo("Успех", f"Предмет '{name}' успешно добавлен!")
                self.window.destroy()
                self.main_window.refresh_items()  # Обновляем главное окно
            else:
                messagebox.showwarning("Предупреждение", "Не удалось добавить предмет. Возможно, он уже существует.")
        
        else:  # edit mode
            # Находим индекс предмета в полном списке
            all_items = self.tracker.get_all_items()
            try:
                # Найдем предмет по совпадению данных
                item_index = None
                for i, item in enumerate(all_items):
                    if (item['name'] == self.item['name'] and 
                        item['region'] == self.item['region'] and 
                        abs(item['x'] - self.item['x']) < 0.1 and 
                        abs(item['y'] - self.item['y']) < 0.1):
                        item_index = i
                        break
                
                if item_index is not None:
                    # Обновляем данные
                    all_items[item_index]['name'] = name
                    all_items[item_index]['region'] = region
                    all_items[item_index]['type'] = item_type
                    all_items[item_index]['x'] = x
                    all_items[item_index]['y'] = y
                    all_items[item_index]['notes'] = notes
                    all_items[item_index]['collected'] = self.collected_var.get()
                    
                    messagebox.showinfo("Успех", f"Предмет '{name}' успешно обновлен!")
                    self.window.destroy()
                    self.main_window.refresh_items()  # Обновляем главное окно
                else:
                    messagebox.showerror("Ошибка", "Не удалось найти предмет для редактирования.")
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить предмет: {e}")


def main():
    """Запускает графический интерфейс."""
    root = tk.Tk()
    app = GenshinTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()