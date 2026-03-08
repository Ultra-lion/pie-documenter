import tkinter as tk


class DatabaseDetailPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_btn = tk.Button(
            self,
            text="← Back to Main",
            command=lambda: controller.show_page("MainPage"),
            font=("Arial", 10)
        )
        back_btn.pack(anchor="nw", padx=10, pady=10)

        self.title_label = tk.Label(
            self,
            text="Database: ",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True)

        functions_btn = tk.Button(
            button_frame,
            text="See Functions",
            command=lambda: self.show_list_page("FunctionsPage"),
            bg="#2196F3",
            fg="white",
            font=("Arial", 14),
            width=20,
            height=2
        )
        functions_btn.pack(pady=15)

        classes_btn = tk.Button(
            button_frame,
            text="See Classes",
            command=lambda: self.show_list_page("ClassesPage"),
            bg="#FF9800",
            fg="white",
            font=("Arial", 14),
            width=20,
            height=2
        )
        classes_btn.pack(pady=15)

        methods_btn = tk.Button(
            button_frame,
            text="See Class Methods",
            command=lambda: self.show_list_page("ClassMethodsPage"),
            bg="#9C27B0",
            fg="white",
            font=("Arial", 14),
            width=20,
            height=2
        )
        methods_btn.pack(pady=15)

    def update_database_name(self, db_name):
        self.db_name = db_name
        self.title_label.config(text=f"Database: {db_name}")

    def show_list_page(self, page_name):
        self.controller.pages[page_name].load_data(self.db_name)
        self.controller.show_page(page_name)
