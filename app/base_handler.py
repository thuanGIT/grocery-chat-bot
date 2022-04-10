from abc import abstractmethod
import os
from app.database import Database
class BaseHandler:
    """Base handler interface for all intent handler.
    """

    def __init__(self, session_id):
        # Set the operation mode (i.e. DEV or PRODUCTION)
        self.runtime_mode = os.getenv("PYTHON_ENV", "DEV")
        self.db = Database.instance(session_id=session_id)
        self.db.connect()

    @abstractmethod
    def handle(self, **kwargs) -> str: ...
