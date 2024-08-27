import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import requests
from agency_swarm.tools import BaseTool
import os
from notion_client import Client

class SendResults(BaseTool):
    """
    This tool sends all results to the user
    """

    def run(self) -> str:
        name: str = self._shared_state.get("Promptname")
        description: str = self._shared_state.get("Promptdescription")
        instruction: str = self._shared_state.get("Promptinstruction")
        prompt: str = self._shared_state.get("Prompt")
        inputs: list = self._shared_state.get("Promptexampleinputs", [])
        image_urls: list = self._shared_state.get("Images", [])

        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        email_user = os.getenv("EMAIL")
        email_password = os.getenv("PASSWORD")
        empfaenger_email = email_user

        message = MIMEMultipart()
        message["From"] = formataddr(("Prompter(Image)", email_user))
        message["To"] = empfaenger_email
        message["Subject"] = "New Image Prompt"

        email_content = f"""
        <h1>{name}</h1>
        <p><strong>Prompt Name:</strong> {name}</p>
        <p><strong>Description:</strong> {description}</p>
        <p><strong>Prompt:</strong> {prompt}</p>
        """

        for i, (input_example, url) in enumerate(zip(inputs, image_urls)):
            email_content += f"""
            <h2>Example Input {i + 1}</h2>
            <p>{input_example}</p>
            <img src="cid:image{i}">
            """

            response = requests.get(url)
            if response.status_code == 200:
                img_data = response.content
                img = MIMEImage(img_data)
                img.add_header('Content-ID', f'<image{i}>')
                img.add_header('Content-Disposition', 'inline', filename=f'image{i}.jpg')
                message.attach(img)

        email_content += f"""
        <h2>Instructions:</h2>
        <p>{instruction}</p>
        """

        html_part = MIMEText(email_content, "html")
        message.attach(html_part)

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, empfaenger_email, message.as_string())
        finally:
            server.quit()

        self.save_idea(idea=self._shared_state.get("PROMPTIDEA"))
        self.replace_prompt_name_in_notion(old_prompt_name=self._shared_state.get("PREVIOUSPROMPTNAME"), new_prompt_name=name)

        return "Sending was successful"
    
    def save_idea(self, idea: str) -> str:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        try:
            notion.pages.create(
                parent={"database_id": os.getenv("DATABASE_ID")},
                properties={
                    "Ideas": {
                        "title": [
                            {
                                "text": {
                                    "content": idea
                                }
                            }
                        ]
                    }
                }
            )
            return "New idea added successfully!"
        except Exception as e:
            return f"An error occurred while adding the new idea: {str(e)}"
        
    def replace_prompt_name_in_notion(self, old_prompt_name: str, new_prompt_name: str) -> None:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))

        response = notion.databases.query(
            **{
                "database_id": os.getenv("PROMPT_CHECKER_DATABASE"),
                "filter": {
                    "property": "Promptname",
                    "title": {
                        "contains": old_prompt_name
                    }
                }
            }
        )
        
        if not response['results']:
            print(f"Prompt name '{old_prompt_name}' not found in the database.")
            return
        
        page_id = response['results'][0]['id']
        
        notion.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    "Promptname": {
                        "title": [
                            {
                                "type": "text",
                                "text": {
                                    "content": new_prompt_name
                                }
                            }
                        ]
                    }
                }
            }
        )