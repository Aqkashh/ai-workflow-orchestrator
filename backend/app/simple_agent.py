class SimpleAgent:
    def __init__(self, name,role):
        self.name = name
        self.role = role

    def run(self,message):
        print(f"{self.name} Role:  {self.role}")
        print(f"input message: {message}")
        return "Agent recieved your message."
    
if __name__ == "__main__":
    agent = SimpleAgent("TestAgent", "Just print whatever message I get.")
    result = agent.run("Hello agent!")
    print("Returned:", result)

