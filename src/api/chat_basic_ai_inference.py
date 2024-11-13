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

# initialize a project and chat client
project = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ['AZURE_AIPROJECT_CONNECTION_STRING'])

chat = project.inference.get_chat_completions_client()

# The model deployment name to use. The model must also be listed in ai.yaml.
model_deployment_name ="gpt-4o-mini"

SYSTEM_PROMPT = "You are a helpful assistant."

def generate_chat_stream(messages):
    system_message = [{"role": "system", "content": SYSTEM_PROMPT}]
    completion = chat.complete(
        model="gpt-4o-mini",
        messages=system_message + messages, 
        stream=True)
    
    return completion
 