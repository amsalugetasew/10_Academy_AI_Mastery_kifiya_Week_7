README for Script Files

Overview

This repository includes three Python scripts that automate data scraping, cleaning, and database setup for Telegram channels related to Ethiopian medical businesses.

Scripts Structure

1. telegram_scraping.py

Scrapes messages and images from specified Telegram channels.

Uses the telethon package to interact with the Telegram API.

Stores raw data in JSON or CSV format for further processing.

2. data_cleaning.py

Reads the raw data and performs cleaning operations:

Removing duplicates.

Handling missing values.

Standardizing data formats.

Validating data integrity.

Outputs a cleaned version of the dataset.

3. database_setup.py

Creates an SQLite database and defines table schemas.

Loads the cleaned data into the database.

Ensures data integrity and facilitates efficient querying.

Installation

Install the required dependencies with:

pip install telethon pandas dbt sqlite3

Usage

Run the scripts in the following order:

Scrape Telegram Data

python telegram_scraping.py

Clean the Scraped Data

python data_cleaning.py

Set Up Database and Store Data

python database_setup.py

Logging and Monitoring

Each script includes logging functionality to track execution progress and errors.

Logs are stored in a logs/ directory for troubleshooting purposes.

Notes

Ensure you have valid Telegram API credentials before running the scraper.

The scripts assume an SQLite database but can be modified for other databases (e.g., PostgreSQL, MySQL).

Modify the channel list in telegram_scraping.py as needed to expand data collection.