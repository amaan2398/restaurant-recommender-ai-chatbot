"""
# Gemini API Client
# This module provides a client for interacting with the Gemini API to get recommendations.
# It allows you to send prompts and receive recommendations based on those prompts.
"""

import os

import requests


class GeminiAPI:
    """
    A client for the Gemini API to fetch recommendations based on user prompts.
    """

    def __init__(self, api_key=None, base_url=None):
        """Initialize the GeminiAPI client."""
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url or "https://api.gemini.com/v1"

    def get_recommendations(self, prompt, max_tokens=128):
        """Fetch recommendations from the Gemini API based on a user prompt."""
        url = f"{self.base_url}/recommend"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "max_tokens": max_tokens}
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # Check for errors in the response
        if response.status_code != 200:
            raise Exception(
                f"Error fetching recommendations: {response.status_code} - {response.text}"  # error handling
            )
        response.raise_for_status()
        return response.json()


# Example usage:
# gemini = GeminiAPI(api_key="your_api_key_here")
# result = gemini.get_recommendations("Suggest a movie for tonight")
# print(result)
