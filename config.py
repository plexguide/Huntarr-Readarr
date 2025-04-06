#!/usr/bin/env python3
"""
Configuration module for Huntarr-Readarr
Handles all environment variables and configuration settings
"""

import os
import logging

# API Configuration
API_KEY = os.environ.get("API_KEY", "your-api-key")
API_URL = os.environ.get("API_URL", "http://your-readarr-address:8787")

# API timeout in seconds
try:
    API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "60"))
except ValueError:
    API_TIMEOUT = 60
    print(f"Warning: Invalid API_TIMEOUT value, using default: {API_TIMEOUT}")

# Missing Content Settings
try:
    HUNT_MISSING_BOOKS = int(os.environ.get("HUNT_MISSING_BOOKS", "1"))
except ValueError:
    HUNT_MISSING_BOOKS = 1
    print(f"Warning: Invalid HUNT_MISSING_BOOKS value, using default: {HUNT_MISSING_BOOKS}")

# Upgrade Settings
try:
    HUNT_UPGRADE_BOOKS = int(os.environ.get("HUNT_UPGRADE_BOOKS", "5"))
except ValueError:
    HUNT_UPGRADE_BOOKS = 5
    print(f"Warning: Invalid HUNT_UPGRADE_BOOKS value, using default: {HUNT_UPGRADE_BOOKS}")

# Sleep duration in seconds after completing one full cycle (default 15 minutes)
try:
    SLEEP_DURATION = int(os.environ.get("SLEEP_DURATION", "900"))
except ValueError:
    SLEEP_DURATION = 900
    print(f"Warning: Invalid SLEEP_DURATION value, using default: {SLEEP_DURATION}")

# Reset processed state file after this many hours (default 168 hours = 1 week)
try:
    STATE_RESET_INTERVAL_HOURS = int(os.environ.get("STATE_RESET_INTERVAL_HOURS", "168"))
except ValueError:
    STATE_RESET_INTERVAL_HOURS = 168
    print(f"Warning: Invalid STATE_RESET_INTERVAL_HOURS value, using default: {STATE_RESET_INTERVAL_HOURS}")

# Selection Settings
RANDOM_SELECTION = os.environ.get("RANDOM_SELECTION", "true").lower() == "true"
MONITORED_ONLY = os.environ.get("MONITORED_ONLY", "true").lower() == "true"
SKIP_FUTURE_RELEASES = os.environ.get("SKIP_FUTURE_RELEASES", "true").lower() == "true"

# Hunt mode: "missing", "upgrade", or "both"
HUNT_MODE = os.environ.get("HUNT_MODE", "both")

# Author mode: If true, refresh the author metadata before refreshing the book
REFRESH_AUTHOR = os.environ.get("REFRESH_AUTHOR", "true").lower() == "true"

# Debug Settings
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"

def log_configuration(logger):
    """Log the current configuration settings"""
    logger.info("=== Huntarr [Readarr Edition] Starting ===")
    logger.info(f"API URL: {API_URL}")
    logger.info(f"API Timeout: {API_TIMEOUT}s")
    logger.info(f"Missing Content Configuration: HUNT_MISSING_BOOKS={HUNT_MISSING_BOOKS}")
    logger.info(f"Upgrade Configuration: HUNT_UPGRADE_BOOKS={HUNT_UPGRADE_BOOKS}")
    logger.info(f"State Reset Interval: {STATE_RESET_INTERVAL_HOURS} hours")
    logger.info(f"MONITORED_ONLY={MONITORED_ONLY}, RANDOM_SELECTION={RANDOM_SELECTION}")
    logger.info(f"SKIP_FUTURE_RELEASES={SKIP_FUTURE_RELEASES}, REFRESH_AUTHOR={REFRESH_AUTHOR}")
    logger.info(f"HUNT_MODE={HUNT_MODE}, SLEEP_DURATION={SLEEP_DURATION}s")
    logger.debug(f"API_KEY={API_KEY}")