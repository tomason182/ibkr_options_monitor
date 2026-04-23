import time
from datetime import datetime


class ContractDTO:
    def __init__(
        self,
        exec_id,
        con_id,
        symbol,
        exec_time,
        expiration_date,
        sec_type,
        right,
        strike,
        side,
        qty,
        price,
        account,
        exchange,
        trade_id=None,
        commission=None,
        delta=None,
        iv_rank_52=None,
    ):

        self.exec_id = exec_id
        self.con_id = con_id
        self.symbol = symbol
        self.exec_time = exec_time
        self.expiration_date = expiration_date
        self.sec_type = sec_type
        self.right = right
        self.strike = strike
        self.side = side
        self.qty = qty
        self.price = price
        self.account = account
        self.exchange = exchange
        self.commissions = commission
        self.delta = delta
        self.iv_rank_52 = iv_rank_52
        self.trade_id = trade_id

        # -------------------------------------------------------
        # Crear representacion del contrato
        # -------------------------------------------------------

        def create(self, contracts):
            state = self.contract_state(self.con_id, contracts)
            description = self.contract_description()

            if state:  # True == abierto
                days = {self.expiration_date - time.time() / 86400}
            else:  # False == cerrado
                days = None  # TODO logica futura calcula dias mantenidos.

            return {
                "trade_id": self.trade_id,
                "state": state,
                "description": description,
                "created_at": self.exec_time,
                "expiration_date": self.expiration_date,
                "days_to_expiration_or_held": days,
            }

        # -----------------------------------------------------------
        # Estado del contrato
        # -----------------------------------------------------------
        def contract_state(self, contracts):
            net_qty = sum(
                e["qty"] if e["side"] == "BOT" else -e["qty"]
                for e in contracts
                if e["con_id"] == self.con_id
            )

            return net_qty != 0  # True = abierto

        def contract_description(self):
            symbol = self.symbol.UPPER()
            exp_date = self.format_date(self.expiration_date)
            right = self.right
            strike = self.strike

            return {
                "symbol": symbol,
                "exp_date": exp_date,
                "right": right,
                "strike": strike,
            }

        # --------------------------------------------------------------
        # Formatter
        # --------------------------------------------------------------
        def format_date(self, timestamp):
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
