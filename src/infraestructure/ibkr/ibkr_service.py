import threading
import time
from src.core.models.position import Position


class IbkrService:
    def __init__(self, client):
        self.client = client
        self.thread = None

    # Connection
    def connect(self, host="127.0.0.1", port=7496, client_id=1):
        if self.client.is_connected:
            return

        if self.thread and self.thread.is_alive():
            return

        # Intentamos conectar a la api de ibkr
        self.client.connect(host, port, client_id)

        self.thread = threading.Thread(target=self.client.run, daemon=True)
        self.thread.start()

        start = time.time()

        # Esperar la coneccion
        while not self.client.is_connected:
            if time.time() - start > 5:
                raise TimeoutError("IBKR could not connect. Timeout")
            time.sleep(0.1)

    def disconnect(self):
        if self.client.is_connected:
            self.client.disconnect()
            self.thread = None  # Necesario resetear el threat
            self.client.is_connected = False

    # ----------------------------------------
    # Posiciones (sync wrapper)
    # ----------------------------------------
    def get_positions(self):
        # Chequear que api esta conectada
        if not self.client.is_connected:
            raise ConnectionError("Not Connected to IBKR")
        # Reset estado
        self.client.positions = []
        self.client.positions_done = False

        self.client.reqPositions()

        start = time.time()

        # Esperar respuesta
        while not self.client.positions_done:
            if time.time() - start > 5:
                raise TimeoutError("IBKR positions timeout")
            time.sleep(0.1)

        print("Positions:", self.client.positions)

        return [
            Position(
                con_id=p["conId"],
                symbol=p["symbol"],
                sec_type=p["secType"],
                strike=p["strike"],
                position=p["position"],
                avg_cost=p["avgCost"],
            )
            for p in self.client.positions
        ]
