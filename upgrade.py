#!/usr/bin/env python3
"""
Quality Upgrade Processing
Handles searching for books that need quality upgrades in Readarr
"""

import random
import time
from utils.logger import logger
from config import HUNT_UPGRADE_BOOKS, RANDOM_SELECTION, REFRESH_AUTHOR
from api import get_cutoff_unmet, refresh_book, book_search, rescan_book, author_refresh
from state import load_processed_ids, save_processed_id, truncate_processed_list, PROCESSED_UPGRADE_FILE

def process_cutoff_upgrades() -> bool:
    """
    Process books that need quality upgrades.
    
    Returns:
        True if any processing was done, False otherwise
    """
    logger.info("=== Checking for Quality Upgrades (Cutoff Unmet) ===")
    
    # Skip if HUNT_UPGRADE_BOOKS is set to 0
    if HUNT_UPGRADE_BOOKS <= 0:
        logger.info("HUNT_UPGRADE_BOOKS is set to 0, skipping quality upgrades")
        return False
    
    upgrade_books = get_cutoff_unmet()
    
    if not upgrade_books:
        logger.info("No books found that need quality upgrades.")
        return False
    
    logger.info(f"Found {len(upgrade_books)} books that need quality upgrades.")
    processed_upgrade_ids = load_processed_ids(PROCESSED_UPGRADE_FILE)
    books_processed = 0
    processing_done = False
    
    # Randomize or use sequential indices
    indices = list(range(len(upgrade_books)))
    if RANDOM_SELECTION:
        random.shuffle(indices)
    
    for i in indices:
        if books_processed >= HUNT_UPGRADE_BOOKS:
            break
        
        book = upgrade_books[i]
        book_id = book.get('id')
        if not book_id or book_id in processed_upgrade_ids:
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
        
        logger.info(f"Processing quality upgrade for \"{title}\" by {author_name} (ID: {book_id}).")
        
        # Refresh author metadata if configured and we have author ID
        if REFRESH_AUTHOR and author_id:
            logger.info(f" - Refreshing author metadata for {author_name}...")
            refresh_res = author_refresh(author_id)
            if refresh_res and 'id' in refresh_res:
                logger.info(f"Author refresh command accepted (ID: {refresh_res.get('id')}). Waiting 5s...")
                time.sleep(5)
            else:
                logger.warning(f"WARNING: Author refresh command failed for {author_name}.")
        
        # Refresh book information
        logger.info(f" - Refreshing book information...")
        refresh_res = refresh_book(book_id)
        if not refresh_res or 'id' not in refresh_res:
            logger.warning(f"WARNING: Refresh command failed for {title}. Skipping this book.")
            time.sleep(10)
            continue
        
        logger.info(f"Refresh command accepted (ID: {refresh_res.get('id')}). Waiting 5s...")
        time.sleep(5)
        
        # Search
        logger.info(f" - Searching for quality upgrade...")
        search_res = book_search(book_id)
        if search_res and 'id' in search_res:
            logger.info(f"Search command accepted (ID: {search_res.get('id')}).")
            processing_done = True
            
            # Rescan
            logger.info(" - Rescanning book folder...")
            rescan_res = rescan_book(book_id)
            if rescan_res and 'id' in rescan_res:
                logger.info(f"Rescan command accepted (ID: {rescan_res.get('id')}).")
            else:
                logger.warning("WARNING: Rescan command not available or failed.")
            
            # Mark processed
            save_processed_id(PROCESSED_UPGRADE_FILE, book_id)
            books_processed += 1
            logger.info(f"Processed {books_processed}/{HUNT_UPGRADE_BOOKS} upgrade books this cycle.")
        else:
            logger.warning(f"WARNING: Search command failed for book ID {book_id}.")
            time.sleep(10)
    
    logger.info(f"Completed processing {books_processed} upgrade books for this cycle.")
    truncate_processed_list(PROCESSED_UPGRADE_FILE)
    
    return processing_done