"""
main.py
-------

This module provides the main entry point for the application that converts natural language prompts to API Endpoint Calls.

The application:
- Loads environment variables to retrieve the OpenAI API key.
- Initializes an instance of the language model specified.
- Continuously prompts the user to enter natural language text.
- Converts the provided text to an API command using the language model.
- Prints the converted API command to the console.

To terminate the loop and exit the application, the user can enter the text "exit".
"""

from dotenv import load_dotenv
from os import getenv
from llm import *

def main():
    """
    Main function to execute the application logic.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Retrieve the OpenAI API key from environment variables
    api_key = getenv('OPENAI_API_KEY')

    # Create an instance of LLMFactory using the provided API key
    factory = LLMFactory(api_key)

    # Specify the type and name of the language model to be used
    model_type = "chatopenai"
    model_name = "gpt-4-0613"

    # Create an instance of the language model using the factory
    llm_instance = factory.create_llm_instance(model_type=model_type, model_name=model_name)

    # Continuously prompt the user for text and convert it to API commands
    while True:
        text = input("Prompt: ")
        if text == "exit":
            break
        print(str(llm_instance.convert_text_to_command(text)) + '\n')

if __name__ == '__main__':
    main()