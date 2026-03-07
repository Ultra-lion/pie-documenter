import tkinter as tk

class MainPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        label = tk.Label(self, text="PIE Page")
        label.pack(pady=10)
        button = tk.Button(self, text="Press For Fun")
        button.pack()



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        container = tk.Frame(self)
        container.pack(fill="both",expand=True)
        self.pages = {}
        for page in (MainPage,):
            page_name = page.__name__
            frame = page(container,self)
            self.pages[page_name] = frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_page("MainPage")
    
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()