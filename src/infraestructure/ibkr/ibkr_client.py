from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.execution import Execution, ExecutionFilter
from ibapi.commission_and_fees_report import CommissionAndFeesReport
from queue import Queue
from threading import Event


class IbkrClient(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

        ## Estados
        # Conexion
        self.is_connected = False
        self.connected_event = Event()

        # Posiciones
        self.positions = []
        self.positions_event = Event()

        # Executions (cola de thread-safe)
        self.execution_queue = Queue()

        # Commissions
        self.commission_queue = Queue()

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
        self.is_connected = True
        self.connected_event.set()

    def connectionClosed(self):
        self.is_connected = False
        self.connected_event.clear()

    # ------------------------------------------
    # Positions
    # ------------------------------------------
    def position(self, account: str, contract: Contract, position, avgCost: float):
        self.positions.append(
            {
                "conId": contract.conId,
                "symbol": contract.symbol,
                "secType": contract.secType,
                "right": contract.right,
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
        self.positions_event.set()
        print("Positions received")

    # ----------------------------------------
    # Executions
    # ----------------------------------------
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print("execDetails trigger.")
        self.execution_queue.put(
            {
                "execId": execution.execId,
                "conId": contract.conId,
                "symbol": contract.symbol,
                "secType": contract.secType,
                "right": contract.right,
                "strike": contract.strike,
                "side": execution.side,
                "qty": execution.shares,
                "price": execution.price,
                "time": execution.time,
            }
        )

    def execDetailsEnd(self, reqId: int):
        print("ExecDetailsEnd. ReqId: ", reqId)

    def requestExecutions(self):
        filter = ExecutionFilter()
        filter.clientId = 0

        self.reqExecutions(1, filter)

    # ----------------------------------------
    # Commissions
    # ----------------------------------------
    def commissionReport(self, commissionAndFeesReport: CommissionAndFeesReport):
        print("Commission Received: ", commissionAndFeesReport.execId)

        self.commission_queue.put(
            {
                "execId": commissionAndFeesReport.execId,
                "commission": commissionAndFeesReport.commissionAndFees,
                "currency": commissionAndFeesReport.currency,
            }
        )
