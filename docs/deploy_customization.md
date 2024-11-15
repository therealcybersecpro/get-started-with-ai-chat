
# Azure AI Studio Starter Template: Deployment customization

This document describes how to customize the deployment of the Azure AI Studio Starter Template. Once you follow the steps here, you can run `azd up` as described in the [Deploying](./README.md#deploying) steps.

* [Disabling resources](#disabling-resources)
* [Customizing resource names](#customizing-resource-names)
* [Customizing OpenAI deployments](#customizing-openai-deployments)

## Disabling resources

* To disable AI Search, run `azd env set USE_SEARCH_SERVICE false`
* To disable Application Insights, run `azd env set USE_APPLICATION_INSIGHTS false`
* To disable Container Registry, run `azd env set USE_CONTAINER_REGISTRY false`

Then run `azd up` to deploy the remaining resources.

## Customizing resource names

By default this template will use a default naming convention to prevent naming collisions within Azure.
To override default naming conventions the following can be set.

* `AZURE_AIHUB_NAME` - The name of the AI Studio Hub resource
* `AZURE_AIPROJECT_NAME` - The name of the AI Studio Project
* `AZURE_AIENDPOINT_NAME` - The name of the AI Studio online endpoint used for deployments
* `AZURE_AISERVICES_NAME` - The name of the Azure OpenAI service
* `AZURE_SEARCH_SERVICE_NAME` - The name of the Azure Search service
* `AZURE_STORAGE_ACCOUNT_NAME` - The name of the Storage Account
* `AZURE_KEYVAULT_NAME` - The name of the Key Vault
* `AZURE_CONTAINER_REGISTRY_NAME` - The name of the container registry
* `AZURE_APPLICATION_INSIGHTS_NAME` - The name of the Application Insights instance
* `AZURE_LOG_ANALYTICS_WORKSPACE_NAME` - The name of the Log Analytics workspace used by Application Insights

To override any of those resource names, run `azd env set <key> <value>` before running `azd up`.

## Customizing OpenAI deployments

To customize the OpenAI deployment, you can set the following environment variables:

### Using a different chat model

Change the chat deployment name:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_NAME Phi-3.5-MoE-instruct
```

Change the chat model format: (OpenAI, Microsoft)

```shell
azd env set AZURE_AI_CHAT_MODEL_FORMAT Microsoft
```

Change the chat model name:

```shell
azd env set AZURE_AI_CHAT_MODEL_NAME Phi-3.5-MoE-instruct
```

Set the version of the chat model:

```shell
azd env set AZURE_AI_CHAT_MODEL_VERSION 2
```

### Setting capacity and deployment SKU

For quota regions, you may find yourself needing to modify the default capacity and deployment SKU.

Change the capacity of the chat deployment:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_CAPACITY 10
```

Change the SKU of the chat deployment:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_SKU Standard
```

Change the capacity of the embeddings deployment:

```shell
azd env set AZURE_AI_EMBED_DEPLOYMENT_CAPACITY 10
```

Change the SKU of the embeddings deployment:

```shell
azd env set AZURE_AI_EMBED_DEPLOYMENT_SKU Standard
```