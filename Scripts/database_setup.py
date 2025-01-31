import os
import logging
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/database_setup.log"),
        logging.StreamHandler()
    ]
)

# Define SQLite database path
DB_PATH = "../data/telegram_messages.db"

def get_db_connection():
    """ Create and return SQLite database engine. """
    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Test connection
        logging.info("✅ Successfully connected to SQLite database.")
        return engine
    except Exception as e:
        logging.error(f"❌ Database connection failed: {e}")
        raise

# Create Table
def create_table(engine):
    """ Create telegram_messages table if it does not exist. """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS telegram_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_title TEXT,
        channel_username TEXT,
        message_id BIGINT UNIQUE,
        message TEXT,
        message_date TEXT,  -- SQLite stores timestamps as TEXT
        media_path TEXT
    );
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(create_table_query))
        logging.info("✅ Table 'telegram_messages' created successfully.")
    except Exception as e:
        logging.error(f"❌ Error creating table: {e}")
        raise

def insert_data(engine, cleaned_df):
    """ Inserts cleaned Telegram data into SQLite database. """
    try:
        # Ensure all required columns exist
        required_columns = ["channel_title", "channel_username", "message_id", "message", "message_date", "media_path"]
        for col in required_columns:
            if col not in cleaned_df.columns:
                cleaned_df[col] = None  # Add missing columns
                logging.warning(f"⚠️ Missing column '{col}' added with default None.")

        # Convert NaT timestamps to None (NULL in SQL)
        cleaned_df["message_date"] = cleaned_df["message_date"].apply(lambda x: None if pd.isna(x) else str(x))

        # ✅ Fixed SQL syntax issue
        insert_query = """
        INSERT OR IGNORE INTO telegram_messages 
        (channel_title, channel_username, message_id, message, message_date, media_path) 
        VALUES (:channel_title, :channel_username, :message_id, :message, :message_date, :media_path);
        """

        with engine.begin() as connection:
            for _, row in cleaned_df.iterrows():
                logging.info(f"Inserting: {row['message_id']} - {row['message_date']}")
                connection.execute(
                    text(insert_query),
                    {
                        "channel_title": row["channel_title"],
                        "channel_username": row["channel_username"],
                        "message_id": row["message_id"],
                        "message": row["message"],
                        "message_date": row["message_date"],
                        "media_path": row["media_path"]
                    }
                )

        logging.info(f"✅ {len(cleaned_df)} records inserted into SQLite database.")
    except Exception as e:
        logging.error(f"❌ Error inserting data: {e}")
        raise