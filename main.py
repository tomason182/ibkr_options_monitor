from src.infraestructure.ibkr.ibkr_client import IbkrClient
from src.infraestructure.ibkr.ibkr_service import IbkrService
from src.interfaces.ui.tkinter_app import TkinterApp
from src.infraestructure.repositories.postgresql_repo import PostgreSQLRepository
from src.infraestructure.ibkr.execution_worker import ExecutionWorker

client = IbkrClient()
service = IbkrService(client)
ui = TkinterApp(service)

worker = ExecutionWorker(client, PostgreSQLRepository)

worker.start()

ui.run()
