from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime, timedelta
from decimal import Decimal


class IbkrClient(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

        # Estado interno
        self.connected_flag = False
        self.next_order_id = None

        # Posiciones
        self.positions = []
        self.positions_done = False

    # Manejar errores
    def error(
        self,
        reqId,
        errorTime: int,
        errorCode: int,
        errorString: str,
        advancedOrderRejectJson="",
    ):
        if errorCode == 2176 and "fractional share" in errorString.lower():
            return
        print(f"Error {errorCode}:{errorString}")

    # Para abrir posiciones usando la api debemos considerar nextValidId para que no se dupliquen los id de los trades
    # Por el momento la app no va a abrir posiciones desde la UI por lo tanto la vamos a usar para cambiar el estado de connected_flag
    def nextValidId(self, orderId: int):
        self.next_order_id = orderId
        self.connected_flag = True
        print("Connected to IBTWS")

    # Position callback (cada vez que se inicia la app, el servidor tws devuelve las posiciones
    def position(
        self, account: str, contract: Contract, position: Decimal, avgCost: float
    ):
        self.positions.append(
            {
                "conId": contract.conId,
                "symbol": contract.symbol,
                "secType": contract.secType,
                "position": Decimal(position),
                "avgCost": float(avgCost),
            }
        )

    def positionEnd(self):
        self.position_done = True
        print("Positions received")
