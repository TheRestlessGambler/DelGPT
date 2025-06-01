import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_gemini_response(prompt):
    response = model.generate_content(
        prompt,
        generation_config={
            "max_tokens": 50000
        }
    )
    return response.text
