"""Module for extracting LinkedIn profile data."""

import time
import requests
import logging
from typing import Dict, Optional, Any

import config

logger = logging.getLogger(__name__)

def extract_linkedin_profile(
    linkedin_profile_url: str,
    api_key: Optional[str] = None,
    mock: bool = False
) -> Dict[str, Any]:
    """Extract LinkedIn profile data using the LinkdAPI service or loads a premade JSON file.

    Args:
        linkedin_profile_url: The LinkedIn profile URL to extract data from.
        api_key: LinkdAPI key. Required if mock is False.
        mock: If True, loads mock data from a premade JSON file instead of using the API.

    Returns:
        Dictionary containing the LinkedIn profile data.
    """
    start_time = time.time()

    try:
        if mock:
            logger.info("Using mock data from a premade JSON file...")
            mock_url = config.MOCK_DATA_URL
            response = requests.get(mock_url, timeout=30)
            response.raise_for_status()
            data = response.json()
        else:
            # Ensure API key is provided when mock is False
            if not api_key:
                raise ValueError("API key is required when mock is set to False.")
            logger.info("Starting to extract the LinkedIn profile via LinkdAPI...")

            # LinkdAPI identifies profiles by username, taken from the end of the profile URL
            username = linkedin_profile_url.rstrip("/").split("/")[-1]

            # NOTE: verify this endpoint against LinkdAPI's current docs (linkdapi.com/docs)
            # before relying on it in production -- third-party API surfaces change over time.
            api_endpoint = "https://api.linkdapi.com/v1/profile/full"
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            params = {"username": username}

            logger.info(f"Sending API request to LinkdAPI at {time.time() - start_time:.2f} seconds...")

            response = requests.get(api_endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

        # Clean the data: remove empty values and fields we don't need
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
        }

        # Remove profile picture URLs from groups to clean the data
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url", None)

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to profile data source failed: {e}")
        return {}
    except ValueError as e:
        logger.error(f"Error parsing profile data response: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error in extract_linkedin_profile: {e}")
        return {}
