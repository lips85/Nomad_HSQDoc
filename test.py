import os

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
    model_name="claude-3-sonnet-20240229",
)

print(llm.invoke("Hello, how are you?"))
