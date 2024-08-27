# Promptbase-Automation

This repository automates the creation of image and text prompts, along with all necessary information required to upload them to the Promptbase platform. 

## Prerequisites

To get started, you will need:
- A Notion account
- An Outlook email account
- An OpenAI API key

## Setup Instructions

### 1. Create a Notion Integration

First, create a Notion integration by following the instructions [here](https://developers.notion.com/docs/create-a-notion-integration).

### 2. Set Up Notion Page and Databases

1. Go to Notion and create a page named `Image-Prompt-Ideas`. This page will store all prompt ideas that have already been used.
2. Within this page, create three full-page databases with the following names:
   - `PromptChecker`
   - `TextPromptIdeas`
   - `ImagePromptIdeas`

#### Database Structure

- **PromptChecker**: 
  - Columns: `Promptname` (Text), `Prompttype` (Text)
  
- **TextPromptIdeas** and **ImagePromptIdeas**:
  - Column: `Ideas` (Text)

### 3. Connect Databases to Integration

Ensure all databases are connected to your Notion integration.

### 4. Clone the Repository

Create a directory where you want to copy the repository and clone it:

```bash
git clone <repository_url>
cd <repository_directory>
```

### 5. Install Dependencies

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` File

Create a `.env` file in the root directory of the repository with the following structure:

```plaintext
OPENAI_API_KEY=""
NOTION_TOKEN=""
DATABASE_ID=""
TEXT_PROMPT_DATABASE_ID=""
PROMPT_CHECKER_DATABASE=""
EMAIL=""
PASSWORD=""
```

### 7. Populate the `.env` File

- **OPENAI_API_KEY**: Your OpenAI API key.
- **NOTION_TOKEN**: Your Notion integration API key.
- **DATABASE_ID**: The database ID from the `ImagePromptIdeas` URL.
- **TEXT_PROMPT_DATABASE_ID**: The database ID from the `TextPromptIdeas` URL.
- **PROMPT_CHECKER_DATABASE**: The database ID from the `PromptChecker` URL.
- **EMAIL**: Your Outlook email.
- **PASSWORD**: Your Outlook email password.

### 8. Run the Script

Run the `main.py` file:

```bash
python main.py
```

The script will prompt you with the following question:

```plaintext
Should I create an image or a text prompt? :
```

Simply answer the question, and the program will create a prompt with all required details, send it to you via email, and generate a small final message.