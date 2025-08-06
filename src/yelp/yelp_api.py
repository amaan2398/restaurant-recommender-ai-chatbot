"""
# Yelp API Client
# This module provides a client for interacting with the Yelp API to search for businesses.
# It allows you to search for businesses and format the results for chatbot responses.
"""

import os

import requests


class YelpAPI:
    """
    A client for the Yelp API to search for businesses.
    """

    PRICE_TIERS = {
        "cheap": "1",
        "moderate": "2",
        "expensive": "3",
        "very expensive": "4",
    }

    def __init__(self, api_key=None, base_url=None):
        """Initialize the YelpAPI client."""
        self.api_key = api_key or os.getenv("YELP_API_KEY")
        self.base_url = base_url or "https://api.yelp.com/v3/businesses/search"
        if not self.api_key:
            raise ValueError(
                "Yelp API key not found. Please set the YELP_API_KEY environment variable."
            )

    def search(self, term, location, price, limit=5):
        """
        Search Yelp for businesses matching the term and location.
        Returns a list of business dictionaries.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "term": term,
            "location": location,
            "limit": limit,
            "price": self.PRICE_TIERS.get(price, "2"),
        }
        response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            raise Exception(
                f"Error fetching data from Yelp API: {response.status_code} - {response.text}"
            )
        response.raise_for_status()
        return response.json().get("businesses", [])

    @staticmethod
    def format_businesses_for_chatbot(businesses):
        """
        Format Yelp business results for chatbot response.
        """
        print("Formatting Yelp businesses for chatbot response...")
        results = []
        for b in businesses:
            print(f"Processing: {b}")
            categories_list = [c.get("title") for c in b.get("categories", []) if c.get("title")]
            hours_info = b.get("business_hours", [{}])[0]
            result = {
                "name": b.get("name"),
                "rating": b.get("rating"),
                "review_count": b.get("review_count"),
                "address": ", ".join(b.get("location", {}).get("display_address", [])),
                "phone": b.get("display_phone"),
                "url": b.get("url"),
                "is_closed": b.get("is_closed"),
                "categories": categories_list,
                "transactions": b.get("transactions", []),
                "is_open_now": hours_info.get("is_open_now", False) if hours_info else False,
            }
            results.append(result)
        return results


# Example usage:
# yelp = YelpAPI(api_key="your_api_key_here")
# businesses = yelp.search("pizza", "New York")
# formatted = YelpAPI.format_businesses_for_chatbot(businesses)
# print(formatted)
# formatted = YelpAPI.format_businesses_for_chatbot(businesses)
# print(formatted)
