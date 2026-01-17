import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_completion(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# --- Step 1: Extract Key Information ---
email_content = """
Subject: Project Alpha Update
From: sarah@example.com
Hi Team,
We've hit a delay in the frontend migration. We need an extra 2 weeks. 
Budget implication is approx $5k.
Can we get approval?
"""

extraction_prompt = f"""
Extract the key issue, requested time, and budget impact from this email:
{email_content}
"""

step_1_output = get_chat_completion(extraction_prompt)
print(f"--- Step 1 Output ---\n{step_1_output}\n")

# --- Step 2: Draft a Response (Chained) ---
response_prompt = f"""
Based on the following issue summary, draft a professional response to Sarah.
Acknowledge the delay but ask for a breakdown of the $5k costs.

Issue Summary:
{step_1_output}
"""

step_2_output = get_chat_completion(response_prompt)
print(f"--- Final Output (Step 2) ---\n{step_2_output}")
