import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        logging.basicConfig(
            filename='requests.log',  # Log file name
            level=logging.INFO,       # Logging level
            format='%(message)s'      # Log format
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # Get user info (AnonymousUser if not authenticated)
        user = request.user if request.user.is_authenticated else "Anonymous"
        # Log the information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        # Proceed to the next middleware or view
        response = self.get_response(request)
        return response
