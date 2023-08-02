---
sidebar_label: 'Authentication'
title: 'Authenticate to Astro from an automation tool'
id: automation-authentication
description: Learn about all possible ways that you can authenticate to Astro from the Astro CLI and automation tools.
---

Astro's authentication process is based on [Auth0 Identifier First Authentication flow](https://auth0.com/docs/authenticate/login/auth0-universal-login/identifier-first). This process doesn't provide authorization and doesn't care what a user can do in Astro. 

Before you can use scripting or automation on Astro, you must prove to Astro that your automation tool is using the right identity to access specific Astro resources. You can do this using the Astro CLI.

For most automation tools, you complete the following actions to authenticate to Astro:

- Create a credential in Astro.
- Install the Astro CLI in the environment where you want to run automated actions, such as a GitHub action.
- Make the credential accessible to the Astro CLI installed in your automation environment.

## Create a credential

You can use any of the following credentials to authenticate in an automated process:

- A Deployment API key. See [Create a Deployment API key](api-keys.md#create-an-api-key).
- A Workspace API token. See [Create a Workspace API token](workspace-api-tokens.md#create-a-workspace-api-token).
- An Organization API token. See [Create an Organization API token](organization-api-tokens.md#create-an-organization-api-token).

You can create API tokens with role-based access permissions, ensuring that they are not over-provisioned for their intended use. When you chose a credential, you should grant it the least amount of permissions possible for the action it's used for. For example, instead of creating an Organization API token to automate actions in two separate Workspaces, you might be able to create two separate Workspace API tokens for each Workspace. 

:::caution

Deployment API keys will soon be deprecated in favor of Deployment API tokens. If you have strict Deployment-level security requirements, you can continue to use Deployment API keys, but you will have to complete a one-time migration to Deployment API tokens in the future. Otherwise, Astronomer recommends using either Workspace API tokens or Organization API tokens in place of Deployment API keys.

:::

## Install the Astro CLI in your automation tool

To authenticate to Astro and run actions programmatically, you must install the Astro CLI in the environment which will execute the actions. Generally, this requires running `brew install astro` or an equivalent installation command before your process starts. See [CI/CD templates](ci-cd-templates/template-overview.md) for examples of how to install the Astro CLI in different version management and workflow automation environments. 

## Make credentials accessible to the Astro CLI

The Astro CLI uses reserved environment variables to read your credential information and share it with Astro. To successfully authenticate your tool to Astro, you must set these environment variables in your automation environment. 

To use a Deployment API key as an authentication credential, export the following environment variables in your automation environment.

```bash
ASTRONOMER_KEY_ID=<your-api-key-id>
ASTRONOMER_KEY_SECRET=<your-api-key-secret>
```

To use a Workspace or Organization API token as an authentication credential, set the following environment variable in your automation environment. 

```bash

ASTRO_API_TOKEN=<your-api-token>
```