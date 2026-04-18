import tkinter as tk
import threading
from typing import List
from src.core.models.position import Position


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.root.title("Option Monitor App")

        # Variables globales
        self.font_title = ("Arial", 18, "bold")
        self.font_subtitle = ("Arial", 14, "bold")
        self.font_body = ("Arial", 12)
        self.font_body_bold = ("Arial", 12, "bold")
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

        ## Frame 1
        frame = tk.Frame(self.root, bd=1, relief="solid", height=100)
        frame.grid(row=0, column=0, sticky="we")
        self.root.columnconfigure(0, weight=1)

        frame.grid_propagate(False)
        # Nombre app
        title = tk.Label(
            frame, text="Monitor de opciones", font=self.font_title, fg=self.text_color
        )
        title.pack()

        ## Frame 2
        # Seccion Conectar api.
        frame_connect = tk.Frame(self.root, bd=1, relief="solid", height=220)
        frame_connect.grid(row=1, column=0, sticky="we")
        self.root.columnconfigure(0, weight=1)

        frame_connect.columnconfigure(0, weight=1)

        # Boton conectar
        btn_connect = tk.Button(
            frame_connect,
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
