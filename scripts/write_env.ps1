# Define the .env file path
$envFilePath = "src\.env"

# Clear the contents of the .env file
Set-Content -Path $envFilePath -Value ""

# Append new values to the .env file
$azureAiProjectConnectionString = azd env get-value AZURE_AIPROJECT_CONNECTION_STRING
$azureAiChatDeploymentName = azd env get-value AZURE_AI_CHAT_DEPLOYMENT_NAME
$azureTenantId = azd env get-value AZURE_TENANT_ID
$azureAIEmbedDeploymentName = azd env get-value AZURE_AI_EMBED_DEPLOYMENT_NAME
$azureAIEmbedDimensions = azd env get-value AZURE_AI_EMBED_DIMENSIONS
$azureAISearchIndexName = azd env get-value AZURE_AI_SEARCH_INDEX_NAME
$azureAISearchEndpoint = azd env get-value AZURE_AI_SEARCH_ENDPOINT
$serviceAPIUri = azd env get-value SERVICE_API_URI

Add-Content -Path $envFilePath -Value "AZURE_AIPROJECT_CONNECTION_STRING=$azureAiProjectConnectionString"
Add-Content -Path $envFilePath -Value "AZURE_AI_CHAT_DEPLOYMENT_NAME=$azureAiChatDeploymentName"
Add-Content -Path $envFilePath -Value "AZURE_TENANT_ID=$azureTenantId"
Add-Content -Path $envFilePath -Value "AZURE_AI_EMBED_DEPLOYMENT_NAME=$azureAIEmbedDeploymentName"
Add-Content -Path $envFilePath -Value "AZURE_AI_EMBED_DIMENSIONS=$azureAIEmbedDimensions"
Add-Content -Path $envFilePath -Value "AZURE_AI_SEARCH_INDEX_NAME=$azureAISearchIndexName"
Add-Content -Path $envFilePath -Value "AZURE_AI_SEARCH_ENDPOINT=$azureAISearchEndpoint"

Write-Host "Web app URL:"
Write-Host $serviceAPIUri -ForegroundColor Cyan