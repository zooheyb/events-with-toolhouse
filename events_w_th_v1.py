import os
from toolhouse import Toolhouse
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Instantiates the Toolhouse class & creates a message.
th = Toolhouse()
th.set_metadata('id', 'Zuhaib')
messages = [{
    "role": "user",
    "content":
        "Search the internet for the next 10 Gen AI tech events in San Francisco after Oct 23, 2024"
        "Include their dates and print them"
   }]
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

# Extract the content from the response
response_content = response.choices[0].message.content

# Store the response content as a variable
events_info = response_content

print(events_info)

messages = [{
    "role": "user",
    "content":
         "Write and print the code for a visual dashboard displaying 10 events using Streamlit"
        f"These are the 10 events: \n{events_info}\n"
        #"Email me a table with the events to zuhaib.mohiuddin@gmail.com"
   }]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

print(response.choices[0].message.content)

messages = [{
    "role": "user",
    "content":
        "Confirm the dashboard code" 
        "Run the code with the code interpreter tool"
   }]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)
print('123')