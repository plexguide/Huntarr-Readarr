#!/usr/bin/env python3
"""
Missing Book Processing
Handles searching for missing books in Readarr
"""

import random
import time
from typing import List
from utils.logger import logger
from config import HUNT_MISSING_BOOKS, MONITORED_ONLY, RANDOM_SELECTION, REFRESH_AUTHOR
from api import get_missing_books, refresh_book, book_search, rescan_book, author_refresh
from state import load_processed_ids, save_processed_id, truncate_processed_list, PROCESSED_MISSING_FILE

def process_missing_books() -> bool:
    """
    Process books that are missing files.
    
    Returns:
        True if any processing was done, False otherwise
    """
    logger.info("=== Checking for Missing Books ===")

    # Skip if HUNT_MISSING_BOOKS is set to 0
    if HUNT_MISSING_BOOKS <= 0:
        logger.info("HUNT_MISSING_BOOKS is set to 0, skipping missing content")
        return False

    missing_books = get_missing_books()
    if not missing_books:
        logger.info("No missing books found.")
        return False
    
    logger.info(f"Found {len(missing_books)} book(s) with missing files.")
    processed_missing_ids = load_processed_ids(PROCESSED_MISSING_FILE)
    books_processed = 0
    processing_done = False
    
    # Randomize or use sequential indices
    indices = list(range(len(missing_books)))
    if RANDOM_SELECTION:
        random.shuffle(indices)
    
    for i in indices:
        if books_processed >= HUNT_MISSING_BOOKS:
            break
        
        book = missing_books[i]
        book_id = book.get('id')
        if not book_id or book_id in processed_missing_ids:
            continue
        
        # Get book details
        title = book.get('title', 'Unknown Title')
        author_name = "Unknown Author"
        author_id = None
        
        # Extract author info from book data structure
        if 'author' in book:
            author_name = book['author'].get('authorName', 'Unknown Author')
            author_id = book['author'].get('id')
        elif 'authorId' in book:
            author_id = book.get('authorId')
        
        logger.info(f"Processing missing book \"{title}\" by {author_name} (ID: {book_id}).")
        
        # Refresh author metadata if configured and we have author ID
        if REFRESH_AUTHOR and author_id:
            logger.info(f" - Refreshing author metadata for {author_name}...")
            refresh_res = author_refresh(author_id)
            if refresh_res and 'id' in refresh_res:
                logger.info(f"Author refresh command accepted (ID: {refresh_res.get('id')}). Waiting 5s...")
                time.sleep(5)
            else:
                logger.warning(f"WARNING: Author refresh command failed for {author_name}.")
        
        # Refresh book
        logger.info(" - Refreshing book metadata...")
        refresh_res = refresh_book(book_id)
        if not refresh_res or 'id' not in refresh_res:
            logger.warning(f"WARNING: Refresh command failed for {title}. Skipping.")
            time.sleep(10)
            continue
        
        logger.info(f"Refresh command accepted (ID: {refresh_res.get('id')}). Waiting 5s...")
        time.sleep(5)
        
        # Search
        logger.info(f" - Searching for \"{title}\"...")
        search_res = book_search(book_id)
        if search_res and 'id' in search_res:
            logger.info(f"Search command accepted (ID: {search_res.get('id')}).")
            processing_done = True
        else:
            logger.warning("WARNING: Book search failed.")
            continue
        
        # Rescan
        logger.info(" - Rescanning book folder...")
        rescan_res = rescan_book(book_id)
        if rescan_res and 'id' in rescan_res:
            logger.info(f"Rescan command accepted (ID: {rescan_res.get('id')}).")
        else:
            logger.warning("WARNING: Rescan command not available or failed.")
        
        # Mark processed
        save_processed_id(PROCESSED_MISSING_FILE, book_id)
        books_processed += 1
        logger.info(f"Processed {books_processed}/{HUNT_MISSING_BOOKS} missing books this cycle.")
    
    # Truncate processed list if needed
    truncate_processed_list(PROCESSED_MISSING_FILE)
    
    return processing_done