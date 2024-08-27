from agency_swarm import Agency

from ImagePromptAgency.PromptCEOSelector.PromptCEOSelector import PromptCEOSelector

from ImagePromptAgency.PromptIdeaGenerator.PromptIdeaGenerator import PromptIdeaGenerator
from ImagePromptAgency.ImagePromptCEO.ImagePromptCEO import ImagePromptCEO
from ImagePromptAgency.PromptDetailsGenerator.PromptDetailsGenerator import PromptDetailsGenerator
from ImagePromptAgency.ImageCreator.ImageCreator import ImageCreator
from ImagePromptAgency.PromptSender.PromptSender import PromptSender

from ImagePromptAgency.TextPromptCEO.TextPromptCEO import TextPromptCEO
from ImagePromptAgency.TextPromptIdeaGenerator.TextPromptIdeaGenerator import TextPromptIdeaGenerator
from ImagePromptAgency.TextPromptDetailsGenerator.TextPromptDetailsGenerator import TextPromptDetailsGenerator
from ImagePromptAgency.TextPromptSender.TextPromptSender import TextPromptSender

from agency_swarm import set_openai_key
import os
from dotenv import load_dotenv

def run_promptbase_agency(prompt: str) -> str:
    load_dotenv()
    set_openai_key(os.getenv("OPENAI_API_KEY"))

    ceo = PromptCEOSelector()

    textceo = TextPromptCEO()
    tepridgen = TextPromptIdeaGenerator()
    teprdegen = TextPromptDetailsGenerator()
    teprse = TextPromptSender()

    imgceo = ImagePromptCEO()
    pridgen = PromptIdeaGenerator()
    prdegen = PromptDetailsGenerator()
    Imgen = ImageCreator()
    PrSe = PromptSender()

    agency = Agency(
                    [ceo,
                    [ceo, imgceo],
                    [ceo, textceo],
                    [textceo, tepridgen],
                    [textceo, teprdegen],
                    [textceo, teprse],
                    [imgceo, pridgen],
                    [imgceo, prdegen],
                    [imgceo, Imgen],
                    [imgceo, PrSe]
                    ],
                    shared_instructions='./agency_manifesto.md',
                    temperature=0.3
                    )
    
    return agency.get_completion(message=prompt)