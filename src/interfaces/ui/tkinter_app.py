from decimal import Decimal
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import List
from src.core.models.position import Position


class TkinterApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        # self.style = ttk.Style()
        self.root.title("Option Monitor App")
        self.root.geometry("800x600")

        self.positions = []

        self.setup_ui()

    # ------------------------------------------
    # Funciones asincronicas
    # ------------------------------------------
    def connect_terminal(self):
        threading.Thread(target=self.connect_service, daemon=True).start()

    def disconnect_terminal(self):
        threading.Thread(target=self.disconnect_service, daemon=True).start()

    def refresh_positions(self):
        threading.Thread(target=self.fetch_positions, daemon=True).start()

    ##Servicios
    # Conectar | desconectar servicio
    def connect_service(self):
        try:
            # Conectamos a ibkr
            self.service.connect()
            self.root.after(0, lambda: self.show_message("Connected to TWS"))
            self.btn_connect.config(state="disabled")
            self.btn_disconnect.config(state="normal")
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    def disconnect_service(self):
        try:
            self.service.disconnect()
            self.root.after(0, lambda: self.show_message("Disconnected from TWS"))
            self.btn_disconnect.config(state="disabled")
            self.btn_connect.config(state="normal")
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    def fetch_positions(self):
        try:
            self.positions = self.service.get_positions()
            self.root.after(0, lambda: self.update_ui())
        except Exception as e:
            self.root.after(0, lambda err=e: self.show_error(str(err)))

    def update_ui(self):
        self.show_message("Positions refreshed")
        self.fill_table(self.positions)

    def fill_table(self, positions: List):
        for p in positions:

            margen = 1000
            multiplier = getattr(p, "multiplier", 100)
            totalCost = p.avg_cost * float(multiplier)  # aqui es Price * 100 + fee
            last = 0  # Se toma de otra funcion de ibkr api
            delta = 0  #
            market_value = last * multiplier * p.position
            cost_basis = p.avg_cost * multiplier * p.position
            net_credit = totalCost * p.position
            pnl = market_value - cost_basis
            pnl_pct = pnl / abs(cost_basis) * 100
            max_loss = margen - net_credit
            self.table.insert(
                "",
                "end",
                values=(
                    p.id,
                    p.symbol,
                    p.strike,
                    p.position,
                    p.avg_cost,
                    last,
                    delta,
                    pnl_pct,
                    net_credit,
                    max_loss,
                ),
            )

    ## Helpers functions
    def show_message(self, msg):
        self.status_label.config(text=msg, foreground="green")

    def show_error(self, msg):
        self.status_label.config(text=msg, foreground="red")
        print("Error: ", msg)

    # ------------------------------------------
    # UI setup
    # ------------------------------------------
    def setup_ui(self):

        ## Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=1)

        title_label = ttk.Label(main_frame, text="Monitor de opciones")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 0))

        ## sections
        self.setup_connection_section(main_frame, 1)
        self.setup_positions_section(main_frame, 2)

    def setup_connection_section(self, parent, row):
        conn_frame = ttk.LabelFrame(
            parent, text="Interactive Brokers Connection", padding="15"
        )
        conn_frame.grid(row=row, column=0, sticky="nswe", pady=(15, 0))
        conn_frame.columnconfigure(0, weight=1)
        # conn_section.columnconfigure(3, weight=1)  -- Para imputs

        ttk.Label(conn_frame, text="Host: 127.0.0.1 | Port: 7496").grid(
            row=0, column=0, padx=(0, 5), sticky="we"
        )

        # Botones - conectar | desconectar
        btn_frame = ttk.Frame(conn_frame)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0))

        self.btn_connect = ttk.Button(
            btn_frame,
            text="Connect",
            command=self.connect_terminal,
        )

        self.btn_connect.pack(side="left", padx=(0, 10))

        self.btn_disconnect = ttk.Button(
            btn_frame,
            text="Disconnect",
            command=self.disconnect_terminal,
            state="disabled",
        )
        self.btn_disconnect.pack(side="left")

        # Refresh positions
        btn_refresh = ttk.Button(
            btn_frame, text="Refresh Positions", command=self.refresh_positions
        )

        btn_refresh.pack(side="left", padx=(10, 0))

        self.status_label = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=4, pady=(5, 0))

    def setup_positions_section(self, parent, row):
        # Monitor
        monitor_frame = ttk.LabelFrame(parent, text="Options Monitor", padding="10")
        monitor_frame.grid(row=row, column=0, sticky=("nswe"), pady=(15, 0))
        monitor_frame.columnconfigure(0, weight=1)
        monitor_frame.rowconfigure(0, weight=1)

        ## Tabla de posiciones
        columns = (
            "id",
            "symbol",
            "strike",
            "position",
            "avg_cost",
            "last",
            "delta",
            "p_l_trade",
            "net_credit",
            "max_loss",
        )
        self.table = ttk.Treeview(monitor_frame, columns=columns, show="headings")

        # id
        # symbol
        # strike
        # position
        # avgCost
        # last
        # delta
        # p_l_trade
        # net_credit
        # max_loss
        # titulos columnas
        self.table.heading("id", text="id")
        self.table.heading("symbol", text="Symbol")
        self.table.heading("strike", text="Strike")
        self.table.heading("position", text="Position")
        self.table.heading("avg_cost", text="avgCost")
        self.table.heading("last", text="Last")
        self.table.heading("delta", text="Delta")
        self.table.heading("p_l_trade", text="P/L x trade")
        self.table.heading("net_credit", text="Net cretid")
        self.table.heading("max_loss", text="Max loss")
        # Insertar datos

        self.table.grid(row=0, column=0, sticky="nsew")

    # ----------------------------------------------
    # Run the app
    # ----------------------------------------------
    def run(self):
        self.root.mainloop()
