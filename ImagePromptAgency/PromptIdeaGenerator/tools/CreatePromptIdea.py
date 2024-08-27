from agency_swarm.tools import BaseTool
from notion_client import Client
from openai import OpenAI
import os

class CreatePromptIdea(BaseTool):
    """
    Tool that creates the prompt ideas
    """

    def run(self):
        try:
            ideas = self.get_previous_prompt_ideas()
            newpromptidea = self.generate_new_prompt_idea(previous_ideas=ideas)
            self._shared_state.set("PROMPTIDEA", newpromptidea)
            return "The prompt idea was successfully created. This is the new promptidea: "+newpromptidea+" These are the previous prompt ideas: "+ideas
        except Exception as e:
            return f"There was an issue while the creation of the prompt idea, tell the ceo that he should report that to the user: {str(e)}"
        
    def generate_new_prompt_idea(self, previous_ideas: str) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Act as a expert in creating new unqiue prompt ideas. The user provides you with 'previous_promptideas' these are ideas already used. Your job is to create a new unique one and only output the idea noting else. Example Outputs: A prompt that generates beautifull landscapes, A prompt that creates highly detailed human faces, etc."},
                {"role": "user", "content": "'previous_promptideas': "+previous_ideas}
            ],
            temperature=1
        )
        return response.choices[0].message.content
    
    def get_previous_prompt_ideas(self) -> str:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        try:
            results = notion.databases.query(database_id=os.getenv("DATABASE_ID")).get('results', [])
            prompt_ideas = []

            for page in results:
                ideas_property = page['properties'].get('Ideas', {})
                
                if ideas_property and ideas_property['type'] == 'title':
                    title_texts = ideas_property.get('title', [])
                    if title_texts:
                        idea = "".join(text['text']['content'] for text in title_texts)
                        prompt_ideas.append(idea)
            return ", ".join(prompt_ideas)
        except Exception as e:
            return f"An error occurred while fetching data: {str(e)}"