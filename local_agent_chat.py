from application.agent.agent import Agent

if __name__ == "__main__":
    agent = Agent()
    while True:
        user_input = input("Enter a message: ")
        if user_input == 'exit':
            exit
        response = agent.agent_executor.run(input=user_input)
        print(response)
