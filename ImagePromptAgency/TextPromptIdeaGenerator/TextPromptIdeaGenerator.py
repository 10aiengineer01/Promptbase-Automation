from agency_swarm.agents import Agent


class TextPromptIdeaGenerator(Agent):
    def __init__(self):
        super().__init__(
            name="TextPromptIdeaGenerator",
            description="Responsible for creating unique text prompt ideas and edit them.",
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
