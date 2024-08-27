from agency_swarm.tools import BaseTool
from openai import OpenAI
from pydantic import BaseModel
import os

class PromptDetails(BaseModel):
    think_step_by_step: str
    promptname: str
    promptdescription: str
    promptinstruction: str
    prompt: str
    example_input: list[str]

class CreatePromptDetails(BaseTool):
    """
    This tool creates the details for prompt ideas
    """
    def run(self) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        promptidea = self._shared_state.get("PROMPTIDEA")
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": """
                 Create a prompt and details based on the 'promptidea' user will provide you. To do this correctly you have 'examples'. Always create prompts with just one input[] and always create 9 exampleinputs not more not less. 'examples': 
                 promptidea=A prompt that creates anime-inspired characters based on user preferences.

                result=

                Promptname: Animetouch

                Promptdescription: 🌟 Bring your ideal character to life with Animetouch! 🌟 Whether you're envisioning a heroic warrior, a mysterious mage, or a lively schoolgirl, our prompt helps you create anime characters with detailed features, expressive emotions, and a unique style. ✨ Dive into the world of anime with characters that reflect your imagination! 🎨 #AnimeArt #CharacterDesign

                Promptinstruction: Add the character's personality, appearance, and any special abilities or traits you want them to have.

                Prompt: A vividly detailed anime character design based on [character's personality and appearance]. The character's features reflect the essence of anime, with large expressive eyes, dynamic poses, and intricate costumes. Their personality shines through their design—whether they're a determined warrior, a playful trickster, or a calm intellectual. If the character has special abilities or traits, these are visually represented through unique elements such as glowing weapons, ethereal auras, or dramatic outfits. The background complements the character, enhancing the overall mood and setting.

                Exampleinputs: [fiery warrior with red hair and a blazing sword, shy schoolgirl with pastel colors and a soft expression, mysterious sorcerer with dark robes and glowing runes, cheerful idol with bright colors and a microphone, brave samurai with traditional armor and a calm demeanor]

                promptidea=A prompt that creates fantasy landscapes based on user preferences.

                result=

                Promptname: Fantascapes

                Promptdescription: 🌌 Step into a world of fantasy! 🌌 Fantascapes brings your dream worlds to life with breathtaking scenery and mythical elements. From enchanted forests to floating islands, each landscape is crafted with rich details and a touch of magic. 🌲🏰✨ Discover the beauty and mystery of your own fantastical realm! 🦄 #FantasyWorlds #ImaginaryLandscapes

                Promptinstruction: Add the type of landscape you want, along with any specific elements like creatures or structures.

                Prompt: A richly detailed fantasy landscape based on [landscape type]. The scene captures the essence of a magical world, filled with vibrant colors, mystical creatures, and awe-inspiring structures. The environment is designed with a blend of natural beauty and supernatural elements, whether it's towering crystal formations, ancient ruins, or floating castles. The atmosphere is immersive, pulling the viewer into a realm where anything is possible, from peaceful meadows with glowing flowers to dark forests shrouded in mist. The lighting and composition enhance the mood, whether it's a serene sunset or an ominous stormy sky.

                Exampleinputs: [crystal caverns with glowing stalactites, floating islands with cascading waterfalls, enchanted forest with luminescent creatures, ancient ruins covered in vines, mystical desert with shifting sands, icy tundra with towering glaciers]

                promptidea=A prompt that creates steampunk gadgets and inventions based on user preferences.

                result=

                Promptname: Steamcraft

                Promptdescription: ⚙️ Step into the world of steampunk! ⚙️ Steamcraft brings your mechanical dreams to life, crafting intricate gadgets and inventions straight out of a Victorian-inspired future. From clockwork automatons to steam-powered vehicles, each creation is a blend of old-world charm and futuristic innovation. 🔩 Let your imagination gear up with creations that are as functional as they are stylish! 🛠️ #Steampunk #InventorsDream

                Promptinstruction: Add the type of gadget or invention you want, along with any specific features or functions.

                Prompt: A detailed design of a steampunk [gadget or invention], capturing the essence of Victorian aesthetics merged with advanced technology. The creation features intricate gears, brass fittings, and steam-powered mechanisms, all designed with both functionality and style in mind. The gadget or invention includes [specific features or functions], which are creatively integrated into the design, whether it's a portable timepiece with hidden compartments, a steam-powered airship with rotating propellers, or an automaton with articulated limbs and glowing eyes. The overall composition reflects the ingenuity and craftsmanship typical of steampunk creations, with an emphasis on both form and function.

                Exampleinputs: [clockwork pocket watch with hidden tools, steam-powered bicycle with reinforced frame, mechanical owl with rotating head, brass gauntlet with retractable blades, steam-powered prosthetic arm with interchangeable attachments]
                 """},
                {"role": "user", "content": "'promptidea': "+promptidea},
            ],
            response_format=PromptDetails,
            temperature=1
        )
        promptdetails = completion.choices[0].message.parsed
        self._shared_state.set("Promptname", promptdetails.promptname)
        self._shared_state.set("Promptdescription", promptdetails.promptdescription)
        self._shared_state.set("Promptinstruction", promptdetails.promptinstruction)
        self._shared_state.set("Prompt", promptdetails.prompt)
        self._shared_state.set("Promptexampleinputs", promptdetails.example_input)

        return "Every promptdetail was successfully created report that back to the ceo"