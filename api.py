#!/usr/bin/env python3
"""
Readarr API Helper Functions
Handles all communication with the Readarr API
"""

import requests
import time
import datetime
from typing import List, Dict, Any, Optional, Union
from utils.logger import logger, debug_log
from config import API_KEY, API_URL, API_TIMEOUT, MONITORED_ONLY, SKIP_FUTURE_RELEASES

# Create a session for reuse
session = requests.Session()

def readarr_request(endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Union[Dict, List]]:
    """
    Make a request to the Readarr API (v1).
    `endpoint` should be something like 'book', 'command', etc.
    """
    url = f"{API_URL}/api/v1/{endpoint}"
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        if method.upper() == "GET":
            response = session.get(url, headers=headers, timeout=API_TIMEOUT)
        elif method.upper() == "POST":
            response = session.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return None
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return None

def get_books() -> List[Dict]:
    """Get all books from Readarr (full list)"""
    result = readarr_request("book")
    if result:
        debug_log("Raw books API response sample:", result[:2] if len(result) > 2 else result)
    return result or []

def get_cutoff_unmet() -> List[Dict]:
    """
    Directly query Readarr for only those books where the quality cutoff is not met.
    This is the most reliable way for big libraries. Optionally filter by monitored.
    """
    query = "wanted/cutoff?pageSize=1000"
    
    # Perform the request
    result = readarr_request(query, method="GET")
    
    # Extract the records from the paginated response
    if result and "records" in result:
        records = result.get("records", [])
        
        # If monitored only, filter the records
        if MONITORED_ONLY:
            records = [book for book in records if book.get("monitored", False)]
            
        return records
    
    return []

def get_missing_books() -> List[Dict]:
    """
    Get a list of books that are missing files.
    Filters based on MONITORED_ONLY setting and optionally
    excludes future releases.
    """
    query = "wanted/missing?pageSize=1000"
    
    # Perform the request
    result = readarr_request(query, method="GET")
    
    # Extract the records from the paginated response
    missing_books = []
    if result and "records" in result:
        records = result.get("records", [])
        
        # Get current date in ISO format (YYYY-MM-DD) for date comparison
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        for book in records:
            # Apply monitored filter if needed
            if MONITORED_ONLY and not book.get('monitored'):
                continue
                
            # Skip future releases if enabled
            if SKIP_FUTURE_RELEASES:
                # Check release date
                release_date = book.get('releaseDate')
                
                # Skip if release date exists and is in the future
                if release_date and release_date > current_date:
                    logger.debug(f"Skipping future release '{book.get('title')}' with date {release_date}")
                    continue
                    
            missing_books.append(book)
    
    return missing_books

def refresh_book(book_id: int) -> Optional[Dict]:
    """Refresh a book by ID"""
    data = {
        "name": "RefreshBook",
        "bookIds": [book_id]
    }
    return readarr_request("command", method="POST", data=data)

def book_search(book_id: int) -> Optional[Dict]:
    """Search for a book by ID"""
    data = {
        "name": "BookSearch",
        "bookIds": [book_id]
    }
    return readarr_request("command", method="POST", data=data)

def author_refresh(author_id: int) -> Optional[Dict]:
    """Refresh author metadata"""
    data = {
        "name": "RefreshAuthor",
        "authorIds": [author_id]
    }
    return readarr_request("command", method="POST", data=data)

def rescan_book(book_id: int) -> Optional[Dict]:
    """Rescan book files"""
    data = {
        "name": "RescanFolders",
        "bookIds": [book_id]
    }
    return readarr_request("command", method="POST", data=data)