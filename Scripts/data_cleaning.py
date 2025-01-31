import pandas as pd
import logging
import re
import os
import emoji
import sys
import io

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Apply UTF-8 encoding for stdout only if sys.stdout has a buffer (avoids Jupyter issues)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_cleaning.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # Console output
    ]
)

def safe_log(msg):
    """ Remove emojis from log messages before logging. """
    logging.info(emoji.replace_emoji(msg, replace=""))

def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        safe_log(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        safe_log(f"❌ Error loading CSV file: {e}")
        raise
def merge_dataframes(*dfs):
    """ Merge multiple dataframes with the same columns into a single dataframe. """
    try:
        merged_df = pd.concat(dfs, ignore_index=True)
        safe_log(f"✅ {len(dfs)} dataframes merged successfully.")
        return merged_df
    except Exception as e:
        safe_log(f"❌ Error merging dataframes: {e}")
        raise

def clean_dataframe(df):
    """ Perform data cleaning. """
    try:
        df = df.drop_duplicates(subset=["ID"]).copy()
        safe_log("✅ Duplicates removed from dataset.")

        df.loc[:, 'Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.loc[:, 'Date'] = df['Date'].where(df['Date'].notna(), None)
        safe_log("✅ Date column formatted.")

        df.loc[:, 'ID'] = pd.to_numeric(df['ID'], errors="coerce").fillna(0).astype(int)
        df.loc[:, 'Message'] = df['Message'].fillna("No Message")
        df.loc[:, 'Media Path'] = df['Media Path'].fillna("No Media")
        safe_log("✅ Missing values filled.")

        df = df.rename(columns={
            "Channel Title": "channel_title",
            "Channel Username": "channel_username",
            "ID": "message_id",
            "Message": "message",
            "Date": "message_date",
            "Media Path": "media_path"
        })

        safe_log("✅ Data cleaning completed.")
        return df
    except Exception as e:
        safe_log(f"❌ Data cleaning error: {e}")
        raise

def save_cleaned_data(df, output_path):
    """ Save cleaned data to a CSV file. """
    try:
        df.to_csv(output_path, index=False, encoding="utf-8")
        safe_log(f"✅ Cleaned data saved to '{output_path}'.")
    except Exception as e:
        safe_log(f"❌ Error saving data: {e}")
        raise

# Function to extract all URLs (any type of link)
def extract_links(text):
    """ Extract all URLs starting with http/https """
    return re.findall(r'https?://[A-Za-z0-9./?&=_-]+', text)

# Function to extract emojis using a regex pattern
def extract_emojis(text):
    """ Extract all emojis using regex pattern """
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric shapes
        "\U0001F800-\U0001F8FF"  # Supplemental arrows
        "\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # Chess symbols
        "\U0001FA70-\U0001FAFF"  # Symbols
        "\U00002702-\U000027B0"  # Dingbats
        "]+", flags=re.UNICODE)
    return ''.join(re.findall(emoji_pattern, text))

# Function to clean the message (remove links and emojis)
def clean_message(text):
    """ Remove URLs and emojis from text """
    # Remove all links (http or https)
    text_no_links = re.sub(r'https?://[A-Za-z0-9./?&=_-]+', '', text)
    # Remove emojis
    text_no_emoji = re.sub(r'[\U0001F600-\U0001F64F'
                           r'\U0001F300-\U0001F5FF'
                           r'\U0001F680-\U0001F6FF'
                           r'\U0001F700-\U0001F77F'
                           r'\U0001F780-\U0001F7FF'
                           r'\U0001F800-\U0001F8FF'
                           r'\U0001F900-\U0001F9FF'
                           r'\U0001FA00-\U0001FA6F'
                           r'\U0001FA70-\U0001FAFF'
                           r'\U00002702-\U000027B0'
                           r']+', '', text_no_links)
    return text_no_emoji
