import os
import concurrent.futures
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def generate_idea(topic):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Give me one innovative startup idea for: {topic}"}],
        temperature=0.9
    )
    return response.choices[0].message.content

topics = ["FinTech", "HealthTech", "EdTech", "AgriTech"]

# --- Run in Parallel ---
print("Generating ideas in parallel...")
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(generate_idea, topics))

for topic, idea in zip(topics, results):
    print(f"\n--- {topic} ---\n{idea}")
