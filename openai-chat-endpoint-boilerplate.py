import os
import openai
import tiktoken
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
enc = tiktoken.get_encoding("cl100k_base")


class ChatAssistant:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.messages = []

    def get_prompt(self, input):
        self.messages.append({"role": "user", "content": input})
        return self.messages

    def create_chat_completion(self, input):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.get_prompt(input),
        )
        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response

    def count_used_tokens(self):
        token_count = len(enc.encode(" ".join([msg["content"] for msg in self.messages])))
        token_cost = token_count / 1000 * 0.002  # gpt-3.5-turbo cost
        return f"🟡 Used tokens this round: {token_count} ({format(token_cost, '.5f')} USD)"


chat_assistant = ChatAssistant()

while True:
    user_input = input("You: ")
    completion = chat_assistant.create_chat_completion(user_input)
    print("Bot:", completion)
    print(chat_assistant.count_used_tokens())
