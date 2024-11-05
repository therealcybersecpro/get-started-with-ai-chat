# Define the .env file path
$envFilePath = "src\.env"

# Clear the contents of the .env file
Set-Content -Path $envFilePath -Value ""

# Append new values to the .env file
$azureProjectDiscoveryUrl = azd env get-value AZUREAI_PROJECT_DISCOVERYURL
$azureSubscriptionId = azd env get-value AZURE_SUBSCRIPTION_ID
$azureResourceGroup = azd env get-value AZURE_RESOURCE_GROUP
$azureProjectName = azd env get-value AZUREAI_PROJECT_NAME

Add-Content -Path $envFilePath -Value "AZUREAI_PROJECT_DISCOVERYURL=$azureProjectDiscoveryUrl"
Add-Content -Path $envFilePath -Value "AZURE_SUBSCRIPTION_ID=$azureSubscriptionId"
Add-Content -Path $envFilePath -Value "AZURE_RESOURCE_GROUP=$azureResourceGroup"
Add-Content -Path $envFilePath -Value "AZUREAI_PROJECT_NAME=$azureProjectName"
