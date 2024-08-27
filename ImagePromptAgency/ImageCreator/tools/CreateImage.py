from agency_swarm.tools import BaseTool
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import os
import re

class Selection(BaseModel):
    think_step_by_step: str
    desion: bool
    editedprompt: Optional[str]

class CreateImage(BaseTool):
    """
    This tool creates the images for the prompt
    """
    def run(self) -> str:
        checker = False
        prompt = self._shared_state.get("Prompt")
        prompt_input = self._shared_state.get("Promptexampleinputs")
        final_image_urls = []

        while not checker:
            final_prompt = self.create_final_prompt(main_prompt=prompt, variable_value=prompt_input[0])
            image = self.generate_image(prompt=final_prompt)
            
            checker, prompt_test = self.check_generated_image(image_url=image, prompt=prompt)
            if not checker:
                prompt = prompt_test

            final_image_urls.append(image)

        for input_prompt in prompt_input[1:]:
            final_prompt = self.create_final_prompt(main_prompt=prompt, variable_value=input_prompt)
            image = self.generate_image(prompt=final_prompt)
            final_image_urls.append(image)

        self._shared_state.set("Images", final_image_urls)
        self._shared_state.set("Prompt", prompt)

        return "Images for the prompt successfully created."
    
    def check_generated_image(self, image_url: str, prompt: str) -> bool:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Act as a prompt validator. You will get a 'image_prompt', a 'image_idea' and an image and your job is to check if the image aligns with what the image_idea wants to create. To do this think step by step if the visual elements are fitting and come up with a final decision. If you think the image does not fit the idea, then you need to edit the prompt, but always remain the [input value] the same, it is very important that in your new prompt, if you create one the input_value is the same and also always keep the []. Do not be too critical. Your output should be structured in the following way: First think about step by step if the prompt needs to be changed, second here you need to input True if you think the prompt does not need to be edited or False if you think the prompt needs to be edited. If you think the prompt needs to be edited (Your output is False not True), then you need to rewrite the prompt and remain the input field the same, if you think it does not need to be edited you can leave the field empty. Example you like the result of the prompt: step-by-step-thinking, True, Example you do not like the result of the prompt: step-by-step-thinking, False, new prompt with [input_value]"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "'image_idea': "+self._shared_state.get("PROMPTIDEA")+" 'image_prompt': "+prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            response_format=Selection,
        )

        output = completion.choices[0].message.parsed
        return output.desion, output.editedprompt
    
    def create_final_prompt(self, main_prompt: str, variable_value: str) -> str:
        return re.sub(r'\[.*?\]', f'[{variable_value}]', main_prompt)
    
    def generate_image(self, prompt: str) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url