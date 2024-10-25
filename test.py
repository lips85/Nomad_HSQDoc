import os

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

llm = ChatAnthropic(
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
    model_name="claude-3-sonnet-20240229",
)

llm2 = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY_PROJECT"],
    model_name="gpt-4o-mini",
)

print(llm.invoke("Hello, how are you?"))
print(llm2.invoke("Hello, how are you?"))
