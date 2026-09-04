from openai import OpenAI
import os

# This connects to Featherless using your hidden key
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=os.environ.get("FEATHERLESS_API_KEY")
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {"role": "user", "content": "Say 'Connection successful!' if you can hear me."}
    ]
)

print(response.choices[0].message.content)