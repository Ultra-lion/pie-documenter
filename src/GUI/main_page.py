import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
from src.parser.parser import node_ingester, linker

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        title = tk.Label(self, text="PIE Documenter - Database Manager", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        import_btn = tk.Button(
            self, 
            text="Import New Database", 
            command=self.import_database,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10
        )
        import_btn.pack(pady=10)
        
        databases_label = tk.Label(self, text="Existing Databases:", font=("Arial", 14, "bold"))
        databases_label.pack(pady=(20, 10))
        
        self.db_listbox = tk.Listbox(self, width=60, height=15, font=("Arial", 11))
        self.db_listbox.pack(pady=10, padx=20)
        self.db_listbox.bind('<Double-Button-1>', self.open_database)
        
        refresh_btn = tk.Button(
            self,
            text="Refresh Database List",
            command=self.refresh_databases,
            font=("Arial", 10)
        )
        refresh_btn.pack(pady=10)
        
        self.refresh_databases()
    
    def refresh_databases(self):
        self.db_listbox.delete(0, tk.END)
        db_folder = Path("pie-databases")
        if db_folder.exists():
            db_files = list(db_folder.glob("*.db"))
            if db_files:
                for db_file in sorted(db_files):
                    self.db_listbox.insert(tk.END, db_file.stem)
            else:
                self.db_listbox.insert(tk.END, "No databases found")
        else:
            self.db_listbox.insert(tk.END, "No databases folder found")
    
    def import_database(self):
        project_path = filedialog.askdirectory(title="Select Project Directory to Import")
        if not project_path:
            return
        
        progress_window = tk.Toplevel(self)
        progress_window.title("Importing Database")
        progress_window.geometry("400x150")
        
        label = tk.Label(progress_window, text="Importing project...\nThis may take a few moments.", font=("Arial", 11))
        label.pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=300)
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        def import_thread():
            try:
                node_ingester(project_path)
                linker(project_path)
                
                progress_window.destroy()
                messagebox.showinfo("Success", f"Database imported successfully!\nProject: {Path(project_path).name}")
                self.refresh_databases()
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("Error", f"Failed to import database:\n{str(e)}")
        
        thread = threading.Thread(target=import_thread, daemon=True)
        thread.start()
    
    def open_database(self, event):
        selection = self.db_listbox.curselection()
        if not selection:
            return
        
        db_name = self.db_listbox.get(selection[0])
        if db_name in ["No databases found", "No databases folder found"]:
            return
        
        self.controller.set_current_database(db_name)
        self.controller.show_page("DatabaseDetailPage")



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PIE Documenter")
        self.geometry("900x700")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self.current_database = None

        from src.GUI.database_detail_page import DatabaseDetailPage
        from src.GUI.functions_page import FunctionsPage
        from src.GUI.classes_page import ClassesPage
        from src.GUI.class_methods_page import ClassMethodsPage
        from src.GUI.show_graph import ShowGraphPage

        for page in (MainPage, DatabaseDetailPage, FunctionsPage,
                     ClassesPage, ClassMethodsPage, ShowGraphPage):
            page_name = page.__name__
            frame = page(container, self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("MainPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def set_current_database(self, db_name):
        self.current_database = db_name
        self.pages["DatabaseDetailPage"].update_database_name(db_name)

    def show_graph(self, node_name, db_name):
        current_page = None
        for page_name, page in self.pages.items():
            try:
                if page.winfo_viewable():
                    current_page = page_name
                    break
            except:
                pass

        if current_page is None:
            current_page = "DatabaseDetailPage"

        self.pages["ShowGraphPage"].load_graph(
            node_name,
            db_name,
            current_page
        )
        self.show_page("ShowGraphPage")