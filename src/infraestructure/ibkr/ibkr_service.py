import threading
import time
from src.core.models.position import Position


class IbkrService:
    def __init__(self, client):
        self.client = client
        self.thread = None

    # Connection
    def connect(self, host="127.0.0.1", port=7497, client_id=1):
        self.client.connect(host, port, client_id)

        self.thread = threading.Thread(target=self.client.run, daemon=True)
        self.thread.start()

        start = time.time()

        # Esperar la coneccion
        while not self.client.connected_flag:
            if time.time() - start > 5:
                raise TimeoutError("IBKR cound not connect. Timeout")
            time.sleep(0.1)

    def disconnect(self):
        self.client.disconnect()

    # ----------------------------------------
    # Posiciones (sync wrapper)
    # ----------------------------------------
    def get_positions(self):
        # Chequear que api esta conectada
        if not self.client.connected_flag:
            raise Exception("Not Connected to IBKR")
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

        return [
            Position(
                con_id=p["conId"],
                symbol=p["symbol"],
                sec_type=p["secType"],
                quantity=p["position"],
                avg_cost=p["avgCost"],
            )
            for p in self.client.positions
        ]
