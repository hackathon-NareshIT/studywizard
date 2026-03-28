import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
# Force-load the .env file from the same folder as this script
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to your .env file."
    )

# Configure Gemini
genai.configure(api_key=api_key)

# Load model
# Use a currently supported Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(prompt):
    """Send a prompt to Gemini and return the response text."""
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No response generated."

    except Exception as e:
        return f"AI Error: {str(e)}"