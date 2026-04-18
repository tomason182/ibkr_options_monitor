import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import List
from src.core.models.position import Position


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.style = ttk.Style()
        self.root.title("Option Monitor App")

        # Variables globales
        self.style.configure("Custom.Title", foreground=self.text_color, font=("Arial", 18, "bold"))
        self.style.configure("subtile", foreground=self.text_color, font=("Arial", 14, "bold"))
        self.style.configure("font_body", fg=self.text_color, font=("Arial", 12))
        self.style.configure("font_body_bold", fg=self.text_color, font=("Arial", 12, "bold"))
        
        self.font_small = ("Arial", 10)
        self.font_bottom = ("Arial", 11, "bold")
        self.font_error = ("Arial", 12, "bold")
        self.font_success = ("Arial", 12, "bold")

        self.color_error = "red"
        self.text_color = "black"
        self.success = "green"
        self.color_mute = "gray"

        self.setup_ui()

    # ------------------------------------------
    # Funciones asincronicas
    # ------------------------------------------
    def connect_terminal(self):
        threading.Thread(target=self.connect_service, daemon=True).start()

    def fetch_positions(self):
        threading.Thread(target=self.render_positions, daemon=True).start()

    ##Servicios
    # Conectar con servicio
    def connect_service(self):
        try:
            self.service.connect()
            self.root.after(0, lambda: self.show_message("Connected to TWS"))
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    def render_positions(self):
        try:
            positions = (
                self.service.get_positions()
            )  #! Positions deberia tener un tipo.
            self.root.after(0, lambda: self.display_positions(positions))
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    ##Render
    # ---------------------------------------------
    def display_positions(self, positions: List[Position]):
        print("Positions")
        for p in positions:
            print(p)

    ## Helpers functions
    def show_message(self, msg):
        self.status_label.config(text=msg)

    def show_error(self, msg):
        self.status_label.config(text=msg, fg="red")
        print("Error: ", msg)

    # ------------------------------------------
    # UI setup
    # ------------------------------------------
    def setup_ui(self):

        ## Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="wens")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title_label = ttk.Label(
            main_frame, text="Monitor de opciones", style="Custom.Title"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0,20))

        ## sections 
        self.setup_connection_section(main_frame,1 )
        self.setup_positions_section(main_frame, 2)
        
        
    def setup_connection_section(self, parent, row):
        conn_section = ttk.LabelFrame(parent, text="Interactive Brokers Connection", padding="15")
        conn_section.grid(row=row, column=0, sticky="we", pady=(0,15))
        conn_section.columnconfigure(1,weight=1)
        #conn_section.columnconfigure(3, weight=1)  -- Para imputs

        ttk.Label(conn_section, text="Host: 127.0.0.1, Port: 7496").grid(row=0, column=0, padx=(0,5), sticky="w")


        # Boton conectar
        btn_connect = ttk.Button(
            parent,
            text="Connect",
            height=1,
            width=12,
            bg="#0f941e",
            command=self.connect_terminal,
        )

        btn_connect.grid(row=0, column=0, sticky="w")

        # Estado

        status_title = tk.Label(
            frame_connect, text="Status", font=self.font_subtitle, fg=self.text_color
        )
        status_title.grid(sticky="ne")

        self.status_label = tk.Label(
            frame_connect,
            text="Disconected",
            fg="red",
            font=self.font_small,
            bg=self.color_mute,
        )
        self.status_label.grid(sticky="se")

        # Monitor
        frame_monitor = tk.Frame(self.root, bd=2, relief="solid")
        frame_monitor.grid(row=2, column=0)

        # Boton posiciones
        btn_positions = tk.Button(
            frame_monitor, text="Get Positions", command=self.fetch_positions
        )

        btn_positions.pack()

    # ----------------------------------------------
    # Run the app
    # ----------------------------------------------
    def run(self):
        self.root.mainloop()
