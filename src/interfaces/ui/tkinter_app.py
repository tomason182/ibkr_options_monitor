import tkinter as tk
import threading
from typing import List
from src.core.models.position import Position


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.root.title("Option Monitor App")

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
        print(msg)

    def show_error(self, msg):
        print("Error: ", msg)

    # ------------------------------------------
    # UI setup
    # ------------------------------------------
    def setup_ui(self):
        # Boton conectar
        btn_connect = tk.Button(
            self.root, text="Connect", command=self.connect_terminal
        )

        btn_connect.pack()

        # Boton posiciones
        btn_positions = tk.Button(
            self.root, text="Get Positions", command=self.fetch_positions
        )

        btn_positions.pack()

    # ----------------------------------------------
    # Run the app
    # ----------------------------------------------
    def run(self):
        self.root.mainloop()
