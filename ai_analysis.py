import os
import json
import asyncio

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


# Create Gemini client
client = genai.Client(
    api_key=API_KEY
)


async def analyze_expenses(expense_data):

    # No expenses
    if not expense_data:

        return {
            "high_spending_categories": [],
            "spending_patterns": [],
            "suggestions": [],
            "message": "Please add expenses to generate AI insights."
        }


    # Prompt sent to Gemini
    prompt = f"""
You are an intelligent personal finance assistant.

Analyze the following expense data:

{json.dumps(expense_data, indent=2)}

Your task is to understand the user's spending behavior.

Generate:

1. High spending categories
2. Spending patterns
3. Practical suggestions
4. A short overall analysis

Important rules:

- Use ONLY the expense data provided.
- Do not invent transactions.
- Do not invent amounts.
- Identify meaningful spending patterns.
- Give practical and understandable suggestions.
- Mention actual categories and amounts when useful.
- Keep the response concise and useful for a student.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not use code fences.

Return exactly this structure:

{{
    "high_spending_categories": [
        "Food: ₹500"
    ],

    "spending_patterns": [
        "Your spending is highest in Food."
    ],

    "suggestions": [
        "Consider setting a monthly budget for Food."
    ],

    "message": "Your overall spending analysis..."
}}
"""


    # Gemini API call
    response = await asyncio.to_thread(
        client.models.generate_content,
        model="gemini-3.8-flash",
        contents=prompt
    )


    # Get Gemini response
    response_text = response.text.strip()


    # Remove accidental Markdown code fences
    if response_text.startswith("```"):

        response_text = response_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()


    # Convert JSON text into Python object
    result = json.loads(response_text)


    # Return only expected fields
    return {

        "high_spending_categories":
            result.get(
                "high_spending_categories",
                []
            ),

        "spending_patterns":
            result.get(
                "spending_patterns",
                []
            ),

        "suggestions":
            result.get(
                "suggestions",
                []
            ),

        "message":
            result.get(
                "message",
                ""
            )
    }