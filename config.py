"""
Configuration file for Accident Hospital Service
Store all API keys and settings here
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS - Store these in environment variables or .env file
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY_HERE')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', True)
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5000))

# Accident Detection Thresholds
ACCELERATION_THRESHOLD = 50  # m/s² - typical car crash is 50-100 m/s²
GYRO_THRESHOLD = 300  # degrees/s
CONFIDENCE_THRESHOLD = 0.7  # For AI detection

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///accident_service.db')

# Camera Settings
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_VIDEO_FORMATS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
CAMERA_TIMEOUT = 30  # seconds

# Hospital Search Radius
SEARCH_RADIUS_KM = 5  # Search for hospitals within 5 km radius
