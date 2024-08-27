from agency_swarm.agents import Agent


class PromptCEOSelector(Agent):
    def __init__(self):
        super().__init__(
            name="PromptCEOSelector",
            description="Selects the prompttype that needs to be created",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
        )
        
    def response_validator(self, message):
        return message
