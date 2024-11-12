---
page_type: sample
languages:
- azdeveloper
- bicep
products:
- azure
urlFragment: azureai-basic-python
name: Azure AI Basic template python
description: Creates an Azure AI Studio hub, project and required dependent resources including Azure OpenAI Service, Cognitive Search and more. Deploys a simple prompt application.
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/en-us/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Azure AI Studio Starter Template

### Quickstart

To learn how to install and get started with the Azure Developer CLI (azd) for deploying templates:
 - Follow the steps in [this quickstart](https://learn.microsoft.com/azure/developer/azure-developer-cli/get-started?tabs=localinstall&pivots=programming-language-nodejs) using this template(`Azure-Samples/azureai-basic-python`)

This quickstart will show you how to authenticate on Azure, initialize using a template, provision infrastructure and deploy code on Azure via the following commands:

```bash
# Log in to azd. Only required once per-install.
azd auth login

# First-time project setup. Initialize a project in the current directory, using this template.
azd init --template Azure-Samples/azureai-basic-python

# Provision and deploy to Azure
azd up

# Provision and deploy to Azure
azd deploy
```

### Creating a local Python environment

Create a python environment using your favorite package manager or python installation. We recommend to use venv to isolate python packages used between applications. 

```
cd src
```

To create a virtual evironment using venv:

On Windows:
```
py -3 -m venv .venv
.venv\scripts\activate
```

On Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

Install python packages:
```
pip install -r requirements.txt
```

### Local development

1. Run the local server:

    ```shell
    cd src
    python -m uvicorn api.main:app
    ```

2. Click 'http://127.0.0.1:8000' in the terminal, which should open a new tab in the browser.

3. Enter your prompt in the box.
### Provisioned Azure Resources

This template creates everything you need to get started with Azure AI Studio:

- [AI Hub Resource](https://learn.microsoft.com/azure/ai-studio/concepts/ai-resources)
- [AI Project](https://learn.microsoft.com/azure/ai-studio/how-to/create-projects)
- [OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Online Endpoint](https://learn.microsoft.com/azure/machine-learning/concept-endpoints-online?view=azureml-api-2)
- [AI Search Service](https://learn.microsoft.com/azure/search/) *(Optional, enabled by default)*

The provisioning will also deploy any models specified within the `./infra/ai.yaml`.

For a list of supported models see [Azure OpenAI Service Models documentation](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)

The template also includes dependent resources required by all AI Hub resources:

- [Storage Account](https://learn.microsoft.com/azure/storage/blobs/)
- [Key Vault](https://learn.microsoft.com/azure/key-vault/general/)
- [Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview) *(Optional, enabled by default)*
- [Container Registry](https://learn.microsoft.com/azure/container-registry/) *(Optional, enabled by default)*

### Optional Configuration

- To disable AI Search, run `azd config set USE_SEARCH_SERVICE false`
- To disable Application Insights, run `azd config set USE_APPLICATION_INSIGHTS false`
- To disable Container Registry, run `azd config set USE_CONTAINER_REGISTRY false`

By default this template will use a default naming convention to prevent naming collisions within Azure.
To override default naming conventions the following can be set.

- `AZUREAI_HUB_NAME` - The name of the AI Studio Hub resource
- `AZUREAI_PROJECT_NAME` - The name of the AI Studio Project
- `AZUREAI_ENDPOINT_NAME` - The name of the AI Studio online endpoint used for deployments
- `AZURE_OPENAI_NAME` - The name of the Azure OpenAI service
- `AZURE_SEARCH_SERVICE_NAME` - The name of the Azure Search service
- `AZURE_STORAGE_ACCOUNT_NAME` - The name of the Storage Account
- `AZURE_KEYVAULT_NAME` - The name of the Key Vault
- `AZURE_CONTAINER_REGISTRY_NAME` - The name of the container registry
- `AZURE_APPLICATION_INSIGHTS_NAME` - The name of the Application Insights instance
- `AZURE_LOG_ANALYTICS_WORKSPACE_NAME` - The name of the Log Analytics workspace used by Application Insights

Run `azd config set <key> <value>` after initializing the template to override the resource names

### Next Steps

Bring your code to the sample, configure the `azure.yaml` file and deploy to Azure using `azd deploy`!

## Try it out right away in GitHub Codespaces

You can use GitHub codespaces to open this repository in a pre-built VS Code development environment so that you can get started right away. 

Click the following to open this repository in GitHub codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azureai-basic-python?quickstart=1)

## Reporting Issues and Feedback

If you have any feature requests, issues, or areas for improvement, please [file an issue](https://aka.ms/azure-dev/issues). To keep up-to-date, ask questions, or share suggestions, join our [GitHub Discussions](https://aka.ms/azure-dev/discussions). You may also contact us via AzDevTeam@microsoft.com.
