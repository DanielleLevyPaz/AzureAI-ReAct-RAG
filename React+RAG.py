#env
# AZURE_OAI_ENDPOINT=https://<your-openai-endpoint>.openai.azure.com/
# AZURE_OAI_KEY=<your-openai-key>
# AZURE_OAI_DEPLOYMENT=gpt-4o
# AZURE_SEARCH_ENDPOINT=https://<your-search-name>.search.windows.net/
# AZURE_SEARCH_KEY=<your-search-admin-key>
# AZURE_SEARCH_INDEX=margies-index

import os
import asyncio
import openai
import wikipedia
from datetime import datetime
from dotenv import load_dotenv

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory

# ---------------------
# Step 1: Load Environment Variables
# ---------------------
load_dotenv()
openai_api_key = os.getenv("AZURE_OAI_KEY")
deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
endpoint = os.getenv("AZURE_OAI_ENDPOINT")
api_version = "2024-02-01"

# ---------------------
# Step 2: Define Tools
# ---------------------
def get_current_datetime(*args, **kwargs):
    return datetime.now().isoformat()

def get_wikipedia_summary(query):
    try:
        return wikipedia.summary(query)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation error: {e}"
    except wikipedia.exceptions.PageError:
        return "Page not found."
    except Exception as e:
        return str(e)

def search_company_docs(query: str) -> str:
    try:
        client = openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=openai_api_key,
            api_version=api_version,
        )

        completion = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": query}],
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
                            "index_name": os.environ["AZURE_SEARCH_INDEX"],
                            "authentication": {
                                "type": "api_key",
                                "key": os.environ["AZURE_SEARCH_KEY"],
                            }
                        }
                    }
                ]
            }
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Search error: {e}"

# List of tools
tools = [
    Tool(
        name="Date Time",
        func=get_current_datetime,
        description="Useful for checking the current date and time."
    ),
    Tool(
        name="Wikipedia",
        func=get_wikipedia_summary,
        description="Useful for getting Wikipedia summaries."
    ),
    Tool(
        name="Company Knowledge Base",
        func=search_company_docs,
        description="Use this to search internal documents and get grounded answers from the knowledge base."
    ),
]

# ---------------------
# Step 3: Load Prompt and LLM
# ---------------------
prompt = hub.pull("hwchase17/react")

llm = AzureChatOpenAI(
    azure_deployment=deployment,
    azure_endpoint=endpoint,
    api_key=openai_api_key,
    api_version=api_version,
    temperature=0,
)

# ---------------------
# Step 4: Set Up Memory
# ---------------------
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    max_token_limit=150,
    return_messages=True,
    k=10
)

# ---------------------
# Step 5: Build Agent and Executor
# ---------------------
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)

# ---------------------
# Step 6: Async Main Loop
# ---------------------
async def main():
    print("🤖 ReAct Agent with RAG + Tools + Memory (LangChain + Azure OpenAI)")
    while True:
        query = input("\nAsk something (or 'quit'): ")
        if query.lower() == "quit":
            break
        response = await agent_executor.ainvoke({"input": query})
        print("\n📣 Response:\n", response["output"])


if __name__ == '__main__':
    asyncio.run(main())