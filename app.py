# import os

# import streamlit as st
# from dotenv import load_dotenv

# from src.ai.gemini_api import InfoExtractionChatBot
# from src.yelp.yelp_api import YelpAPI


# # --- Helper: Search Restaurants ---
# def search_restaurants(cuisine, location, price=None, open_now=True):
#     term = cuisine if cuisine else "restaurant"
#     businesses = yelp.search(term=term, location=location, limit=5)
#     return YelpAPI.format_businesses_for_chatbot(businesses)


# # --- Chat Processing ---
# def chat_response(user_input):
#     gemini_reply = gemini.get_info_from_prompt(user_input)
#     if not gemini_reply:
#         return {
#             "type": "text",
#             "content": "❌ Sorry, I couldn't extract the necessary information from your request.",
#         }

#     restaurants = search_restaurants(
#         cuisine=gemini_reply.get("cuisine"),
#         location=gemini_reply.get("location"),
#         price=gemini_reply.get("price"),
#         open_now=True,
#     )

#     if not restaurants:
#         return {"type": "text", "content": "😞 Sorry, I couldn't find any matching restaurants."}

#     # Sort the restaurants by rating from lowest to highest.
#     restaurants = sorted(restaurants, key=lambda x: x["rating"])

#     return {"type": "cards", "data": restaurants}


# # --- Load environment variables ---
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# YELP_API_KEY = os.getenv("YELP_API_KEY")

# # --- Streamlit Page Config ---
# st.set_page_config(page_title="Restaurant Recommendation ChatBot", page_icon="🍽️", layout="wide")

# # --- Header ---
# st.title("🍽️ Restaurant Recommendation ChatBot")
# st.caption("Find the best places to eat based on your preferences")

# with st.expander("🔑 Debug API Keys"):
#     st.write(f"Google Gemini Key: `{GOOGLE_API_KEY}`")
#     st.write(f"Yelp API Key: `{YELP_API_KEY}`")

# st.markdown("---")

# # --- Initialize Session State ---
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- Instantiate APIs ---
# gemini = InfoExtractionChatBot(api_key=GOOGLE_API_KEY)
# yelp = YelpAPI(api_key=YELP_API_KEY)

# # --- User Input ---
# st.markdown("### 💬 Ask me anything about restaurants!")
# user_input = st.text_input(
#     "Type your query (e.g., *Find me a sushi place in New York*)", key="input"
# )

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     bot_reply = chat_response(user_input)
#     st.session_state.messages.append({"role": "bot", "content": bot_reply})


# # --- Chat History ---
# def render_restaurant_card(restaurant):
#     """Returns the HTML string for a single restaurant card, now with an interactive map using an iframe."""
#     # The URL for Google Maps embeds
#     iframe_url = f"https://maps.google.com/maps?q={restaurant['address']}&output=embed"
#     maps_link = f"http://maps.google.com/?q={restaurant['address']}"

#     return f"""
#         <div style="
#             border: 1px solid var(--border-color);
#             background-color: var(--secondary-background-color);
#             border-radius: 10px;
#             padding: 15px;
#             margin: 5px;
#             min-width: 300px;
#             box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between;
#         ">
#             <h4><a href="{maps_link}" target="_blank" style="text-decoration: none; color: var(--text-color);">{restaurant['name']}</a></h4>
#             <div style="
#                 border-radius: 8px;
#                 overflow: hidden;
#                 margin-top: 10px;
#                 margin-bottom: 10px;
#             ">
#                 <iframe
#                     src="{iframe_url}"
#                     style="border:0;"
#                     width="100%"
#                     height="150"
#                     allowfullscreen=""
#                     loading="lazy"
#                     referrerpolicy="no-referrer">
#                 </iframe>
#             </div>
#             <p style="margin-top: 0; color: var(--text-color);"><strong>⭐ Rating:</strong> {restaurant['rating']}</p>
#             <p style="color: var(--text-color);"><strong>📍 Address:</strong> {restaurant['address']}</p>
#         </div>
#     """


# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(
#             f"<div style='background:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0;'>"
#             f"<b>You:</b><br>{msg['content']}</div>",
#             unsafe_allow_html=True,
#         )
#     elif msg["role"] == "bot":
#         content = msg["content"]
#         if content.get("type") == "cards":
#             st.markdown("### 🍴 Recommended Restaurants")
#             # Container for the horizontally scrolling cards
#             print(f"Displaying {content['data']} restaurant cards.")
#             card_html = "".join([render_restaurant_card(r) for r in content["data"]])
#             st.markdown(
#                 f"""
#                 <div style="
#                     display: flex;
#                     flex-direction: row;
#                     overflow-x: auto;
#                     padding: 10px 0;
#                     -webkit-overflow-scrolling: touch; /* For smoother scrolling on iOS */
#                     scrollbar-width: thin; /* For Firefox */
#                     scrollbar-color: #A9A9A9 #F1F0F0; /* For Firefox */
#                 ">
#                     {card_html}

#                 """,
#                 unsafe_allow_html=True,
#             )
#         else:
#             st.markdown(
#                 f"<div style='background:#F1F0F0; padding:10px; border-radius:10px; margin:5px 0;'>"
#                 f"<b>Bot:</b><br>{content['content']}</div>",
#                 unsafe_allow_html=True,
#             )

import os

import streamlit as st
from dotenv import load_dotenv

from core.logic import chat_response
from core.ui import render_chat_history
from src.ai.gemini_api import InfoExtractionChatBot
from src.yelp.yelp_api import YelpAPI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
YELP_API_KEY = os.getenv("YELP_API_KEY")

# Streamlit Page Config
st.set_page_config(page_title="Restaurant Recommendation ChatBot", page_icon="🍽️", layout="wide")

# Header and Expander
st.title("🍽️ Restaurant Recommendation ChatBot")
st.caption("Find the best places to eat based on your preferences")
with st.expander("🔑 Debug API Keys"):
    st.write(f"Google Gemini Key: `{GOOGLE_API_KEY}`")
    st.write(f"Yelp API Key: `{YELP_API_KEY}`")
st.markdown("---")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Instantiate APIs
gemini = InfoExtractionChatBot(api_key=GOOGLE_API_KEY)
yelp = YelpAPI(api_key=YELP_API_KEY)

# User Input and Response
st.markdown("### 💬 Ask me anything about restaurants!")
user_input = st.text_input(
    "Type your query (e.g., *Find me a sushi place in New York*)", key="input"
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = chat_response(user_input, gemini, yelp)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# Render Chat History
render_chat_history()
