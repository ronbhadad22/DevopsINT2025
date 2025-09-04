"""
Hello module for the nexus example package.
"""

import requests
from . import __version__


def greet(name: str) -> str:
    """
    Generate a greeting message.
    
    Args:
        name (str): The name to greet
        
    Returns:
        str: A greeting message
    """
    message = f"Hello, {name}! Welcome to the Nexus Example Package."
    print(message)
    return message


def get_version() -> str:
    """
    Get the package version.
    
    Returns:
        str: The current package version
    """
    return __version__


def make_request(url: str) -> dict:
    """
    Make a simple HTTP GET request (demonstrates dependency usage).
    
    Args:
        url (str): The URL to request
        
    Returns:
        dict: Response data or error information
    """
    try:
        response = requests.get(url, timeout=10)
        return {
            "status_code": response.status_code,
            "success": response.ok,
            "url": url
        }
    except requests.RequestException as e:
        return {
            "error": str(e),
            "success": False,
            "url": url
        }
