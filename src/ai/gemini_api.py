import json
import os
import re

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class InfoExtractionChatBot:
    """
    Extracts cuisine, location, and price from user prompt using few-shot learning.
    Returns dict with keys: cuisine, location, price
    """

    def __init__(self, api_key=None, model_name="gemini-1.5-flash"):
        self.llm_api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=self.llm_api_key,
            temperature=0,
        )

        # --- Define JSON schema for output ---
        response_schemas = [
            ResponseSchema(name="cuisine", description="Type of cuisine"),
            ResponseSchema(name="location", description="City or location"),
            ResponseSchema(name="price", description="Price category (cheap, moderate, expensive)"),
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # --- Few-shot examples ---
        examples = [
            {
                "user_prompt": "Find me a cheap sushi place in San Francisco",
                "output": '{{"cuisine": "sushi", "location": "San Francisco", "price": "cheap", "limit": 5}}',
            },
            {
                "user_prompt": "I want Italian food in New York, not too expensive (3 restaurants)",
                "output": '{{"cuisine": "Italian", "location": "New York", "price": "moderate", "limit": 3}}',
            },
            {
                "user_prompt": "Recommend a fancy French restaurant in Paris for a special occasion (2 restaurants)",
                "output": '{{"cuisine": "French", "location": "Paris", "price": "expensive", "limit": 2}}',
            },
            {
                "user_prompt": "Recommend a desi indian restaurant in Paris 4 restaurants",
                "output": '{{"cuisine": "Indian", "location": "Paris", "price": "very expensive", "limit": 4}}',
            },
        ]

        example_prompt = PromptTemplate(
            input_variables=["user_prompt", "output"],
            template="User: {user_prompt}\nExtracted: {output}",
        )

        self.prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=(
                "Extract cuisine, location, suggestion count(limit) and price from the user prompt. "
                "Respond only with JSON in the following format:\n"
                '{{"cuisine": "###", "location": "###", "price": "###", "limit": "###"}}\n'
            ),
            suffix="User: {user_prompt}\nExtracted:",
            input_variables=["user_prompt"],
        )

        # --- Chain with enforced JSON output ---
        self.chain = self.prompt | self.llm | self.output_parser

    def get_info_from_prompt(self, user_prompt: str):
        """
        Get structured info from user prompt.
        """
        return self.chain.invoke({"user_prompt": user_prompt})
