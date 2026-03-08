import tkinter as tk
from tkinter import Canvas, Scrollbar
from pathlib import Path
import networkx as nx
from src.utils.utils import retrieve_neighbours_of_a_node


class ShowGraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_btn = tk.Button(
            self,
            text="← Back",
            command=self.go_back,
            font=("Arial", 10)
        )
        back_btn.pack(anchor="nw", padx=10, pady=10)

        self.title_label = tk.Label(
            self,
            text="Graph Visualization",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=10)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.info_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 12),
            justify=tk.LEFT
        )
        self.info_label.pack(pady=10)

        scrollbar_y = Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar_x = Scrollbar(main_frame, orient=tk.HORIZONTAL)
        
        self.canvas = Canvas(
            main_frame,
            bg="white",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.canvas.yview)
        scrollbar_x.config(command=self.canvas.xview)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.previous_page = None

    def go_back(self):
        if self.previous_page:
            self.controller.show_page(self.previous_page)
        else:
            self.controller.show_page("DatabaseDetailPage")

    def load_graph(self, node_name, db_name, previous_page):
        self.previous_page = previous_page
        self.title_label.config(text=f"Graph for: {node_name}")
        
        db_path = f"pie-databases/{db_name}"
        project_dir = str(Path(db_path).parent.parent / db_name)
        
        neighbors = retrieve_neighbours_of_a_node(project_dir, node_name)
        
        self.canvas.delete("all")
        
        if not neighbors:
            self.info_label.config(
                text=f"Node: {node_name}\nNo neighbors found"
            )
            self.canvas.create_text(
                400, 300,
                text="No neighbors to display",
                font=("Arial", 14),
                fill="gray"
            )
            return

        self.info_label.config(
            text=f"Node: {node_name}\nNeighbors: {len(neighbors)}"
        )
        
        G = nx.Graph()
        G.add_node(node_name)
        
        edges_info = []
        for neighbor in neighbors:
            neighbor_name = neighbor['properties']['name']
            G.add_node(neighbor_name)
            G.add_edge(node_name, neighbor_name)
            
            rel_type = neighbor.get('rel_type', 'UNKNOWN')
            edges_info.append((node_name, neighbor_name, rel_type))
        
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        width = max(800, len(neighbors) * 50)
        height = max(600, len(neighbors) * 40)
        self.canvas.config(scrollregion=(0, 0, width, height))
        
        scale_x = width / 2
        scale_y = height / 2
        offset_x = width / 2
        offset_y = height / 2
        
        for (n1, n2, rel_type) in edges_info:
            x1 = pos[n1][0] * scale_x + offset_x
            y1 = pos[n1][1] * scale_y + offset_y
            x2 = pos[n2][0] * scale_x + offset_x
            y2 = pos[n2][1] * scale_y + offset_y
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="gray",
                width=2,
                arrow=tk.LAST
            )
            
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            self.canvas.create_text(
                mid_x, mid_y - 10,
                text=rel_type,
                font=("Arial", 8),
                fill="blue"
            )
        
        for node in G.nodes():
            x = pos[node][0] * scale_x + offset_x
            y = pos[node][1] * scale_y + offset_y
            
            if node == node_name:
                color = "#FF5722"
                radius = 30
            else:
                color = "#2196F3"
                radius = 25
            
            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=color,
                outline="black",
                width=2
            )
            
            self.canvas.create_text(
                x, y,
                text=node,
                font=("Arial", 9, "bold"),
                fill="white",
                width=radius * 2 - 10
            )
