import os
from toolhouse import Toolhouse
# 👋 Make sure you've also installed the Groq SDK through: pip install groq
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# If you don't specify an API key, Toolhouse will expect you
# specify one in the TOOLHOUSE_API_KEY env variable.
th = Toolhouse()
messages = [{
    "role": "user",
    "content":
        "Generate FizzBuzz code."
        "Execute it to show me the results up to 15."
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

print(response.choices[0].message.content)