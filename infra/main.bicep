targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Location for all resources')
// Look for desired models on the availability table:
// https://learn.microsoft.com/azure/ai-services/openai/concepts/models#global-standard-model-availability
@allowed([
  'australiaeast'
  'brazilsouth'
  'canadaeast'
  'eastus'
  'eastus2'
  'francecentral'
  'germanywestcentral'
  'japaneast'
  'koreacentral'
  'northcentralus'
  'norwayeast'
  'polandcentral'
  'spaincentral'
  'southafricanorth'
  'southcentralus'
  'southindia'
  'swedencentral'
  'switzerlandnorth'
  'uksouth'
  'westeurope'
  'westus'
  'westus3'
])
@metadata({
  azd: {
    type: 'location'
  }
})
param location string

@description('The Azure resource group where new resources will be deployed')
param resourceGroupName string = ''
@description('The Azure AI Studio Hub resource name. If ommited will be generated')
param aiHubName string = ''
@description('The Azure AI Studio project name. If ommited will be generated')
param aiProjectName string = ''
@description('The application insights resource name. If ommited will be generated')
param applicationInsightsName string = ''
@description('The AI Services resource name. If ommited will be generated')
param aiServicesName string = ''
@description('The AI Services connection name. If ommited will use a default value')
param aiServicesConnectionName string = ''
@description('The AI Services content safety connection name. If ommited will use a default value')
param aiServicesContentSafetyConnectionName string = ''
@description('The Azure Container Registry resource name. If ommited will be generated')
param containerRegistryName string = ''
@description('The Azure Key Vault resource name. If ommited will be generated')
param keyVaultName string = ''
@description('The Azure Search resource name. If ommited will be generated')
param searchServiceName string = ''
@description('The Azure Search connection name. If ommited will use a default value')
param searchConnectionName string = ''
@description('The Azure Storage Account resource name. If ommited will be generated')
param storageAccountName string = ''
@description('The log analytics workspace name. If ommited will be generated')
param logAnalyticsWorkspaceName string = ''
@description('Id of the user or app to assign application roles')
param principalId string = ''

// Chat completion model
@description('Format of the chat model to deploy')
@allowed(['Microsoft', 'OpenAI'])
param chatModelFormat string

@description('Name of the chat model to deploy')
param chatModelName string
@description('Name of the model deployment')
param chatDeploymentName string

@description('Version of the chat model to deploy')
// See version availability in this table:
// https://learn.microsoft.com/azure/ai-services/openai/concepts/models#global-standard-model-availability
param chatModelVersion string

@description('Sku of the chat deployment')
param chatDeploymentSku string

@description('Capacity of the chat deployment')
// You can increase this, but capacity is limited per model/region, so you will get errors if you go over
// https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits
param chatDeploymentCapacity int

// Embedding model
@description('Format of the embedding model to deploy')
@allowed(['Microsoft', 'OpenAI'])
param embedModelFormat string

@description('Name of the embedding model to deploy')
param embedModelName string
@description('Name of the embedding model deployment')
param embedDeploymentName string

@description('Version of the embedding model to deploy')
// See version availability in this table:
// https://learn.microsoft.com/azure/ai-services/openai/concepts/models#embeddings-models
@secure()
param embedModelVersion string

@description('Sku of the embeddings model deployment')
param embedDeploymentSku string

@description('Capacity of the embedding deployment')
// You can increase this, but capacity is limited per model/region, so you will get errors if you go over
// https://learn.microsoft.com/azure/ai-services/openai/quotas-limits
param embedDeploymentCapacity int

param useContainerRegistry bool = true
param useApplicationInsights bool = true
param useSearch bool = false

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var projectName = !empty(aiProjectName) ? aiProjectName : 'ai-project-${resourceToken}'
var tags = { 'azd-env-name': environmentName }

var aiDeployments = [
  {
    name: chatDeploymentName
    model: {
      format: chatModelFormat
      name: chatModelName
      version: chatModelVersion
    }
    sku: {
      name: chatDeploymentSku
      capacity: chatDeploymentCapacity
    }
  }
  {
    name: embedDeploymentName
    model: {
      format: embedModelFormat
      name: embedModelName
      version: embedModelVersion
    }
    sku: {
      name: embedDeploymentSku
      capacity: embedDeploymentCapacity
    }
  }
]

//for container and app api
param apiAppExists bool = false

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

module ai 'core/host/ai-environment.bicep' = {
  name: 'ai'
  scope: rg
  params: {
    location: location
    tags: tags
    hubName: !empty(aiHubName) ? aiHubName : 'ai-hub-${resourceToken}'
    projectName: projectName
    keyVaultName: !empty(keyVaultName) ? keyVaultName : '${abbrs.keyVaultVaults}${resourceToken}'
    storageAccountName: !empty(storageAccountName)
      ? storageAccountName
      : '${abbrs.storageStorageAccounts}${resourceToken}'
    aiServicesName: !empty(aiServicesName) ? aiServicesName : 'aoai-${resourceToken}'
    aiServicesConnectionName: !empty(aiServicesConnectionName) ? aiServicesConnectionName : 'aoai-${resourceToken}'
    aiServicesContentSafetyConnectionName: !empty(aiServicesContentSafetyConnectionName)
      ? aiServicesContentSafetyConnectionName
      : 'aoai-content-safety-connection'
    aiServiceModelDeployments: aiDeployments
    logAnalyticsName: !useApplicationInsights
      ? ''
      : !empty(logAnalyticsWorkspaceName)
          ? logAnalyticsWorkspaceName
          : '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: !useApplicationInsights
      ? ''
      : !empty(applicationInsightsName) ? applicationInsightsName : '${abbrs.insightsComponents}${resourceToken}'
    containerRegistryName: !useContainerRegistry
      ? ''
      : !empty(containerRegistryName) ? containerRegistryName : '${abbrs.containerRegistryRegistries}${resourceToken}'
    searchServiceName: !useSearch
      ? ''
      : !empty(searchServiceName) ? searchServiceName : '${abbrs.searchSearchServices}${resourceToken}'
    searchConnectionName: !useSearch
      ? ''
      : !empty(searchConnectionName) ? searchConnectionName : 'search-service-connection'
  }
}

var hostName = split(ai.outputs.discoveryUrl, '/')[2]
var projectConnectionString = '${hostName};${subscription().subscriptionId};${rg.name};${projectName}'

module userAcrRolePush 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-acr-role-push'
  scope: rg
  params: {
    principalId: principalId
    roleDefinitionId: '8311e382-0749-4cb8-b61a-304f252e45ec'
  }
}

module userAcrRolePull 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-acr-role-pull'
  scope: rg
  params: {
    principalId: principalId
    roleDefinitionId: '7f951dda-4ed3-4680-a7ca-43fe172d538d'
  }
}

module userRoleDataScientist 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-role-data-scientist'
  scope: rg
  params: {
    principalId: principalId
    roleDefinitionId: 'f6c7c914-8db3-469d-8ca1-694a8f32e121'
  }
}

module userRoleSecretsReader 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-role-secrets-reader'
  scope: rg
  params: {
    principalId: principalId
    roleDefinitionId: 'ea01e6af-a1c1-4350-9563-ad00f8c72ec5'
  }
}

module userRoleAzureAIDeveloperUser 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-role-azureai-developer-user'
  scope: rg
  params: {
    principalId: principalId
    roleDefinitionId: '64702f94-c441-49e6-a78b-ef80e0188fee'
  }
}

module userRoleAzureAIDeveloperBackend 'core/security/role.bicep' = if (!empty(principalId)) {
  name: 'user-role-azureai-developer-backend'
  scope: rg
  params: {
    principalId: api.outputs.SERVICE_API_IDENTITY_PRINCIPAL_ID
    roleDefinitionId: '64702f94-c441-49e6-a78b-ef80e0188fee'
  }
}

//Container apps host and api
// Container apps host (including container registry)
module containerApps 'core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: rg
  params: {
    name: 'app'
    location: location
    tags: tags
    containerAppsEnvironmentName: 'containerapps-env-${resourceToken}'
    containerRegistryName: ai.outputs.containerRegistryName
    logAnalyticsWorkspaceName: ai.outputs.logAnalyticsWorkspaceName
  }
}

// API app
module api 'api.bicep' = {
  name: 'api'
  scope: rg
  params: {
    name: 'ca-api-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}api-${resourceToken}'
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    projectConnectionString: projectConnectionString
    chatDeploymentName: chatDeploymentName
    exists: apiAppExists
  }
}

// output the names of the resources
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name

output AZURE_AIHUB_NAME string = ai.outputs.hubName
output AZURE_AIPROJECT_NAME string = ai.outputs.projectName

output AZURE_AISERVICES_NAME string = ai.outputs.aiServicesName
output AZURE_AISERVICES_ENDPOINT string = ai.outputs.aiServiceEndpoint

output AZURE_SEARCH_NAME string = ai.outputs.searchServiceName
output AZURE_SEARCH_ENDPOINT string = ai.outputs.searchServiceEndpoint

output AZURE_KEYVAULT_NAME string = ai.outputs.keyVaultName
output AZURE_KEYVAULT_ENDPOINT string = ai.outputs.keyVaultEndpoint

output AZURE_STORAGE_ACCOUNT_NAME string = ai.outputs.storageAccountName
output AZURE_STORAGE_ACCOUNT_ENDPOINT string = ai.outputs.storageAccountName

output AZURE_APPLICATION_INSIGHTS_NAME string = ai.outputs.applicationInsightsName
output AZURE_LOG_ANALYTICS_WORKSPACE_NAME string = ai.outputs.logAnalyticsWorkspaceName

output AZURE_AIPROJECT_CONNECTION_STRING string = projectConnectionString

//Container and api
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output SERVICE_API_IDENTITY_PRINCIPAL_ID string = api.outputs.SERVICE_API_IDENTITY_PRINCIPAL_ID
output SERVICE_API_NAME string = api.outputs.SERVICE_API_NAME
output SERVICE_API_URI string = api.outputs.SERVICE_API_URI
output SERVICE_API_IMAGE_NAME string = api.outputs.SERVICE_API_IMAGE_NAME
output SERVICE_API_ENDPOINTS array = ['${api.outputs.SERVICE_API_URI}']
