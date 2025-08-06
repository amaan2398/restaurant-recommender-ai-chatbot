import streamlit as st


def render_restaurant_card(restaurant):
    """Returns the HTML string for a single restaurant card."""
    # Corrected Google Maps iframe URL
    iframe_url = f"https://maps.google.com/maps?q={restaurant['address']}&output=embed"
    # Corrected Google Maps link URL
    maps_link = f"https://maps.google.com/?q={restaurant['address']}"

    # Determine the open status text and color
    is_open = restaurant.get("is_open_now", False)
    open_status_text = "Open now" if is_open else "Closed"
    open_status_color = "green" if is_open else "red"

    # Format transactions for display
    transactions = ", ".join(restaurant.get("transactions", [])).replace("_", " ").title()

    # Format categories for display
    categories = ", ".join(restaurant.get("categories", []))

    return f"""
        <div style="
            border: 1px solid var(--border-color);
            background-color: transparent !important;
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            min-width: 300px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <h4>
                <a href="{maps_link}" target="_blank" style="text-decoration: none; color: var(--text-color);">{restaurant['name']}</a>
            </h4>
            <div style="
                border-radius: 8px;
                overflow: hidden;
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: transparent !important;
            ">
                <iframe
                    src="{iframe_url}"
                    style="border:0;"
                    width="100%"
                    height="150"
                    allowfullscreen=""
                    loading="lazy"
                    referrerpolicy="no-referrer">
                </iframe>
            </div>
            <p style="margin-top: 0; color: var(--text-color);"><strong>⭐ Rating:</strong> {restaurant['rating']} ({restaurant['review_count']} reviews)</p>
            <p style="color: var(--text-color);"><strong>📍 Address:</strong> {restaurant['address']}</p>
            <p style="color: var(--text-color);"><strong>📞 Phone:</strong> {restaurant.get('phone', 'N/A')}</p>
            <p style="color: var(--text-color);"><strong>🏷️ Categories:</strong> {categories if categories else 'N/A'}</p>
            <p style="color: {open_status_color}; margin-bottom: 5px;"><strong>⏰ Status:</strong> {open_status_text}</p>
            <p style="color: var(--text-color);"><strong>💳 Transactions:</strong> {transactions if transactions else 'N/A'}</p>
            <a href="{restaurant['url']}" target="_blank" style="color: var(--primary-color); text-decoration: none;">View on Yelp</a>
        </div>
    """


def render_chat_history():
    """Renders the full chat history stored in Streamlit's session state."""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            html_string = f"""<div style='background:var(--background-color); padding:10px; border-radius:10px; margin:5px 0;'>
                <b>You:</b><br>{msg['content']}</div>"""
            st.markdown(
                html_string,
                unsafe_allow_html=True,
            )
        elif msg["role"] == "bot":
            content = msg["content"]
            if content.get("type") == "cards":
                st.markdown("### 🍴 Recommended Restaurants")
                card_html = "".join([render_restaurant_card(r) for r in content["data"]])
                html_string = f"""
                    <div style="
                        display: flex;
                        flex-direction: row;
                        overflow-x: auto;
                        padding: 10px 0;
                        -webkit-overflow-scrolling: touch;
                        scrollbar-width: thin;
                        scrollbar-color: #A9A9A9 #F1F0F0;
                    ">
                        {card_html}
                    </div>
                    """
                st.markdown(html_string, unsafe_allow_html=True)
            else:
                # Corrected: Combine into a single f-string to ensure proper HTML structure
                html_string = f"""
                    <div style='background:#F1F0F0; padding:10px; border-radius:10px; margin:5px 0;'>
                        <b>Bot:</b><br>{content['content']}
                    </div>
                    """
                st.markdown(html_string, unsafe_allow_html=True)
