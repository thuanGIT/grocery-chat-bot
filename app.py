from app.agent import Agent
# from dialogflow_migration.bot import Bot

def main():
    agent = Agent()
    #initiate conversation with customer
    agent.start_conversation()


if __name__ == '__main__':
  main()