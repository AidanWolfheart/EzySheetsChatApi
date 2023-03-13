import kwargs as kwargs
from langchain import PromptTemplate

from application.agent.load_tools import load_tools
from application.constants.constants import OPENAI_API_KEY
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain, SequentialChain
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

from application.tools.GoogleSheetsTool import GoogleSheetsBatchUpdateTool, GoogleSheetsCreateTool
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


class Agent:
    def __init__(self):
        tools = load_tools()

        prefix = """You are Ezy a software that helps users to deal with Google Sheets. 
        You execute user request related to Google Sheets by writing json code and executing it with google sheets api.
        Assume you have already been authenticated and authorized.
        Use google sheets formulas to complete the user requests where possible.
        You have access to the following tools:""".replace('\n', '').replace('  ', '')

        suffix = """Begin! Remember to execute user request related to Google Sheets by using google sheets api."""

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

        llm_chain = LLMChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), prompt=prompt, verbose=True)

        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

        # agent_executor.run("Make a spreadsheet.")


class Agent1:
    def __init__(self):
        tools = [GoogleSheetsBatchUpdateTool(api_wrapper=GoogleSheetsToolWrapper())]

        PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
        SUFFIX = """Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""

        codex = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        template1 = """
        {input}\n\nThis was your previous work "
                                                     f"(but I haven't seen any of it! I only see what "
                                                     "you return as final answer):\n{agent_scratchpad}
        You are a Google Sheets API assistant. Given the user's request, it is your job to make a json code that would be executable in Google Sheets API. Users might ask to make formulas and it's you job to provide them with them.

        Request: {request}
        Assistant: This is a json code for the Google Sheets API request:"""
        prompt_template1 = PromptTemplate(input_variables=["request", 'input', 'agent_scratchpad'], template=template1)
        json_chain = LLMChain(llm=codex, prompt=prompt_template1, output_key="json_code", verbose=True)

        template2 = """You are a code executor. Given the json code for Google Sheets API you execute using the {tool}.

        Code: {code}
        Code Executor: This a code to execute the provided json code:"""

        # prompt_template2 = PromptTemplate(input_variables=["code"], template=template2)


        #=================================
        prefix = """You are a code executor. You get the json code for Google Sheets API from previous chain and you execute using the tool. You have access to the following tools:"""
        suffix = """Begin! Remember to execute user request related to Google Sheets by using the tools. Please use the tool if it's about Google Sheets if not respond with I don't know"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=[]
        )

        messages = [
            SystemMessagePromptTemplate(prompt=prompt),
            HumanMessagePromptTemplate.from_template("{input}\n\nThis was your previous work "
                                                     f"(but I haven't seen any of it! I only see what "
                                                     "you return as final answer):\n{agent_scratchpad}")
        ]

        prompt = ChatPromptTemplate.from_messages(messages)

        chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.1)

        code_chain = LLMChain(llm=chat, prompt=prompt, output_key="result", verbose=True)

        # This is the overall chain where we run these two chains in sequence.

        overall_chain = SequentialChain(chains=[json_chain, code_chain],
                                        input_variables=["request", 'input', 'agent_scratchpad'],
                                        output_variables=["json_code", "result"], verbose=True)

        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=overall_chain, allowed_tools=tool_names)

        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

        # agent_executor.run("Make a spreadsheet.")
