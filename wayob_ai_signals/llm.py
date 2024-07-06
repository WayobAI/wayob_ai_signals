import os

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAI

from .constants import AI_TOKEN
from .documents import (
    get_vectorstore,
    multi_query_retriever,
)
from .mappings import MODEL_MAP

os.environ["OPENAI_API_KEY"] = AI_TOKEN


class AIChatbot:
    def __init__(
        self,
        mode,
        memory=True,
        documents=None,
    ):
        self.mode = mode
        self.memory = memory
        self.documents = documents
        self.llm = ChatOpenAI(
            model_name=MODEL_MAP[mode],
            temperature=0,
        )
        self.prompt, self.tool = self.setup_prompt_and_tool()
        self.agent = self.setup_agent()

    def setup_prompt_and_tool(self):
        # Code to configure the prompt and external tools
        pass

    def create_memory(self):
        # Code to create memory
        pass

    def setup_agent(self):
        # Code to configure the agent
        pass

    async def get_response(self, message):
        try:
            # Code to get response
            pass
        except Exception as e:
            print(e)
            return "Sorry, I couldn't process your request. Please try again later."
