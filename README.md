# 10_Academy_AI_Mastery_kifiya_Week_7
10_Academy_AI_Mastery_kifiya_Week_7


README: Telegram Data Scraping, Cleaning, and Storage Pipeline

Project Overview

This project focuses on scraping, cleaning, and transforming data from selected public Telegram channels related to Ethiopian medical businesses. The pipeline extracts messages, images, and relevant information, processes and cleans the data, and stores it in a structured database for further analysis.

1. Notebooks README

Notebook Structure

telegram_scraping.ipynb - Handles data extraction from Telegram channels using the Telethon library.

data_cleaning.ipynb - Focuses on preprocessing and transforming raw data.

database_setup.ipynb - Prepares and manages the database to store the cleaned data.

Usage

Open each notebook in Jupyter Notebook or VS Code.

Follow the sequential execution of code cells.

Modify configurations (such as Telegram API credentials) as needed.

Calling Methods in Jupyter Notebook



2. Scripts README

File: telegram_scraping.py

Purpose: Extracts messages and images from specified Telegram channels.

Steps:

Connects to Telegram API via Telethon.

Extracts messages and media from selected channels.

Stores raw data in a local database or JSON/CSV format.

Implements logging to track errors and progress.

Usage:

python telegram_scraping.py

Ensure API credentials are correctly set up in the script.

File: data_cleaning.py

Purpose: Cleans and transforms the raw data.

Steps:

Removes duplicate messages.

Handles missing values.

Standardizes text and timestamps.

Stores cleaned data in a structured database.

Usage:

python data_cleaning.py

File: database_setup.py

Purpose: Sets up the database schema and tables for storing the cleaned Telegram data.

Steps:

Creates necessary tables for messages, images, and metadata.

Configures indexing for faster querying.

Loads initial cleaned data into the database.

Usage:

python database_setup.py

3. Dependencies & Installation

Install required Python packages:

pip install telethon pandas sqlalchemy sqlite3 dbt

Ensure DBT is set up properly:

pip install dbt

4. Logging & Monitoring

Each script includes logging to track the progress and capture errors.

Logs are stored in logs/ directory for debugging purposes.

5. Future Enhancements

Implement automated scheduling for periodic data scraping.

Enhance error handling for better fault tolerance.

Extend database schema to support additional data insights.

