from agency_swarm.agents import Agent


class PromptSender(Agent):
    def __init__(self):
        super().__init__(
            name="PromptSender",
            description="Responsible for sending the result to the user",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            model="gpt-4o-mini"
        )
        
    def response_validator(self, message):
        return message
