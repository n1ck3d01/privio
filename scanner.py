from openai import OpenAI
import os

# Connect to Featherless AI using your hidden key
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=os.environ.get("FEATHERLESS_API_KEY")
)

def scan_privacy_policy(legal_text):
    print("🤖 AI is scanning the document for red flags... Please wait.\n")
    
    # We send the instructions (system prompt) and the text (user prompt) to Qwen
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct", 
        messages=[
            {
                "role": "system", 
                "content": "You are a privacy advocate. Read this terms of service text. Extract and summarize any clauses where the company shares data with third parties, tracks location, or claims ownership of user content. Explain the risks to a teenager in very simple terms. If it is safe, say 'Looks good!'"
            },
            {
                "role": "user", 
                "content": f"Here is the policy: {legal_text}"
            }
        ]
    )
    
    return response.choices[0].message.content

# --- Let's test it out with a fake, sketchy privacy policy ---
sketchy_policy = """
By using this app, you agree to grant us a non-exclusive, royalty-free license to use, reproduce, 
and distribute all photos uploaded. We may also collect background GPS location data to improve 
our services and share this data with our marketing partners and third-party affiliates.
"""

print("--- 🚨 Terms of Service Scanner 🚨 ---")
print(scan_privacy_policy(sketchy_policy))