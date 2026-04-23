import threading
import time
from src.core.models.position import Position


class IbkrService:
    def __init__(self, client, worker):
        self.client = client
        self.worker = worker
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

        if not self.client.connected_event.wait(timeout=5):
            raise TimeoutError("Connection timeout")

        print("Connected to tws")

    def disconnect(self):
        # Pregunta para Chat: ¿aqui, al desconectar, deberiamos hacer self.theard.clear()?
        if self.client.is_connected:
            self.client.disconnect()
            self.worker.stop()

        if self.thread:
            self.thread.join(timeout=2)
        self.thread = None

    # ----------------------------------------
    # Posiciones (event driven)
    # ----------------------------------------
    def get_positions(self):
        if not self.client.is_connected:
            raise ConnectionError("Not Connected to IBKR")
        # Reset estado
        self.client.positions = []
        self.client.positions_event.clear()

        self.client.reqPositions()

        if not self.client.positions_event.wait(timeout=5):
            raise TimeoutError("Positions timeout")

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

    # ------------------------------------------
    # Execuciones
    # ------------------------------------------
    def get_executions(self):
        if not self.client.is_connected:
            raise ConnectionError("Not connected to TWS api")

        self.client.requestExecutions()

        return
