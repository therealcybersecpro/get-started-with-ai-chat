from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

#project_connection_string ="eastus.api.azureml.ms;ca26d469-a43d-4f1d-adcd-28662e586808;rg-jagatjit-8392_ai;jagatjit-5577"
#project_connection_string ="francecentral.api.azureml.ms;f93b65a5-0bac-4e59-b286-140e2dae416d;rg-contosodev;jturuk-3055"
#project_connection_string = "northcentralus.api.azureml.ms;f93b65a5-0bac-4e59-b286-140e2dae416d;rg-azure-basic-python;ai-project-fj4t2lv3dee7c"
#project_connection_string="northcentralus.api.azureml.ms;f93b65a5-0bac-4e59-b286-140e2dae416d;rg-jturuk-8571_ai;jturuk-5739"
model_deployment_name ="gpt-35-turbo-16k"

from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import UserMessage

import os
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()

print(os.environ)

project_connection_string = urlparse(os.environ["AZUREAI_PROJECT_DISCOVERYURL"]).netloc +";"+os.environ["AZURE_SUBSCRIPTION_ID"]+";"+os.environ["AZURE_RESOURCE_GROUP"]+";"+os.environ["AZUREAI_PROJECT_NAME"]

project_client = AIProjectClient.from_connection_string(credential=DefaultAzureCredential(),conn_str=project_connection_string)


client = project_client.inference.get_chat_completions_client()

response = client.complete(
    model=model_deployment_name,
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "What is the capital of India"},
    ]
)

print(response.choices[0].message.content)