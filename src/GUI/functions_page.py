import tkinter as tk
from pathlib import Path
from src.utils.utils import load_graph, get_all_functions


class FunctionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_page = 0
        self.page_size = 20

        back_btn = tk.Button(
            self,
            text="← Back",
            command=lambda: controller.show_page("DatabaseDetailPage"),
            font=("Arial", 10)
        )
        back_btn.pack(anchor="nw", padx=10, pady=10)

        title = tk.Label(
            self,
            text="Functions",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        self.listbox = tk.Listbox(
            self,
            width=80,
            height=20,
            font=("Arial", 11)
        )
        self.listbox.pack(pady=10, padx=20)
        self.listbox.bind('<Double-Button-1>', self.show_graph)

        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        self.prev_btn = tk.Button(
            nav_frame,
            text="← Previous",
            command=self.previous_page,
            font=("Arial", 10)
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(
            nav_frame,
            text="Page 1",
            font=("Arial", 10)
        )
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.next_btn = tk.Button(
            nav_frame,
            text="Next →",
            command=self.next_page,
            font=("Arial", 10)
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

    def load_data(self, db_name):
        self.db_name = db_name
        db_path = f"pie-databases/{db_name}"
        project_dir = str(Path(db_path).parent.parent / db_name)
        self.graph = load_graph(project_dir)
        self.current_page = 0
        self.display_page()

    def display_page(self):
        self.listbox.delete(0, tk.END)
        offset = self.current_page * self.page_size
        functions = get_all_functions(
            self.graph,
            offset=offset,
            limit=self.page_size
        )

        if not functions:
            self.listbox.insert(tk.END, "No functions found")
            self.next_btn.config(state=tk.DISABLED)
        else:
            for func in functions:
                self.listbox.insert(tk.END, func)
            if len(functions) < self.page_size:
                self.next_btn.config(state=tk.DISABLED)
            else:
                self.next_btn.config(state=tk.NORMAL)

        self.prev_btn.config(
            state=tk.NORMAL if self.current_page > 0 else tk.DISABLED
        )
        self.page_label.config(text=f"Page {self.current_page + 1}")

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_page(self):
        self.current_page += 1
        self.display_page()

    def show_graph(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        func_name = self.listbox.get(selection[0])
        if func_name == "No functions found":
            return

        self.controller.show_graph(func_name, self.db_name)
