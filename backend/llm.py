import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_explanation(context, user_query=None):
    print(user_query)
    if user_query:
        query_instruction = f"User Query: {user_query}\n\nInstruction: Answer the user query directly using the data insights provided, then provide the standard summary below."
    else:
        query_instruction = "Instruction: Provide a standard forecasting summary."

    prompt = f"""
You are a forecasting analyst.

Data insights:
Trend strength: {context['trend']}
Seasonality strength: {context['seasonality']}
Noise level: {context['noise']}
Forecast range: {context['forecast']}
Anomalies: {context['anomalies']}
Model used: {context['model']}

{query_instruction}

Standard Summary:
1. What will happen
2. Why
3. Any risks
Keep it simple.

Do not start with "Okay, understood" or "Here is an explanation" or any other similar phrases.
"""

    response = model.generate_content(prompt)
    return response.text