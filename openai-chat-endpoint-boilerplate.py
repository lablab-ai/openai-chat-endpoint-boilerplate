import os
import openai
import tiktoken
from dotenv import load_dotenv
load_dotenv()
openai.api_key =  os.getenv('OPENAI_API_KEY')
enc = tiktoken.get_encoding("cl100k_base")

messages = []

def get_prompt(input):
    context = []
    messages.append(input)
    for index, message in enumerate(messages):
        if index % 2 == 0:
            context.append({"role": "user", "content": message})
        else:
            context.append({"role": "assistant", "content": message})
    return context

def create_chat_completion(input):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #  you can also go with gpt-4 here (cost will be different! https://openai.com/pricing )
        messages=get_prompt(input),
    )
    messages.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def count_used_tokens():
    token_count = len(enc.encode(" ".join(messages)))
    token_cost = token_count / 1000 * 0.002 # gpt-3.5-turbo cost
    return "🟡 Used tokens this round: " + str(token_count) + " (" + format(token_cost, '.5f') + " USD)"

while True:
    user_input = input("You: ")
    completion = create_chat_completion(user_input)
    print("Bot:", completion)
    print(count_used_tokens())