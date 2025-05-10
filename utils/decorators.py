#Local
from config.logger_config import logger
# Standard Library
from functools import wraps
from datetime import datetime
import os
import json
# Third Party

TRACKER_FILE = "logs/api_tracker.json"
RateLimit = 1000

def track_api_call(api_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Load usage log
            today = datetime.today().date()
            date_str = today.strftime("%Y-%m-%d")
            
            if os.path.exists(TRACKER_FILE):
                with open(TRACKER_FILE, "r") as f:
                    usage = json.load(f)
                    if usage["Date"] != date_str:
                        usage = {"total_calls": 0, "calls": [], "Date": date_str}
            else:
                usage = {"total_calls": 0, "calls": [], "Date": date_str}
            
            if usage["total_calls"] >= RateLimit:
                logger.warning(f"[{api_name.upper()}] Rate limit reached. No more calls allowed.")
                return None, None
            
            logger.info(f"[{api_name.upper()}] Calling {func.__name__}")
            output = func(*args, *kwargs)
            logger.debug(f"[{api_name.upper()}] {func.__name__} returned: {output}")
            
            # Update tracking
            usage["total_calls"] += 1
            usage["calls"].append({
                "timestamp": datetime.now().isoformat(),
                "API Name": api_name,
            })

            # Save usage log
            with open(TRACKER_FILE, "w") as f:
                json.dump(usage, f, indent=2)

            return output
        return wrapper
    return decorator


def conversionLogger():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Converting {args[0]} using {func.__name__}")
            conversion = func(*args, **kwargs)
            logger.debug(f"Converted value: {conversion}")
            return conversion
        return wrapper
    return decorator