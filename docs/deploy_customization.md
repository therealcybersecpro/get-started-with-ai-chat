
# Azure AI Studio Starter Template: Deployment customization

This document describes how to customize the deployment of the Azure AI Studio Starter Template. Once you follow the steps here, you can run `azd up` as described in the [Deploying](./README.md#deploying) steps.

## Disabling resources

* To disable AI Search, run `azd env set USE_SEARCH_SERVICE false`
* To disable Application Insights, run `azd env set USE_APPLICATION_INSIGHTS false`
* To disable Container Registry, run `azd env set USE_CONTAINER_REGISTRY false`

Then run `azd up` to deploy the remaining resources.

## Customizing resource names

By default this template will use a default naming convention to prevent naming collisions within Azure.
To override default naming conventions the following can be set.

* `AZUREAI_HUB_NAME` - The name of the AI Studio Hub resource
* `AZUREAI_PROJECT_NAME` - The name of the AI Studio Project
* `AZUREAI_ENDPOINT_NAME` - The name of the AI Studio online endpoint used for deployments
* `AZURE_AISERVICE_NAME` - The name of the Azure OpenAI service
* `AZURE_SEARCH_SERVICE_NAME` - The name of the Azure Search service
* `AZURE_STORAGE_ACCOUNT_NAME` - The name of the Storage Account
* `AZURE_KEYVAULT_NAME` - The name of the Key Vault
* `AZURE_CONTAINER_REGISTRY_NAME` - The name of the container registry
* `AZURE_APPLICATION_INSIGHTS_NAME` - The name of the Application Insights instance
* `AZURE_LOG_ANALYTICS_WORKSPACE_NAME` - The name of the Log Analytics workspace used by Application Insights

To override any of those resource names, run `azd env set <key> <value>` before running `azd up`.
