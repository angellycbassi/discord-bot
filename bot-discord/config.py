"""
Configuration module for the Discord RPG Bot.
Contains all sensitive variables and settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')  # Bot token from Discord Developer Portal
COMMAND_PREFIX = '!'  # Prefix for text commands

# Data storage configuration
DATA_DIR = 'data'
CHARACTER_FILE = os.path.join(DATA_DIR, 'characters.json')
INVENTORY_FILE = os.path.join(DATA_DIR, 'inventories.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
