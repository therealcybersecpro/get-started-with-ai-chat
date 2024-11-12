# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
   This sample demonstrates how to get an authenticated AIProjectClient using the connection string
   and how to generate chat completions.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from urllib.parse import urlparse


from dotenv import load_dotenv
load_dotenv()


project_connection_string = urlparse(os.environ["AZUREAI_PROJECT_DISCOVERYURL"]).netloc +";"+os.environ["AZURE_SUBSCRIPTION_ID"]+";"+os.environ["AZURE_RESOURCE_GROUP"]+";"+os.environ["AZUREAI_PROJECT_NAME"]

#--Provide the model deployment name here. The model must also be listed in ai.yaml--#
model_deployment_name ="gpt-35-turbo-16k"

def generate_chat_stream(messages):
    body = {
        "model": model_deployment_name,
        "messages": messages,
        "stream": True
    }

    project_client = AIProjectClient.from_connection_string(credential=DefaultAzureCredential(),conn_str=project_connection_string)

    client = project_client.inference.get_chat_completions_client()
    
    completion = client.complete(model = model_deployment_name, messages=messages, stream=True)
    
    print(f"Completion: {completion}")
    
    return completion
 