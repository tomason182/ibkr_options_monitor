from src.infraestructure.ibkr.ibkr_client import IbkrClient
from src.infraestructure.ibkr.ibkr_service import IbkrService
from src.interfaces.ui.tkinter_app import TkinterApp
from src.infraestructure.repositories.sql_lite_repo import ExecutionsRepositorySQL
from src.infraestructure.repositories.sql_lite_repo import SQLiteConnect
from src.infraestructure.ibkr.execution_worker import ExecutionWorker

db = SQLiteConnect("trading.db")
db.get_conn()
db.create_tables()

repo = ExecutionsRepositorySQL(db)

client = IbkrClient()
service = IbkrService(client)
ui = TkinterApp(service)

worker = ExecutionWorker(client, repo)

worker.start()


ui.run()
