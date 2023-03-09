import kwargs as kwargs

from application.constants.constants import OPENAI_API_KEY
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain
from langchain.utilities import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains.conversation.memory import ConversationBufferMemory
import os

from application.tools.GoogleSheetsTool import GoogleSheetsBatchUpdateTool
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


class Agent:
    def __init__(self):
        tools = [GoogleSheetsBatchUpdateTool(api_wrapper=GoogleSheetsToolWrapper())]

        prefix = """You are Ezy a software that helps users to deal with Google Sheets. You execute user request related to Google Sheets by writing json code and executing it with google sheets api. You have access to the following tools:"""
        suffix = """Begin! Remember to execute user request related to Google Sheets by using google sheets api. Please use the tool if it's about Google Sheets if not respond with I don't know"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=[]
        )

        messages = [
            SystemMessagePromptTemplate(prompt=prompt),
            HumanMessagePromptTemplate.from_template("{chat_history}\n\n{input}\n\nThis was your previous work "
                                                     f"(but I haven't seen any of it! I only see what "
                                                     "you return as final answer):\n{agent_scratchpad}")
        ]

        memory = ConversationBufferMemory(memory_key="chat_history")

        prompt = ChatPromptTemplate.from_messages(messages)

        llm_chain = LLMChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), prompt=prompt)

        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

        # agent_executor.run("Make a spreadsheet.")
