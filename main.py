#!/usr/bin/env python3
"""
Huntarr [Readarr Edition] - Python Version
Main entry point for the application
"""

import time
import sys
from utils.logger import logger
from config import HUNT_MODE, SLEEP_DURATION, log_configuration
from missing import process_missing_books
from upgrade import process_cutoff_upgrades
from state import check_state_reset, calculate_reset_time

def main_loop() -> None:
    """Main processing loop for Huntarr-Readarr"""
    while True:
        # Check if state files need to be reset
        check_state_reset()
        
        logger.info(f"=== Starting Huntarr-Readarr cycle ===")
        
        # Track if any processing was done in this cycle
        processing_done = False
        
        # Process books based on HUNT_MODE
        if HUNT_MODE in ["missing", "both"]:
            if process_missing_books():
                processing_done = True
                
        if HUNT_MODE in ["upgrade", "both"]:
            if process_cutoff_upgrades():
                processing_done = True
        
        # Calculate time until the next reset
        calculate_reset_time()
        
        # Sleep at the end of the cycle only
        logger.info(f"Cycle complete. Sleeping {SLEEP_DURATION}s before next cycle...")
        logger.info("⭐ Tool Great? Donate @ https://donate.plex.one for Daughter's College Fund!")
        time.sleep(SLEEP_DURATION)

if __name__ == "__main__":
    # Log configuration settings
    log_configuration(logger)

    try:
        main_loop()
    except KeyboardInterrupt:
        logger.info("Huntarr-Readarr stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)