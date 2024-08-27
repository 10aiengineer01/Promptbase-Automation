from agency_swarm.tools import BaseTool
from pydantic import Field
from notion_client import Client
import os

class Detector(BaseTool):
    """
    This detector tool tells you if you should create a text or an image prompt.
    """

    previous_prompt_name: str = Field(
        ..., description="The name of the prompt in the email"
    )

    def run(self) -> str:
        promptdata = self.extract_prompt_data()

        if self.previous_prompt_name in promptdata:
            found_value = promptdata[self.previous_prompt_name]
            self._shared_state.set("PREVIOUSPROMPTNAME", self.previous_prompt_name)
            return f"Create a : {found_value}"+" Type prompt."
        else:
            keys_only = ", ".join(promptdata.keys())
            return f"Prompt name not found. Available prompt names: {keys_only}"

    def extract_prompt_data(self) -> dict:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        prompt_data = {}
        
        response = notion.databases.query(
            **{
                "database_id": os.getenv("PROMPT_CHECKER_DATABASE")
            }
        )
        
        for result in response.get('results', []):
            properties = result.get('properties', {})
            
            prompt_name = properties.get('Promptname', {}).get('title', [])
            if prompt_name:
                prompt_name = prompt_name[0].get('text', {}).get('content', '')

            prompt_type = properties.get('Prompttype', {}).get('rich_text', [])
            if prompt_type:
                prompt_type = prompt_type[0].get('text', {}).get('content', '')

            if prompt_name:
                prompt_data[prompt_name] = prompt_type

        return prompt_data