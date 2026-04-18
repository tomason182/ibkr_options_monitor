import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import List
from src.core.models.position import Position


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        #self.style = ttk.Style()
        self.root.title("Option Monitor App")

        # Variables globales
        #self.style.configure("Custom.Title", foreground=self.text_color, font=("Arial", 18, "bold"))
        #self.style.configure("subtile", foreground=self.text_color, font=("Arial", 14, "bold"))
        
        #self.style.configure("font_body", fg=self.text_color, font=("Arial", 12))
        #self.style.configure("font_body_bold", fg=self.text_color, font=("Arial", 12, "bold"))
        
        #self.font_small = ("Arial", 10)
        #self.font_bottom = ("Arial", 11, "bold")
        #self.font_error = ("Arial", 12, "bold")
        #self.font_success = ("Arial", 12, "bold")

        #self.color_error = "red"
        #self.text_color = "black"
        #self.success = "green"
        #self.color_mute = "gray"

        self.setup_ui()

    # ------------------------------------------
    # Funciones asincronicas
    # ------------------------------------------
    def connect_terminal(self):
        threading.Thread(target=self.connect_service, daemon=True).start()

    def disconnect_terminal(self):
        threading.Thread(target=self.disconnect_service, daemon=True).start()

    def fetch_positions(self):
        threading.Thread(target=self.render_positions, daemon=True).start()

    ##Servicios
    # Conectar | desconectar servicio
    def connect_service(self):
        try:
            self.service.connect()
            self.root.after(0, lambda: self.show_message("Connected to TWS"))
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    def disconnect_service(self):
        try:
            self.service.disconnect()
            self.root.after(0, lambda: self.show_message("Disconnected from TWS"))
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
        self.status_label.config(text=msg)
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
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=1)

        title_label = ttk.Label(
            main_frame, text="Monitor de opciones"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0,0))

        ## sections 
        self.setup_connection_section(main_frame,1 )
        self.setup_positions_section(main_frame, 2)
        

    

    def setup_connection_section(self, parent, row):
        conn_frame = ttk.LabelFrame(parent, text="Interactive Brokers Connection", padding="15")
        conn_frame.grid(row=row, column=0, sticky="nswe", pady=(15, 0))
        conn_frame.columnconfigure(0,weight=1)
        #conn_section.columnconfigure(3, weight=1)  -- Para imputs

        ttk.Label(conn_frame, text="Host: 127.0.0.1 | Port: 7496").grid(row=0, column=0, padx=(0,5), sticky="we")


        # Botones - conectar | desconectar
        btn_frame = ttk.Frame(conn_frame)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=(10,0))

        btn_connect = ttk.Button(
            btn_frame,
            text="Connect",
            command=self.connect_terminal,
        )

        btn_connect.pack(side="left", padx=(0,10))

        btn_disconnect = ttk.Button(btn_frame, text="Disconnect", command=self.disconnect_terminal, state="disable")
        btn_disconnect.pack(side="left")

                # Refresh positions
        btn_refresh = ttk.Button(
            btn_frame, text="Refresh Positions", command=self.fetch_positions
        )

        btn_refresh.pack(side="left", padx=(10,0))


        self.status_label = ttk.Label(
            conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=4, pady=(5,0))

    def setup_positions_section(self, parent, row):
        # Monitor
        monitor_frame = ttk.LabelFrame(parent, text="Options Monitor", padding="10")
        monitor_frame.grid(row=row, column=0, sticky=("nwe"), pady=(15))
        monitor_frame.columnconfigure(0, weight=1)


        ## Tabla de posiciones
        columns = ("id", "description","type", "strike", "position", "price", "total",  "last", "delta", "%_p_l_trade", "net_credit", "max_loss")
        table = ttk.Treeview(monitor_frame, columns=columns, show="headings")

        # titulos columnas
        table.heading("id", text="id")
        table.heading("description", text="Description")
        table.heading("type", text="Type")
        table.heading("strike", text="Strike")
        table.heading("position", text="Position")
        table.heading("price", text="Price")
        table.heading("total", text="Total")                # total = price * 100 + fee
        table.heading("last", text="Last")
        table.heading("delta", text="Delta")
        table.heading("%_p_l_trade", text="P/L x trade")
        table.heading("net_credit", text="Net cretid")
        table.heading("max_loss", text="Max loss")
        # Insertar datos



        table.pack()




    # ----------------------------------------------
    # Run the app
    # ----------------------------------------------
    def run(self):
        self.root.mainloop()
