import tkinter as tk
import threading


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.root.title("Option Monitor App")

        self.setup_ui()

    # ------------------------------------------
    # UI setup
    # ------------------------------------------
    def setup_ui(self):
        # Boton conectar
        btn_connect = tk.Button(self.root, text="Connect", command=self.service.connect)
        btn_connect.pack()

        # Boton posiciones
        btn_positions = tk.Button(
            self.root, text="Get Positions", command=self.fetch_positions
        )
        btn_positions.pack()

    # ------------------------------------------
    # Thread Wrapper
    # ------------------------------------------
    def fetch_positions(self):
        threading.Thread(target=self.render_positions, daemon=True).start()

    # --------------------------------------------
    # Logica
    # --------------------------------------------
    def render_positions(self):
        positions = self.service.get_positions()

        # Volver al hilo principal
        self.root.after(0, lambda: self.display_positions(positions))

    # ---------------------------------------------
    # Render
    # ---------------------------------------------
    def display_positions(self, positions):
        print("Positions")
        for p in positions:
            print(p)

    # ----------------------------------------------
    # Run the app
    # ----------------------------------------------
    def run(self):
        self.root.mainloop()
