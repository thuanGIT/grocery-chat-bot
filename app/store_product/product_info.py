from app.base_handler import BaseHandler


class ProductInfoHandler(BaseHandler):
    """A class used to represent a mini-agent to handle product queries.
    """

    def __init__(self) -> None:
        super().__init__()

    def handle(self, **kwargs) -> str:
        ...