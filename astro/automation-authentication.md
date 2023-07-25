---
sidebar_label: 'Authentication'
title: 'Authenticate to Astro from an automation tool'
id: automation-authentication
description: Learn about all possible ways that you can authenticate to Astro from the Astro CLI and automation tools.
---

Astro's authentication process is based on [Auth0 Identifier First Authentication flow](https://auth0.com/docs/authenticate/login/auth0-universal-login/identifier-first). Before you can use scripting or automation on Astro, you must prove to Astro that your automation tool is using the right identity to access specific Astro resources. You can do this using the Astro CLI.

For most automation tools, you complete the following actions to authenticate to Astro:

- Create a credential in Astro.
- Install the Astro CLI in the environment where you want to run automated actions, such as a GitHub action.
- Make the credential accessible to the Astro CLI installed in your automation environment.

## Create a credential

You can use any of the following credentials to authenticate in an automated process:

- A Deployment API key.
- A Workspace API token.
- An Organization API token.

You can create API tokens with granular access permissions, ensuring these tokens are not over-provisioned for their intended use.

## Install the Astro CLI in your automation tool

## Make credentials accessible to the Astro CLI


### Deployment API keys

:::caution

Deployment API keys will soon be deprecated in favor of Deployment API tokens. If you have strict Deployment-level security requirements, you can continue to use Deployment API keys, but you will have to complete a one-time migration to Deployment API tokens in the future. Otherwise, Astronomer recommends using either Workspace API tokens or Organization API tokens in place of Deployment API keys.

:::

A Deployment API key, a unique key ID and secret pair, provides an alternative to manual user authentication. It is strictly scoped to a Deployment. You can use API keys to automate common actions on Astro that require manual inputs.

To use a Deployment API key as an authentication method, export the following environment variables in your local or CI/CD environment:

```bash

ASTRONOMER_KEY_ID=<your-api-key-id>
ASTRONOMER_KEY_SECRET=<your-api-key-secret>

```

When using a Deployment API key, keep the following in mind:

- A Deployment API key ID and secret are permanently valid.
- Deployment API keys are deleted permanently if their corresponding Deployment is deleted.
- A Deployment API key is not bound to the user who creates it. When a user who created the API key is removed from the Workspace, or their permissions change, the Deployment and CI/CD workflows that use that API key are not affected.
- Any user or service with access to an API key and secret can access the corresponding Deployment. The only way to delete this access is to delete the API key or delete the Deployment.


### Workspace API tokens

A Workspace API token is strictly scoped to a Workspace. You can use Workspace API tokens to automate actions you perform on a Workspace or the Deployments in a Workspace. 

To use a Workspace API token as an authentication method, export the following environment variable in your local or CI/CD environment:

```bash

ASTRO_API_TOKEN=<your-api-token>

```

### Organization API tokens

To use an Organization API token as an authentication method, export the following environment variable in your local or CI/CD environment:

```bash

ASTRO_API_TOKEN=<your-api-token>
w
```