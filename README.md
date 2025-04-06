# Huntarr [Readarr Edition] - Force Readarr to Hunt Missing Books & Upgrade Book Qualities

<h2 align="center">Want to Help? Click the Star in the Upper-Right Corner! ⭐</h2>

<table>
  <tr>
    <td colspan="2"><img src="https://github.com/user-attachments/assets/3ea6d2a0-19fd-4e7c-9dfd-797e735b2955" width="100%"/></td>
  </tr>
</table>

**NOTE**: This utilizes Readarr API Version - `1`.

## Table of Contents
- [Overview](#overview)
- [Related Projects](#related-projects)
- [Features](#features)
- [How It Works](#how-it-works)
- [Configuration Options](#configuration-options)
- [Installation Methods](#installation-methods)
  - [Docker Run](#docker-run)
  - [Docker Compose](#docker-compose)
  - [Unraid Users](#unraid-users)
  - [SystemD Service](#systemd-service)
- [Use Cases](#use-cases)
- [Tips](#tips)
- [Troubleshooting](#troubleshooting)

## Overview

This script continually searches your Readarr library for books with missing files and books that need quality upgrades. It automatically triggers searches for both missing books and books below your quality cutoff. It's designed to run continuously while being gentle on your indexers, helping you gradually complete your book collection with the best available quality.

## Related Projects

* [Huntarr - Sonarr Edition](https://github.com/plexguide/Huntarr-Sonarr) - Sister version for TV shows
* [Huntarr - Radarr Edition](https://github.com/plexguide/Huntarr-Radarr) - Sister version for movies
* [Huntarr - Lidarr Edition](https://github.com/plexguide/Huntarr-Lidarr) - Sister version for music
* [Unraid Intel ARC Deployment](https://github.com/plexguide/Unraid_Intel-ARC_Deployment) - Convert videos to AV1 Format (I've saved 325TB encoding to AV1)
* Visit [PlexGuide](https://plexguide.com) for more great scripts

## PayPal Donations – Building My Daughter's Future

My 12-year-old daughter is passionate about singing, dancing, and exploring STEM. She consistently earns A-B honors and dreams of a bright future. Every donation goes directly into her college fund, helping turn those dreams into reality. Thank you for your generous support!

[![Donate with PayPal button](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=58AYJ68VVMGSC)

## Features

- 🔄 **Continuous Operation**: Runs indefinitely until manually stopped
- 🎯 **Dual Targeting System**: Targets both missing books and quality upgrades
- 🎲 **Random Selection**: By default, selects books randomly to distribute searches across your library
- ⏱️ **Throttled Searches**: Includes configurable delays to prevent overloading indexers
- 📊 **Status Reporting**: Provides clear feedback about what it's doing and which books it's searching for
- 🛡️ **Error Handling**: Gracefully handles connection issues and API failures
- 🔁 **State Tracking**: Remembers which books have been processed to avoid duplicate searches
- ⚙️ **Configurable Reset Timer**: Automatically resets search history after a configurable period
- 📦 **Modular Design**: Modern codebase with separated concerns for easier maintenance
- ⏲️ **Configurable Timeouts**: Adjustable API timeout for large libraries
- 🗓️ **Future Release Filtering**: Option to skip books with future release dates
- 👩‍💼 **Author Metadata Refresh**: Option to refresh author metadata before processing books

## How It Works

1. **Initialization**: Connects to your Readarr instance and analyzes your library
2. **Missing Books**: 
   - Identifies books without files
   - Optionally filters out future releases
   - Randomly selects books to process (up to configurable limit)
   - Refreshes metadata and triggers searches
3. **Quality Upgrades**:
   - Finds books that don't meet your quality cutoff settings
   - Processes them in configurable batches
   - Uses smart selection to distribute searches
4. **State Management**:
   - Tracks which books have been processed
   - Automatically resets this tracking after a configurable time period
5. **Repeat Cycle**: Waits for a configurable period before starting the next cycle

## Configuration Options

The following environment variables can be configured:

| Variable                     | Description                                                              | Default    |
|------------------------------|-----------------------------------------------------------------------|---------------|
| `API_KEY`                    | Your Readarr API key                                                     | Required   |
| `API_URL`                    | URL to your Readarr instance                                             | Required   |
| `API_TIMEOUT`                | Timeout in seconds for API requests to Readarr                           | 60         |
| `MONITORED_ONLY`             | Only process monitored books                                             | true       |
| `SKIP_FUTURE_RELEASES`       | Skip processing books with release dates in the future                   | true       |
| `HUNT_MISSING_BOOKS`         | Maximum missing books to process per cycle                               | 1          |
| `HUNT_UPGRADE_BOOKS`         | Maximum upgrade books to process per cycle                               | 5          |
| `SLEEP_DURATION`             | Seconds to wait after completing a cycle (900 = 15 minutes)              | 900        |
| `RANDOM_SELECTION`           | Use random selection (`true`) or sequential (`false`)                    | true       |
| `STATE_RESET_INTERVAL_HOURS` | Hours which the processed state files reset (168=1 week, 0=never reset)  | 168        |
| `REFRESH_AUTHOR`             | Refresh author metadata before processing book (`true` or `false`)       | true       |
| `DEBUG_MODE`                 | Enable detailed debug logging (`true` or `false`)                        | false      |

### Detailed Configuration Explanation

- **API_TIMEOUT**
  - Sets the maximum number of seconds to wait for Readarr API responses before timing out.
  - This is particularly important when working with large libraries.
  - If you experience timeout errors, increase this value.
  - For libraries with thousands of books, values of 90-120 seconds may be necessary.
  - Default is 60 seconds, which works well for most medium-sized libraries.

- **SKIP_FUTURE_RELEASES**
  - When set to `true`, books with release dates in the future will be skipped during missing book processing.
  - This prevents searching for content that isn't yet available.
  - Set to `false` if you want to process all missing books regardless of release date.

- **HUNT_MISSING_BOOKS**  
  - Sets the maximum number of missing books to process in each cycle.  
  - Once this limit is reached, the script stops processing further missing books until the next cycle.
  - Set to `0` to disable missing book processing completely.

- **HUNT_UPGRADE_BOOKS**  
  - Sets the maximum number of upgrade books to process in each cycle.  
  - When this limit is reached, the upgrade portion of the cycle stops.
  - Set to `0` to disable quality upgrade processing completely.

- **RANDOM_SELECTION**
  - When `true`, selects books randomly, which helps distribute searches across your library.
  - When `false`, processes books sequentially, which can be more predictable and methodical.

- **STATE_RESET_INTERVAL_HOURS**  
  - Controls how often the script "forgets" which books it has already processed.  
  - The script records the IDs of missing books and upgrade books that have been processed.  
  - When the age of these records exceeds the number of hours set by this variable, the records are cleared automatically.  
  - This reset allows the script to re-check books that were previously processed, so if there are changes (such as improved quality), they can be processed again.
  - Setting this to `0` will disable the reset functionality entirely - processed items will be remembered indefinitely.
  - Default is 168 hours (one week) - meaning the script will start fresh weekly.

- **REFRESH_AUTHOR**
  - When set to `true`, the script will refresh author metadata before processing a book.
  - This can help ensure that all book information is up-to-date before searching.
  - Particularly useful if you've recently added new authors or if you suspect metadata may be out of date.
  - Set to `false` to skip this step and potentially speed up processing.

- **DEBUG_MODE**
  - When set to `true`, the script will output detailed debugging information about API responses and internal operations.
  - Useful for troubleshooting issues but can make logs verbose.

---

## Installation Methods

### Docker Run

The simplest way to run Huntarr is via Docker:

```bash
docker run -d --name huntarr-readarr \
  --restart always \
  -e API_KEY="your-api-key" \
  -e API_URL="http://your-readarr-address:8787" \
  -e API_TIMEOUT="60" \
  -e MONITORED_ONLY="true" \
  -e SKIP_FUTURE_RELEASES="true" \
  -e HUNT_MISSING_BOOKS="1" \
  -e HUNT_UPGRADE_BOOKS="5" \
  -e SLEEP_DURATION="900" \
  -e RANDOM_SELECTION="true" \
  -e REFRESH_AUTHOR="true" \
  -e STATE_RESET_INTERVAL_HOURS="168" \
  -e DEBUG_MODE="false" \
  huntarr/huntarr-readarr:1.0
```

To check on the status of the program, you should see new files downloading or you can type:
```bash
docker logs huntarr-readarr
```

### Docker Compose

For those who prefer Docker Compose, add this to your `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  huntarr-readarr:
    image: huntarr/huntarr-readarr:1.0
    container_name: huntarr-readarr
    restart: always
    environment:
      API_KEY: "your-api-key"
      API_URL: "http://your-readarr-address:8787"
      API_TIMEOUT: "60"
      MONITORED_ONLY: "true"
      SKIP_FUTURE_RELEASES: "true"
      HUNT_MISSING_BOOKS: "1"
      HUNT_UPGRADE_BOOKS: "5"
      SLEEP_DURATION: "900"
      RANDOM_SELECTION: "true"
      REFRESH_AUTHOR: "true"
      STATE_RESET_INTERVAL_HOURS: "168"
      DEBUG_MODE: "false"
```

Then run:

```bash
docker-compose up -d huntarr-readarr
```

To check on the status of the program, you should see new files downloading or you can type:
```bash
docker logs huntarr-readarr
```

### Unraid Users

Run from the Unraid Command Line. This will eventually be submitted to the Unraid App Store:

```bash
docker run -d --name huntarr-readarr \
  --restart always \
  -e API_KEY="your-api-key" \
  -e API_URL="http://your-readarr-address:8787" \
  -e API_TIMEOUT="60" \
  -e MONITORED_ONLY="true" \
  -e SKIP_FUTURE_RELEASES="true" \
  -e HUNT_MISSING_BOOKS="1" \
  -e HUNT_UPGRADE_BOOKS="5" \
  -e SLEEP_DURATION="900" \
  -e RANDOM_SELECTION="true" \
  -e REFRESH_AUTHOR="true" \
  -e STATE_RESET_INTERVAL_HOURS="168" \
  -e DEBUG_MODE="false" \
  huntarr/huntarr-readarr:1.0
```

### SystemD Service

For a more permanent installation on Linux systems using SystemD:

1. Save the script to `/usr/local/bin/huntarr-readarr.sh`
2. Make it executable: `chmod +x /usr/local/bin/huntarr-readarr.sh`
3. Create a systemd service file at `/etc/systemd/system/huntarr-readarr.service`:

```ini
[Unit]
Description=Huntarr Readarr Service
After=network.target readarr.service

[Service]
Type=simple
User=your-username
Environment="API_KEY=your-api-key"
Environment="API_URL=http://localhost:8787"
Environment="API_TIMEOUT=60"
Environment="MONITORED_ONLY=true"
Environment="SKIP_FUTURE_RELEASES=true"
Environment="HUNT_MISSING_BOOKS=1"
Environment="HUNT_UPGRADE_BOOKS=5"
Environment="SLEEP_DURATION=900"
Environment="RANDOM_SELECTION=true"
Environment="REFRESH_AUTHOR=true"
Environment="STATE_RESET_INTERVAL_HOURS=168"
Environment="DEBUG_MODE=false"
ExecStart=/usr/local/bin/huntarr-readarr.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

4. Enable and start the service:

```bash
sudo systemctl enable huntarr-readarr
sudo systemctl start huntarr-readarr
```

## Use Cases

- **Library Completion**: Gradually fill in missing books in your collection
- **Quality Improvement**: Automatically upgrade book quality as better versions become available
- **New Book Setup**: Automatically find newly added books
- **Background Service**: Run it in the background to continuously maintain your library
- **Smart Rotation**: With state tracking, ensures all content gets attention over time
- **Large Library Management**: With optimized performance and configurable timeouts, handles even the largest libraries
- **Release Date Awareness**: Skip books that aren't released yet, focusing only on currently available content
- **Author Management**: Refreshes author metadata to ensure all book data is up-to-date

## Tips

- **First-Time Use**: Start with default settings to ensure it works with your setup
- **Adjusting Speed**: Lower the `SLEEP_DURATION` to search more frequently (be careful with indexer limits)
- **Batch Size Control**: Adjust `HUNT_MISSING_BOOKS` and `HUNT_UPGRADE_BOOKS` based on your indexer's rate limits
- **Monitored Status**: Set `MONITORED_ONLY=false` if you want to download all missing books regardless of monitored status
- **System Resources**: The script uses minimal resources and can run continuously on even low-powered systems
- **Debugging Issues**: Enable `DEBUG_MODE=true` temporarily to see detailed logs when troubleshooting
- **API Timeouts**: If you have a large library, increase the `API_TIMEOUT` value to 90-120 seconds to prevent timeout errors
- **Future Releases**: Use `SKIP_FUTURE_RELEASES=true` to avoid searching for books not yet released
- **Author Metadata**: If you notice that book information is incomplete, set `REFRESH_AUTHOR=true` to refresh author metadata

## Troubleshooting

- **API Key Issues**: Check that your API key is correct in Readarr settings
- **Connection Problems**: Ensure the Readarr URL is accessible from where you're running the script
- **Command Failures**: If search commands fail, try using the Readarr UI to verify what commands are available in your version
- **Logs**: Check the container logs with `docker logs huntarr-readarr` if running in Docker
- **Debug Mode**: Enable `DEBUG_MODE=true` to see detailed API responses and process flow
- **State Files**: The script stores state in `/tmp/huntarr-state/` - if something seems stuck, you can try deleting these files
- **Timeout Errors**: If you see "Read timed out" errors, increase the `API_TIMEOUT` value to give Readarr more time to respond

---

**Change Log:**
- **v1**: Initial release of Huntarr [Readarr Edition] based on the Radarr version

---

This script helps automate the tedious process of finding missing books and quality upgrades in your collection, running quietly in the background while respecting your indexers' rate limits.

---

Thanks to: 

[IntensiveCareCub](https://www.reddit.com/user/IntensiveCareCub/) for the Hunter to Huntarr idea!