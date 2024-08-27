from agency_swarm.tools import BaseTool
from pydantic import Field
from openai import OpenAI
import os

class EditPromptIdea(BaseTool):
    """
    This tool edits prompt ideas based on feedback.
    """

    changes: str = Field(
        ..., description="Description of the changes to be made to the prompt idea."
    )

    def run(self) -> str:
        result = self.do_editing(feedback=self.changes)

        return result
    
    def do_editing(self, feedback: str) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will get 'feedback' from the user and your job is to adjust the prompt idea based on the whishes. Only output the edited promp nothing else."},
                {"role": "user", "content": "'feedback': "+feedback+" 'Promptidea': "+self._shared_state.get("PROMPTIDEA")}
            ]
        )
        return response.choices[0].message.content