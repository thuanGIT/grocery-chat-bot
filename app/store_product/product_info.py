from math import prod
from app.base_handler import BaseHandler
from app.error import SQLException
from app.utilities.wolfram_alpha import NutritionQuery
class ProductInfoHandler(BaseHandler):
    """A class used to represent a mini-agent to handle product queries.
    """

    def __init__(self, session_id) -> None:
        super().__init__(session_id=session_id)

    def handle(self, **kwargs):
        # Get the intent name & parameters
        intent_name = str(kwargs["intent"])
        params = kwargs["params"]

        # Get the sub-intent
        sub_intent = intent_name[intent_name.index(".") + 1:]

        # Check if product param is available and the sub-intent is not exchange_refund
        if sub_intent == "exchange_refund":
            return "..."
        elif "product" not in params.keys():
            return "No information yet. Sorry..."

        # Get the product name
        product = params["product"]
        if sub_intent == "nutrition":
            # Get an API instance
            image = NutritionQuery.instance().get_nutritional_fact(product=product)
            return image if image else "No information yet. Sorry..."
        elif sub_intent == "price":
            price = self.get_price(product=product)
            return f"${price}" if price else "No price information..."
        elif sub_intent == "stock":
            stock = self.get_stock(product=product)
            if stock is None:
                return "No stock information..."
            else: 
                return f"Yes! Still in stock" if stock else "No. Unfortunately..."
        else:
            raise SQLException("Not sub-intent found!")

    
    def get_price(self, product):
        """Get the price of the product

        Args:
            product (str): Product name
        Returns:
            float: Price of the product
        """
        result = self.db.execute(f"SELECT ListPrice FROM Product WHERE ProductName = f{product}")
        if len(result) > 0:
            return list(result)[0][0]
        else:
            return None

    def get_stock(self, product):
        """Check if the product is still in stock.

        Args:
            product (str): Product name
        Returns:
            bool: Whether the product is still in stock
        """
        result = self.db.execute(f"SELECT InStock FROM Product WHERE ProductName = f{product}")
        if len(result) > 0:
            return list(result)[0][0]
        else:
            return None