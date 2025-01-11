import logging
from datetime import datetime
from django.http import HttpResponseForbidden

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
    

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app based on server time.
    Denies access outside 9 AM to 6 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access between 9 AM (9) and 6 PM (18)
        if 9 <= current_hour < 18:
            return self.get_response(request)

        # Deny access outside allowed hours
        return HttpResponseForbidden("Access to the chat is restricted outside 9 AM to 6 PM.")