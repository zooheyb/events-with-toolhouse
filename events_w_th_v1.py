# Imports the OS Module and the Toolhouse & Groq classes.
import os
from toolhouse import Toolhouse
from groq import Groq

# Instantiates the Groq client with the API key.
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Instantiates the Toolhouse class & creates a message.
th = Toolhouse()
#th.set_metadata('zuhaib', -8)
messages = [{
    "role": "user",
    "content":
        "Given the date of October 21, 2024 what are the next five events you see on the url https://lu.ma/sf?utm_source=dp_email"
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