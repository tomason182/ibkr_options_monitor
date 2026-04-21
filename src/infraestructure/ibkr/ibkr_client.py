from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from decimal import Decimal
from queue import Queue


class IbkrClient(EClient, EWrapper):
    def __init__(self):
        super().__init__(self)

        # Estado interno
        self.is_connected = False
        self.next_order_id = None

        # Posiciones
        self.positions = []
        self.positions_done = False

        # Errores
        self.error_queue = Queue()

    # -----------------------------------
    # Errores
    # -----------------------------------

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

        msg = f"Error {errorCode}: {errorString}"
        self.error_queue.put(msg)

    # --------------------------------------
    # Connection
    # --------------------------------------

    def nextValidId(self, orderId: int):
        self.next_order_id = orderId
        self.is_connected = True

    # ------------------------------------------
    # Positions
    # ------------------------------------------
    def position(self, account: str, contract: Contract, position, avgCost: float):
        self.positions.append(
            {
                "conId": contract.conId,
                "symbol": contract.symbol,
                "secType": contract.secType,
                "rigth": contract.right,
                "multiplier": contract.multiplier,
                "currency": contract.currency,
                "localSymbol": contract.localSymbol,
                "tradingClass": contract.tradingClass,
                "lastTradeDateOrContractMonth": contract.lastTradeDateOrContractMonth,
                "strike": contract.strike,
                "position": float(position),
                "avgCost": float(avgCost),
            }
        )

    def positionEnd(self):
        self.positions_done = True
        print("Positions received")
