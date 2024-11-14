# Define the .env file path
$envFilePath = "src\.env"

# Clear the contents of the .env file
Set-Content -Path $envFilePath -Value ""

# Append new values to the .env file
$azureAiProjectConnectionString = azd env get-value AZURE_AIPROJECT_CONNECTION_STRING

Add-Content -Path $envFilePath -Value "AZURE_AIPROJECT_CONNECTION_STRING=$azureAiProjectConnectionString"