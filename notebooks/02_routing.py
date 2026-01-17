import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()

# Define the router structure
class Route(BaseModel):
    category: str
    urgency: str

def route_query(query):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Classify the query into: 'technical_support', 'billing', or 'general_inquiry'. Determine urgency: 'high' or 'low'."},
            {"role": "user", "content": query},
        ],
        response_format=Route,
    )
    return completion.choices[0].message.parsed

# --- Example Usage ---
queries = [
    "My server is down and I'm losing customers!",
    "How do I update my credit card?",
    "What is the pricing for the enterprise plan?"
]

print(f"{'QUERY':<50} | {'CATEGORY':<20} | {'URGENCY'}")
print("-" * 85)

for q in queries:
    route = route_query(q)
    print(f"{q:<50} | {route.category:<20} | {route.urgency}")
