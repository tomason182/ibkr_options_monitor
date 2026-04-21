class Position:
    def __init__(self, con_id, symbol, sec_type, strike, position, avg_cost):
        self.id = con_id
        self.symbol = symbol
        self.sec_type = sec_type
        self.strike = strike
        self.position = position
        self.avg_cost = avg_cost


#   def __repr__(self):
#       return f"<Position {self.symbol} {self.quantity} @ {self.avg_cost}>"
