from app.base_handler import BaseHandler

class FeedbackHandler(BaseHandler):
    """A class used to represent a mini-agent to handle feedbacks.
    """
    def __init__(self, session_id):
        super().__init__(session_id)

    def handle(self, **kwargs):
        # Get the sentiment
        sentiment_score = kwargs["sentiment"]["queryTextSentiment"]["score"]
        return "Sorry to hear that!" if sentiment_score <= 0 else "That's great! Thank you for your feedback!"