from src.application.models.ContractDTO import ContractsDTO


class TradesService:
    def __init__(self, worker) -> None:
        self.worker = worker

        def create_trade(self):
            existing_contracts = self.worker.get()

            contracts = ContractsDTO.create(existing_contracts)
