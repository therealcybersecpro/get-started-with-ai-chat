---
page_type: sample
languages:
- azdeveloper
- bicep
- python
products:
- azure
- azure-openai
- azure-ai
- azure-cognitive-search
- azure-container-apps
urlFragment: azureai-basic-python
name: Azure AI basic template (Python)
description: Creates an Azure AI Foundry hub, project and required dependent resources including Azure AI Services, Azure AI Search and more. Deploys a simple chat application.
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/en-us/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Azure AI Foundry Starter Template

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azureai-basic-python)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/azureai-basic-python)

This project creates an Azure AI Foundry hub, project and connected resources including Azure AI Services, AI Search and more. It also deploys a simple chat application to Azure Container Apps.
The main path walks you through deploying the application using local development environment. After the local development environment instructions, there are also instructions for developing in GitHub Codespaces and VS Code Dev Containers.

* [Prerequisites](#prerequisites)
  * [Azure account](#azure-account)
  * [Required tools](#required-tools)
  * [Bringing an existing AI project resource](#bringing-an-existing-ai-project-resource)
* [Development](#development)
  * [Code](#code)
  * [Logging](#logging)
  * [Tracing to App Insights](#tracing-to-app-insights)
* [Deployment](#deployment)
* [Tracing and Monitoring](#tracing-and-monitoring)
* [Development server](#development-server)
* [Alternatives to Local Development](#alternatives-to-local-development)
  * [GitHub Codespaces](#github-codespaces)
  * [VS Code Dev Containers](#vs-code-dev-containers)
* [Supporting Documentation](#supporting-documentation)
  * [Costs](#costs)
  * [Security guidelines](#security-guidelines)
  * [Resources](#resources)


## Prerequisites

#### Azure account
If you do not have an Azure Subscription, you can set one up following these instructions:

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/) and create an Azure Subscription.
2. Check that you have the necessary permissions:
    * Your Azure account must have `Microsoft.Authorization/roleAssignments/write` permissions, such as [Role Based Access Control Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview), [User Access Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#user-access-administrator), or [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner).
    * Your Azure account also needs `Microsoft.Resources/deployments/write` permissions on the subscription level.

#### Required tools
Make sure the following tools are installed:

1. [Azure Developer CLI (azd)](https://aka.ms/install-azd) If you have the Azure Developer CLI already installed, you can update to latest version using:
    ```shell
    winget upgrade microsoft.azd
    ```
2. [Python 3.9+](https://www.python.org/downloads/)
3. [Git](https://git-scm.com/downloads)

#### Bringing an existing AI project resource

This step applies if you have an existing AI project resource, and you want to bring it into the Azure AI Foundry Starter Template by setting the following environment variable:

```shell
azd env set AZURE_EXISTING_AIPROJECT_CONNECTION_STRING "<connection-string>"
```

You can find the connection string on the overview page of your Azure AI project.

If you do not have a deployment named "gpt-4o-mini" in your existing AI project, you should either create one in Azure AI Foundry or follow the steps in [Customizing model deployments](#customizing-model-deployments) to specify a different model.

## Development

#### Code
Download the project code:

```shell
azd init -t azureai-basic-python
```
At this point you could make changes to the code if required. However, no changes are needed to deploy and test the app as shown in the next step.

#### Logging
If you want to enable logging to file instead of console, make the following modifications to main.py:

```code
TBA
```

#### Tracing to App Insights
To enable tracing to App Insights, modify the value of ENABLE_AZURE_MONITOR_TRACING environment variable to true in Dockerfile found in src directory:
```code
ENV ENABLE_AZURE_MONITOR_TRACING=true
```
Note that the optinal App Insights resource is required for tracing (it is created by default).

To enable message contents to be included in the traces, set the following environment variable to true in the same Dockerfile. Note that the messages may contain personally identifiable information.

```code
ENV AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true
```

## Deployment

1. Login to Azure:

    ```shell
    azd auth login
    ```

2. (Optional) If you would like to customize the deployment to [disable resources](docs/deploy_customization.md#disabling-resources), [customize resource names](docs/deploy_customization.md#customizing-resource-names),
or [customize the models](docs/deploy_customization.md#customizing-model-deployments), you can follow those steps now.

3. Provision and deploy all the resources:

    ```shell
    azd up
    ```

    It will prompt you to provide an `azd` environment name (like "azureaiapp"), select a subscription from your Azure account, and select a location which has quota for all the resources. Then it will provision the resources in your account and deploy the latest code. If you get an error or timeout with deployment, changing the location can help, as there may be availability constraints for the resources.

4. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI, and you should see the app! 🎉

5. If you make further modification to the app code, you can deploy the updated version with:

    ```shell
    azd deploy
    ```

## Tracing and Monitoring

You can view console logs here: TBA
Choose the app option to view the logs from the app. You can also switch between historical and real-time views on the UI.

If you enabled logging to file, you can view the log file by... TBA

You can view the App Insights tracing here: TBA

## Development server

You can optionally use a development server to test app changes locally. Make sure you first [deployed the app](#deploying) to Azure before running the development server.

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

    On Windows:

    ```shell
    py -3 -m venv .venv
    .venv\scripts\activate
    ```

    On Linux:

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Navigate to the `src` directory:

    ```shell
    cd src
    ```

3. Install required Python packages:

    ```shell
    python -m pip install -r requirements.txt
    ```

4. Run the local server:

    ```shell
    python -m uvicorn "api.main:create_app" --factory --reload
    ```

5. Click 'http://127.0.0.1:8000' in the terminal, which should open a new tab in the browser.

6. Enter your message in the box.

## Alternatives to Local Development Environment

#### GitHub Codespaces

You can run this template virtually by using GitHub Codespaces. The button will open a web-based VS Code instance in your browser:

1. Open the template (this may take several minutes):

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azureai-basic-python)

2. Open a terminal window
3. Continue with the [deploying steps](#deployment)

#### VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed [Docker Desktop](https://www.docker.com/products/docker-desktop/))
2. Open the project:

    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/azureai-basic-python)

3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.
4. Continue with the [deploying steps](#deployment)


## Supporting Documentation

#### Costs

Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.
The majority of the Azure resources used in this infrastructure are on usage-based pricing tiers.
However, Azure Container Registry has a fixed cost per registry per day.

You can try the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator) for the resources:

* Azure AI Foundry: Free tier. [Pricing](https://azure.microsoft.com/pricing/details/ai-studio/)
* Azure AI Search: Standard tier, S1. Pricing is based on the number of documents and operations. [Pricing](https://azure.microsoft.com/pricing/details/search/)
* Azure Storage Account: Standard tier, LRS. Pricing is based on storage and operations. [Pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)
* Azure Key Vault: Standard tier. Pricing is based on the number of operations. [Pricing](https://azure.microsoft.com/pricing/details/key-vault/)
* Azure AI Services: S0 tier, defaults to gpt-4o-mini and text-embedding-ada-002 models. Pricing is based on token count. [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)
* Azure Container App: Consumption tier with 0.5 CPU, 1GiB memory/storage. Pricing is based on resource allocation, and each month allows for a certain amount of free usage. [Pricing](https://azure.microsoft.com/pricing/details/container-apps/)
* Azure Container Registry: Basic tier. [Pricing](https://azure.microsoft.com/pricing/details/container-registry/)
* Log analytics: Pay-as-you-go tier. Costs based on data ingested. [Pricing](https://azure.microsoft.com/pricing/details/monitor/)

⚠️ To avoid unnecessary costs, remember to take down your app if it's no longer in use,
either by deleting the resource group in the Portal or running `azd down`.

#### Security guidelines

This template uses Azure AI Foundry connections to communicate between resources, which stores keys in Azure Key Vault.
This template also uses [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for local development and deployment.

To ensure continued best practices in your own repository, we recommend that anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled.

You may want to consider additional security measures, such as:

* Enabling Microsoft Defender for Cloud to [secure your Azure resources](https://learn.microsoft.com/azure/security-center/defender-for-cloud).
* Protecting the Azure Container Apps instance with a [firewall](https://learn.microsoft.com/azure/container-apps/waf-app-gateway) and/or [Virtual Network](https://learn.microsoft.com/azure/container-apps/networking?tabs=workload-profiles-env%2Cazure-cli).

#### Resources

This template creates everything you need to get started with Azure AI Foundry:

* [AI Hub Resource](https://learn.microsoft.com/azure/ai-studio/concepts/ai-resources)
* [AI Project](https://learn.microsoft.com/azure/ai-studio/how-to/create-projects)
* [Azure AI Service](https://learn.microsoft.com/azure/ai-services): Default models deployed are gpt-4o-mini and text-embedding-ada-002, but any Azure AI models can be specified per the [documentation](docs/deploy_customization.md#customizing-model-deployments).
* [AI Search Service](https://learn.microsoft.com/azure/search/) *(Optional, disabled by default)*

The template also includes dependent resources required by all AI Hub resources:

* [Storage Account](https://learn.microsoft.com/azure/storage/blobs/)
* [Key Vault](https://learn.microsoft.com/azure/key-vault/general/)
* [Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview) *(Optional, enabled by default)*
* [Container Registry](https://learn.microsoft.com/azure/container-registry/) *(Optional, enabled by default)*