from agency_swarm.agents import Agent


class TextPromptCEO(Agent):
    def __init__(self):
        super().__init__(
            name="TextPromptCEO",
            description="Guides the whole text prompt creation process and coordinates the other agents.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
        )
        
    def response_validator(self, message):
        return message
