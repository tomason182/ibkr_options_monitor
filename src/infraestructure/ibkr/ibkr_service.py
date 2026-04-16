import threading
import time
from core.models.position import Position


class IbkrService:
    def __init__(self, client):
        self.client = client
        self.thread = None

        # Connection
        def connect(self, host="127.0.0.1", port=7497, client_id=0):
            self.client.connect(host, port, client_id)

            self.thread = threading.Thread(target=self.client.run, daemon=True)
            self.thread.start()

            # Esperar la coneccion
            while not self.client.connected_flag:
                time.sleep(0.5)

        def disconnect(self):
            self.client.disconnect()

        # ----------------------------------------
        # Posiciones (sync wrapper)
        # ----------------------------------------
        def get_positions(self):
            # Reset estado
            self.client.positions = []
            self.client_positions_done = False

            self.client.reqPositions()

            # Esperar respuesta
            while not self.client.positions_done:
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
