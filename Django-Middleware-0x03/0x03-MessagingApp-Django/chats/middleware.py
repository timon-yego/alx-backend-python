import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from django.core.cache import cache

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
    
class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of POST requests (messages) from each IP address
    within a time window to prevent spamming. Limits 5 messages per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # Maximum allowed messages per time window
        self.time_window = 60  # Time window in seconds (1 minute)

    def __call__(self, request):
        if request.method == "POST":
            user_ip = self.get_client_ip(request)
            cache_key = f"message_count_{user_ip}"
            message_data = cache.get(cache_key, {"count": 0, "start_time": time.time()})

            current_time = time.time()
            elapsed_time = current_time - message_data["start_time"]

            if elapsed_time > self.time_window:
                # Reset the counter if the time window has passed
                message_data = {"count": 1, "start_time": current_time}
            else:
                # Increment the counter within the time window
                if message_data["count"] >= self.limit:
                    return HttpResponseForbidden("Message limit exceeded. Please wait before sending more messages.")
                message_data["count"] += 1

            # Save the updated data back to the cache
            cache.set(cache_key, message_data, self.time_window)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve the client's IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip