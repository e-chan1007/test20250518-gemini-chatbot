from dotenv import load_dotenv

load_dotenv()

import os

from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))

chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="あなたは日本語を話すAIアシスタントです。ユーザーの質問に答えたり、情報を提供したりします。",
    ),
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat.send_message_stream(user_input)
    for chunk in response:
        print(chunk.text, end="")
