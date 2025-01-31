README for Jupyter Notebooks

Overview

This repository contains Jupyter notebooks that handle data scraping, cleaning, transformation, and storage for Telegram channels related to Ethiopian medical businesses. The notebooks facilitate exploratory data analysis and interactive debugging for the data pipeline.

Notebooks Structure

1. Telegram Scraping Notebook

Uses the telethon package to scrape data from selected public Telegram channels.

Extracts text messages, images, and metadata from posts.

Stores raw data in temporary storage for further processing.

2. Data Cleaning Notebook

Removes duplicate records.

Handles missing values by filling or removing null data.

Standardizes formats for consistency.

Validates data for completeness and correctness.

Outputs a cleaned dataset ready for database storage.

3. Database Setup Notebook

Creates and configures an SQLite database for storing the processed data.

Defines table structures and schemas.

Loads cleaned data into the database for further analysis.

Installation

To run the notebooks, install the required dependencies using:

pip install telethon pandas dbt sqlite3

Usage

Open the notebooks in Jupyter.

Run the cells sequentially to execute the entire data pipeline.