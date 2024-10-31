import os
from typing import List
# 👋 Make sure you've also installed the OpenAI SDK through: pip install openai
from openai import OpenAI
from toolhouse import Toolhouse

# Let's set our API Keys.
# Please remember to use a safer system to store your API KEYS 
# after finishing the quick start.
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
th = Toolhouse(api_key='TOOLHOUSE_API_KEY',
               provider= "openai")

# Define the OpenAI model we want to use
MODEL = 'gpt-4o-mini'
th = Toolhouse()
th.set_metadata('id', 'Zuhaib')

messages = [{
    "role": "user",
    "content":
        #"Delete all memory stored with my ID including events and email"
        "Show me what memories are associated with my ID"
}]

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools()
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
messages += th.run_tools(response)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools()
)
# Prints the response with the answer
print(response.choices[0].message.content)