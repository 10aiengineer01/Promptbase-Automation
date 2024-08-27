from agency_swarm.agents import Agent


class ImagePromptCEO(Agent):
    def __init__(self):
        super().__init__(
            name="ImagePromptCEO",
            description="Guides the whole creation process and coordinates the other agents.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
        )
        
    def response_validator(self, message):
        return message
