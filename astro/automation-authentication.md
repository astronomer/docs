---
sidebar_label: 'Authenticate your automation tool'
title: 'Authenticate to Astro for automated workflows'
id: automation-authentication
description: Learn about all possible ways that you can authenticate your automation tool to Astro.
---

Before you can automate actions on Astro, you must prove to Astro that your automation tool has the correct identity and access to interact with specific Astro resources. Complete the following actions to authenticate to Astro using the Astro CLI and API tokens:

- Create an API key or token in Astro.
- Install the Astro CLI in your automation environment, such as a GitHub Actions.
- Make the key or token accessible to the Astro CLI installed in your automation environment.

After you complete this setup, your automation environment is authenticated to Astro. You can then write and run scripts to manage your Deployments through CI/CD.

Astro's authentication process is based on the [Auth0 Identifier First Authentication flow](https://auth0.com/docs/authenticate/login/auth0-universal-login/identifier-first). This process doesn't provide authorization and isn't affected by what a user can do in Astro. To manage authorization in Astro, see [User permissions](user-permissions.md).

## Step 1: Create an API token or API key

You can use any of the following credentials to authenticate in an automated process:

- A Deployment API key. See [Create a Deployment API key](api-keys.md).
- A Workspace API token. See [Create a Workspace API token](workspace-api-tokens.md).
- An Organization API token. See [Create an Organization API token](organization-api-tokens.md).

When you create an API token or key for your environment, keep the following best practices in mind:

- Always give your API token or key the minimum permissions required to perform an action. This improves control and security over your Astro components. For example, instead of creating an Organization API token to automate actions across two  Workspaces, create a separate Workspace API token for each Workspace.

- Always set an expiration date for your API tokens.
- Always [rotate your API tokens](workspace-api-tokens.md#rotate-a-workspace-api-token) for enhanced security.

## Step 2: Install the Astro CLI in your automation tool

To manage your Astro workflows programmatically, you must install the Astro CLI in the environment which will run the workflows. Typically, this requires running `curl -sSL install.astronomer.io | sudo bash -s` or an equivalent installation command before your process starts. See [CI/CD templates](ci-cd-templates/template-overview.md) for examples of how to install the Astro CLI in different version management and workflow automation environments. 

## Step 3: Add your API token or API key to your environment

To make your API key or token accessible to the Astro CLI, you need to set specific environment variables in your CI/CD tool or automation environment.

:::caution

Because these environment variables store sensitive credentials, Astronomer recommends encrypting the variable values before using them in your script. You can do this either directly in your automation tool or in a secrets backend. 

:::

To use a Deployment API key as an authentication credential, set the following environment variables in your script:

```bash
ASTRONOMER_KEY_ID=<your-api-key-id>
ASTRONOMER_KEY_SECRET=<your-api-key-secret>
```

To use a Workspace or Organization API token as an authentication credential, set the following environment variable in your script: 

```bash
ASTRO_API_TOKEN=<your-api-token>
```

## See also

- [Develop a CI/CD workflow](set-up-ci-cd.md)
- [Manage Deployments as code](manage-deployments-as-code.md)