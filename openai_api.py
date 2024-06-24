import os
import openai

api_key = os.getenv('OPENAI_API_KEY')


def request_response(prompt):
    openai.api_key = api_key  
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    #print(response)
    return response['choices'][0]['message']['content'].strip()

prompt = ""
print(request_response(prompt))
print("API Key used:", api_key)