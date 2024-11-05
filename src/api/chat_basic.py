#AzureAIClient is deprecated. AIProjectClient is to be used. Ignore this file.

import os
from azure.ai.client import AzureAIClient
from azure.identity import DefaultAzureCredential


from dotenv import load_dotenv
load_dotenv()

client = AzureAIClient.from_connection_string(
    conn_str = os.environ["PROJECT_CONNECTION_STRING"],
    credential = DefaultAzureCredential()
)

chat = client.inference.get_chat_completions_client()
response = chat.complete(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    messages =[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"     
        }
    ]
)

print(response.messages[-1].content)
