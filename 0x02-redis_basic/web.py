#!/usr/bin/env python3
"""
Web module.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redisStore = redis.Redis()


def data_caching(method: Callable) -> Callable:
    """Decorator that cache fetched data from url"""
    @wraps(method)
    def wrapper(url):
        """Function that cache the data"""
        redisStore.incr(f"count:{url}")
        cached_page = redisStore.get(f"page:{url}")
        if cached_page:
            return cached_page.decode('utf-8')

        result = method(url)
        redisStore.setex(f"page:{url}", 10, result)
        return result

    return wrapper


@data_caching
def get_page(url: str) -> str:
    """Function that get and return the html content of url"""
    html_content = requests.get(url).text
    return html_content
