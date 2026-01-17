import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def generate_code(task):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Python coding assistant. Output only code."},
            {"role": "user", "content": task}
        ]
    )
    return response.choices[0].message.content

def critique_code(code):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Review this code for bugs or security issues. If none, say 'PASS'."},
            {"role": "user", "content": code}
        ]
    )
    return response.choices[0].message.content

# --- The Loop ---
task = "Write a python function to calculate fibonacci recursively without a base case."

# 1. Draft
draft_code = generate_code(task)
print(f"--- Draft Code ---\n{draft_code}\n")

# 2. Critique
critique = critique_code(draft_code)
print(f"--- Critique ---\n{critique}\n")

# 3. Refine (if needed)
if "PASS" not in critique:
    final_code = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Fix this code based on the critique:\nCode: {draft_code}\nCritique: {critique}"}
        ]
    ).choices[0].message.content
    print(f"--- Final Polished Code ---\n{final_code}")
else:
    print("Code passed initial checks.")
