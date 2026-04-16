from src.infraestructure.ibkr.ibkr_client import IbkrClient
from src.infraestructure.ibkr.ibkr_service import IbkrService
from src.interfaces.ui.tkinter_app import TkinterApp


cliente = IbkrClient()
service = IbkrService(cliente)
ui = TkinterApp(service)

ui.run()
