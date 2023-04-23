from application.agent.agent_manager import AgentManager


class MessageHandler:
    def __init__(self):
        self.agent_manager = AgentManager()

    def handle_message(self, userid, msg):
        agent = self.agent_manager.get_agent(userid)
        return agent.agent_executor.run(input=msg)

