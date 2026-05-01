import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

#Имя файла для хранения данных
DB_FILE = 'movies.json'


class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Личная кинотека")
        self.root.geometry("800x500")

        #Список для хранения данных о фильмах
        self.movies = self.load_data()

        self.create_widgets()
        self.refresh_table()

    def load_data(self):
        """Загрузка данных из JSON."""
        if not os.path.exists(DB_FILE):
            return []
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def save_data(self):
        """Сохранение данных в JSON."""
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        #Для ввода данных(архитектура)
        input_frame = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e")
        self.ent_title = tk.Entry(input_frame)
        self.ent_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="e")
        self.ent_genre = tk.Entry(input_frame)
        self.ent_genre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Год:").grid(row=1, column=0, sticky="e")
        self.ent_year = tk.Entry(input_frame)
        self.ent_year.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="e")
        self.ent_rating = tk.Entry(input_frame)
        self.ent_rating.grid(row=1, column=3, padx=5, pady=2)

        btn_add = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="#4CAF50", fg="white")
        btn_add.grid(row=0, column=4, rowspan=2, padx=20, ipadx=10, ipady=5)

        #Для фильтрации
        filter_frame = tk.Frame(self.root, padx=10, pady=5)
        filter_frame.pack(fill="x")

        tk.Label(filter_frame, text="Фильтр Жанр:").pack(side="left")
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Год:").pack(side="left")
        self.filter_year = tk.Entry(filter_frame, width=10)
        self.filter_year.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Применить", command=self.apply_filter).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.refresh_table).pack(side="left")

        #Таблица
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.column("year", width=100, anchor="center")
        self.tree.column("rating", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_movie(self):
        title = self.ent_title.get().strip()
        genre = self.ent_genre.get().strip()
        year_str = self.ent_year.get().strip()
        rating_str = self.ent_rating.get().strip()

        #Исключение ошибок
        if not (title and genre and year_str and rating_str):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        #Добавление
        new_movie = {
            "title": title,
            "genre": genre,
            "year": int(year_str),
            "rating": rating
        }
        self.movies.append(new_movie)
        self.save_data()
        self.refresh_table()

        #Очистка полей
        self.ent_title.delete(0, tk.END)
        self.ent_genre.delete(0, tk.END)
        self.ent_year.delete(0, tk.END)
        self.ent_rating.delete(0, tk.END)

    def refresh_table(self, data_to_show=None):
        """Обновление данных в таблице GUI."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_list = data_to_show if data_to_show is not None else self.movies

        for m in display_list:
            self.tree.insert("", "end", values=(m["title"], m["genre"], m["year"], m["rating"]))

    def apply_filter(self):
        f_genre = self.filter_genre.get().lower().strip()
        f_year = self.filter_year.get().strip()

        filtered = self.movies
        if f_genre:
            filtered = [m for m in filtered if f_genre in m["genre"].lower()]
        if f_year:
            filtered = [m for m in filtered if str(m["year"]) == f_year]

        self.refresh_table(filtered)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()