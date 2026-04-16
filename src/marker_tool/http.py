import time
import requests

from marker_tool.constants import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF,
    USER_AGENT,
)


def fetch(url: str):
    """
    Perform HTTP GET request with retry and exponential backoff.
    """
    headers = {"User-Agent": USER_AGENT}

    delay = RETRY_BACKOFF
    last_exception = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response

        except requests.RequestException as exc:
            last_exception = exc

            if attempt < MAX_RETRIES:
                time.sleep(delay)
                delay *= 2

    raise last_exception