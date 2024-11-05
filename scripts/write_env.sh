#!/bin/bash

# Define the .env file path
ENV_FILE_PATH="src/.env"

# Clear the contents of the .env file
> $ENV_FILE_PATH

echo "AZUREAI_PROJECT_DISCOVERYURL=$(azd env get-value AZUREAI_PROJECT_DISCOVERYURL)" >> $ENV_FILE_PATH
echo "AZURE_SUBSCRIPTION_ID=$(azd env get-value AZURE_SUBSCRIPTION_ID)" >> $ENV_FILE_PATH
echo "AZURE_RESOURCE_GROUP=$(azd env get-value AZURE_RESOURCE_GROUP)" >> $ENV_FILE_PATH
echo "AZUREAI_PROJECT_NAME=$(azd env get-value AZUREAI_PROJECT_NAME)" >> $ENV_FILE_PATH
