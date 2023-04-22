from application.agent.agent import Agent, MyAppScriptZeroShotAgent


class AgentManager:
    def __init__(self):
        self.users_agent = {}

    def get_agent(self, userid):
        if userid not in self.users_agent:
            self.create_agent(userid)
        return self.users_agent[userid]

    def create_agent(self, userid):
        agent = MyAppScriptZeroShotAgent()
        self.users_agent[userid] = agent
        return agent
