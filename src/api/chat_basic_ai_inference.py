# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    Given an AIProjectClient, this sample demonstrates how to get an authenticated 
    async ChatCompletionsClient from the azure.ai.inference package. For more information
    on the azure.ai.inference package see https://pypi.org/project/azure-ai-inference/.

USAGE:
    python sample_get_chat_completions_client.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    * PROJECT_CONNECTION_STRING - The Azure AI Project connection string, as found in your AI Studio Project.
    * MODEL_DEPLOYMENT_NAME - The model deployment name, as found in your AI Studio Project.
"""

import os
from typing import Any, Mapping, Optional, overload
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import UserMessage, ChatRequestMessage, ChatResponseMessage
from azure.identity import DefaultAzureCredential
import fastapi
from urllib.parse import urlparse


from dotenv import load_dotenv
load_dotenv()

print(os.environ)

#project_connection_string ="northcentralus.api.azureml.ms;f93b65a5-0bac-4e59-b286-140e2dae416d;rg-jturuk-8571_ai;jturuk-5739"
#project_connection_string = "northcentralus.api.azureml.ms;f93b65a5-0bac-4e59-b286-140e2dae416d;rg-azureai-basic-python;ai-project-iyjj47eku46ow"
project_connection_string = "eastus2.api.azureml.ms;597966d1-829f-417e-9950-8189061ec09c;rg-dantaylo-e2e-demo2;dantaylo-e2e-demo2"
model_deployment_name ="gpt-4o-mini"

print(project_connection_string)



def generate_chat(input):
    print("input 2 "+input)
    project_client = AIProjectClient.from_connection_string(credential=DefaultAzureCredential(),conn_str=project_connection_string)

    client = project_client.inference.get_chat_completions_client()

    response = client.complete(
        model=model_deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
            {"role": "user", "content": "What is the capital of India"},
    ]
    )
    return response.choices[0].message.content

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
 