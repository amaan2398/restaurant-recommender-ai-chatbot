from src.ai.gemini_api import InfoExtractionChatBot
from src.yelp.yelp_api import YelpAPI


def search_restaurants(yelp: YelpAPI, cuisine, location, price=None, limit=5):
    """
    Searches for restaurants using the Yelp API with a given query.

    Args:
        yelp (YelpAPI): An instance of the YelpAPI class.
        cuisine (str): The cuisine to search for.
        location (str): The location for the search.
        price (str): The price tier.

    Returns:
        A list of formatted restaurant dictionaries.
    """
    term = cuisine if cuisine else "restaurant"
    businesses = yelp.search(term=term, location=location, price=price, limit=limit)
    return YelpAPI.format_businesses_for_chatbot(businesses)


def chat_response(user_input, gemini: InfoExtractionChatBot, yelp: YelpAPI):
    """
    Handles the core logic of processing a user's chat message and returning a response.

    Args:
        user_input (str): The user's message.
        gemini (InfoExtractionChatBot): An instance of the InfoExtractionChatBot class.
        yelp (YelpAPI): An instance of the YelpAPI class.

    Returns:
        A dictionary containing the bot's response.
    """
    gemini_reply = gemini.get_info_from_prompt(user_input)
    if not gemini_reply:
        return {
            "type": "text",
            "content": "❌ Sorry, I couldn't extract the necessary information from your request.",
        }

    restaurants = search_restaurants(
        yelp=yelp,
        cuisine=gemini_reply.get("cuisine"),
        location=gemini_reply.get("location"),
        price=gemini_reply.get("price"),
        limit=gemini_reply.get("limit", 5),
    )

    if not restaurants:
        return {"type": "text", "content": "😞 Sorry, I couldn't find any matching restaurants."}

    # Sort the restaurants by rating from lowest to highest.
    restaurants = sorted(restaurants, key=lambda x: x["rating"])

    return {"type": "cards", "data": restaurants}
