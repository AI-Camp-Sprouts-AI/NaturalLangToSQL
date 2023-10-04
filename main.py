from dotenv import load_dotenv
from os import getenv
from llm import *

if __name__ == '__main__':
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    factory = LLMFactory(api_key)

    # model_type = input("Model Type: ").lower().strip()
    # model_name = input("Model Name: ").lower().strip()
    model_type = "chatopenai"
    model_name = "gpt-4-0613"
    llm_instance = factory.create_llm_instance(model_type=model_type, model_name=model_name)

    while True:
        text = input("Prompt: ")
        if text == "exit":
            break
        print(llm_instance.convert_text_to_command(text) + '\n')