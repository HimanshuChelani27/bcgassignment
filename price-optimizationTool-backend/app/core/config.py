import os
import logging
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# URL configuration
URL = os.getenv("URL")

# Define all required environment variables
REQUIRED_ENV_VARS = {
    "DATABASE_URL": DATABASE_URL,
    "SENDER_EMAIL": SENDER_EMAIL,
    "EMAIL_APP_PASSWORD": EMAIL_APP_PASSWORD,
    "URL": URL
    # Add any other required variables here
}

def validate_env_vars():
    """Check if all required environment variables are set"""
    missing_vars = []
    
    for var_name, var_value in REQUIRED_ENV_VARS.items():
        if var_value is None:
            missing_vars.append(var_name)
    
    return missing_vars

def check_env_vars():
    """Check environment variables and log warnings for missing ones"""
    missing_vars = validate_env_vars()
    
    if missing_vars:
        for var in missing_vars:
            logger.warning(f"Missing required environment variable: {var}")
        logger.warning("Some environment variables are not set. Application may not function correctly.")
        return False, missing_vars
    
    logger.info("All required environment variables are set")
    return True, []

