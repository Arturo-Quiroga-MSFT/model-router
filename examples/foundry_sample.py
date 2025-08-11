import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

endpoint = os.getenv("azure_openai_endpoint")
model = "model-router"

print(f"Using Azure OpenAI endpoint: {endpoint}")

# Initialize Azure OpenAI client with Entra ID authentication
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-01-01-preview",
)

def modelrouter(prompt):
    """
    Generates a response from the chat model based on the provided prompt.

    Args:
        prompt (str): The user's input to which the chat model will respond.

    Returns:
        response: The complete response object from the chat model, including the generated message and model details.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
        )
        print()
        print("\033[1;31;34m")
        print(response.choices[0].message.content)
        print("\033[1;31;32m")
        print()
        print(f"This model was automatically selected: {response.model}")
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

prompt = "What is FIFA?"

modelrouter(prompt)