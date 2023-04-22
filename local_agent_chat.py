from application.agent.agent import Agent, MyAppScriptZeroShotAgent
import logging

if __name__ == "__main__":
    logging.getLogger('gunicorn.error')
    agent = MyAppScriptZeroShotAgent()
    while True:
        user_input = input("Enter a message: ")
        if user_input == 'exit':
            exit
        response = agent.agent_executor.run(input=user_input)
        logging.info(response)
