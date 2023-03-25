from application.agent.agent import Agent, MyAppScriptZeroShotAgent

if __name__ == "__main__":
    agent = MyAppScriptZeroShotAgent()
    while True:
        user_input = input("Enter a message: ")
        if user_input == 'exit':
            exit
        response = agent.agent_executor.run(input=user_input)
        print(response)
