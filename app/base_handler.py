from abc import abstractmethod
import os
class BaseHandler:
    """Base handler interface for all intent handler.
    """

    def __init__(self, *args, **kwargs):
        # Set the operation mode (i.e. DEV or PRODUCTION)
        self.runtime_mode = os.getenv("PYTHON_ENV", "DEV")

    @abstractmethod
    def handle(self, **kwargs) -> str: ...
