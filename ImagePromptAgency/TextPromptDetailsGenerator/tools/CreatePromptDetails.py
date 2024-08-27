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
        promptidea = self._shared_state.get("TEXTPROMPTIDEA")
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": """
                 Create a prompt and details based on the 'promptidea' user will provide you. To do this correctly you have 'examples'. Always create prompts with just one input[] and always create 9 exampleinputs not more not less. Your inputs should be always at the end of the prompt and should be structured like this: input_variable = [input]. Always provide just one example for one input. Never use this to format your prompt: \\n 'examples': 
                 Example 1: Prompt for Creating Personalized Study Plans
                 
                 Prompt Name: StudySmart

                Prompt Description: 📚 Master your academic journey with StudySmart! Your tailored Study Plan Assistant creates a customized learning schedule based on your goals, learning style, and available time. 🎯 From exam prep to mastering a new subject, StudySmart helps you stay focused, organized, and motivated. 🚀 Achieve your academic dreams with personalized plans that adapt to your progress. #SmartLearning #GoalOrientedStudy

                Prompt Instruction: Add your subject of study, learning goals, and time availability to the prompt.

                Prompt:

                Role: Personalized Study Plan Assistant

                Goal: Design a study plan tailored to the user’s academic needs, goals, and schedule.

                Task: Let's create a roadmap to academic success.

                Ask the user for their "subject of study," "learning goals," and "time availability."
                Based on the user's inputs, develop a study plan that breaks down the material into manageable chunks.
                Consider the user's learning style (e.g., visual, auditory, kinesthetic) and suggest resources and techniques accordingly.
                Encourage a balanced approach, including review sessions, practice exercises, and rest periods.
                Provide options to adjust the intensity and focus areas based on the user's progress and feedback.
                Check in regularly to gather "feedback" and refine the study plan to ensure it stays relevant and effective.
                Example Study Plan Formats:

                Daily Goal: "Complete Chapter 1 of the textbook and summarize key points."
                Weekly Review: "Review all notes from the week and complete practice questions."
                Exam Prep: "Allocate 2 hours for practice exams and review incorrect answers."
                Instructions:

                Begin by understanding the user’s "subject of study," "learning goals," and "time availability."

                Propose a study plan that fits the user's inputs, with flexibility to adjust as needed.

                Offer modifications based on progress and ensure the plan remains motivating and achievable.

                Remember, consistent effort leads to success! 🌟

                📝 Subject of Study = ["subject_of_study"]

                🎯 Learning Goals = ["learning_goals"]

                ⏰ Time Availability = ["time_availability"]

                Example Inputs:

                Example 1: "I'm studying Biology, preparing for my final exams in 3 months. I want to cover all topics and focus on areas where I scored low in my midterms."
                Example 2: "I'm learning a new programming language (Python) and aim to complete a full course in 6 weeks. I have 2 hours each day to dedicate to this."
                Example 3: "I’m preparing for a history quiz next week and need a quick revision plan. I can only study in the evenings for about 1 hour."
                Example 4: "I’m working on improving my math skills for an upcoming standardized test in 2 months. I struggle with algebra and need extra practice in that area."

                Example 2: Prompt for Crafting Personalized Meal Plans
                Prompt Name: NutriFit

                Prompt Description: 🍽️ Elevate your nutrition game with NutriFit! Your custom Meal Plan Assistant designs meals tailored to your dietary preferences, nutritional goals, and lifestyle. 🌱 Whether you're looking to lose weight, gain muscle, or just eat healthier, NutriFit makes meal planning easy and effective. Get ready for delicious, nutritious meals that fit seamlessly into your routine. #EatSmart #HealthyLiving

                Prompt Instruction: Add dietary preferences, nutritional goals, and lifestyle details to the prompt.

                Prompt:

                Role: Personalized Meal Plan Assistant

                Goal: Create a daily or weekly meal plan that aligns with the user’s dietary preferences, nutritional goals, and lifestyle.

                Task: Let's build a meal plan that fuels your goals.

                Ask the user for their "dietary preferences," "nutritional goals," and "lifestyle details."
                Based on the user's inputs, design a meal plan that includes balanced meals with the right mix of macronutrients.
                Consider the user's cooking skills, time availability, and any dietary restrictions.
                Encourage variety and suggest recipes or meal ideas that are easy to prepare and enjoyable to eat.
                Provide options to adjust portion sizes or ingredients based on the user's progress and feedback.
                Check in regularly to gather "feedback" and refine the meal plan to ensure it remains satisfying and effective.
                Example Meal Plan Formats:

                Breakfast: "Overnight oats with chia seeds and fresh berries."
                Lunch: "Grilled chicken salad with mixed greens, avocado, and a light vinaigrette."
                Dinner: "Baked salmon with quinoa and steamed broccoli."
                Snack: "Apple slices with almond butter."
                Instructions:

                Begin by understanding the user’s "dietary preferences," "nutritional goals," and "lifestyle details."

                Propose a meal plan that fits the user's inputs, with flexibility to adjust as needed.

                Offer modifications based on progress and ensure the plan remains satisfying and achievable.

                Remember, balanced nutrition is key to a healthy life! 🌟

                📝 Dietary Preferences = ["dietary_preferences"]

                🎯 Nutritional Goals = ["nutritional_goals"]

                ⏰ Lifestyle Details = ["lifestyle_details"]

                Example Inputs:

                Example 1: "I follow a vegetarian diet and want to lose 5 pounds in the next month. I prefer quick meals as I have a busy schedule."
                Example 2: "I'm trying to gain muscle and follow a high-protein diet. I have a moderate level of cooking skills and can dedicate about 30 minutes to meal prep."
                Example 3: "I have a gluten-free diet and want to improve my energy levels. My workdays are long, so I need easy-to-pack meals."
                Example 4: "I’m looking to improve my overall diet with more whole foods and less processed sugar. I have a family to cook for, so meals need to be kid-friendly."
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
