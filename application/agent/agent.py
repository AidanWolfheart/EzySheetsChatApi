from application.constants.constants import OPENAI_API_KEY
from langchain.llms import OpenAIChat
from langchain.tools import BaseTool
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import LLMChain
import os

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "A simple calculator tool"

    def _run(self, equation: str) -> str:
        """Use the tool to solve a math equation."""
        try:
            result = eval(equation)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, equation: str) -> str:
        """Use the tool asynchronously to solve a math equation."""
        raise NotImplementedError("CalculatorTool does not support async")


class Agent:
    def __init__(self):
        calculator = CalculatorTool()

        a_tool = [
            Tool(
                name=calculator.name,
                func=calculator.run,
                description=calculator.description
            )]

        prefix = """Have a conversation with a human, 
        answering the following questions as best you can. 
        You have access to the following tools:"""

        suffix = """Begin!"
        
        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            a_tool,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"]
        )

        new_memory = ConversationBufferMemory(memory_key="chat_history")

        turbo = OpenAIChat(model_name="gpt-3.5-turbo", temperature=0)
        llm_chain = LLMChain(llm=turbo, prompt=prompt)
        new_agent = ZeroShotAgent(llm_chain=llm_chain, tools=a_tool, verbose=True)
        self.agentExecutor = AgentExecutor.from_agent_and_tools(agent=new_agent,
                                                                tools=a_tool,
                                                                verbose=True,
                                                                memory=new_memory)
