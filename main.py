"""
This module provides functionality to track shipments using an external API.
It includes functions to initiate tracking and check the tracking status.
"""

import os
import time
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from a .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
TRACKING_URL = "https://parcelsapp.com/api/v3/shipments/tracking"
SHIPMENTS = [
    {
        "trackingId": "420184339200190333885205049528",
        "language": "en",
        "country": "United States",
    },
]


def initiate_tracking(api_key, shipments):
    """Initiates the tracking request and returns the UUID."""
    try:
        logging.info("Initiating tracking request...")
        response = requests.post(
            TRACKING_URL, json={"apiKey": api_key, "shipments": shipments}, timeout=10
        )
        response.raise_for_status()

        data = response.json()
        uuid = data.get("uuid")
        status = data.get("shipments")[0].get("lastState")
        logging.info("Tracking initiated successfully. UUID: %s \n%s", uuid, status)
        return uuid
    except requests.RequestException as e:
        logging.error("Error initiating tracking: %s", e)
        return None


def check_tracking_status(api_key, uuid, interval=10):
    """Checks the tracking status using the UUID."""
    logging.info("Checking tracking status...")
    while True:
        try:
            response = requests.get(
                TRACKING_URL, params={"apiKey": api_key, "uuid": uuid}, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data.get("done"):
                logging.info("Tracking complete.")
                break
            else:
                logging.info("Tracking in progress...")
                time.sleep(interval)
        except requests.RequestException as e:
            logging.error("Error checking tracking status: %s", e)
            break


def main():
    """Main execution"""
    if not API_KEY:
        logging.error("API key not found. Please set it in a .env file.")
        return

    uuid = initiate_tracking(API_KEY, SHIPMENTS)
    if uuid:
        check_tracking_status(API_KEY, uuid)


if __name__ == "__main__":
    main()
