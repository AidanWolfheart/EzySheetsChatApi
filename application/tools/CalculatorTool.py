from langchain.tools import BaseTool

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