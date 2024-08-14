#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL and caches it.
    '''
    # Increment the access count for the URL
    redis_store.incr(f'count:{url}')
    
    # Check if the URL content is already cached
    cached_content = redis_store.get(f'cached:{url}')
    if cached_content:
        return cached_content.decode('utf-8')
    
    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text
    
    # Cache the HTML content with an expiration time of 10 seconds
    redis_store.setex(f'cached:{url}', 10, html_content)
    
    return html_content

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
