# Restaurant Recommender AI Chat Bot

A conversational AI chatbot that recommends restaurants based on user preferences, powered by Google Gemini or OpenAI ChatGPT APIs, and uses the Yelp API for backend restaurant data.

## Features

- Natural language restaurant recommendations
- Integrates with Google Gemini or ChatGPT API
- Fetches real restaurant data using the Yelp API
- Customizable cuisine, location, and budget filters
- Modern, user-friendly UI built with Streamlit
- Easy-to-use chat interface

## Getting Started

### Prerequisites

- Python 3.11+
- API key for Google Gemini or OpenAI ChatGPT
- Yelp API key

### Installation

```bash
git clone https://github.com/yourusername/restaurant-recommender-chatbot.git
cd restaurant-recommender-chatbot
pip install -r requirements.txt
```

### Configuration

1. Add your API keys to `.env`:

    ```
    API_KEY=your_ai_api_key_here
    YELP_API_KEY=your_yelp_api_key_here
    ```

2. Select the AI API provider in `config.py`.

### Usage

```bash
streamlit run app.py
```

Interact with the chatbot via a modern web interface powered by Streamlit.

## Technologies

- Python
- Google Gemini / OpenAI ChatGPT API
- Yelp API (for restaurant data)
- Streamlit (for web UI)

## License

MIT License

## Acknowledgements

- [OpenAI](https://openai.com/)
- [Google Gemini](https://ai.google/)
- [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3)
- [Streamlit](https://streamlit.io/)