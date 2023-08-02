---
sidebar_label: 'Authentication'
title: 'Authenticate to Astro using Astro CLI'
id: automation-authentication
description: Learn about all possible ways that you can authenticate the Astro CLI and automation tools for automated workflows.
---

Authentication is a process that proves a user's identity in Astro. Astro's authentication process is based on [Auth0 Identifier First Authentication flow](https://auth0.com/docs/authenticate/login/auth0-universal-login/identifier-first). This process doesn't provide authorization and doesn't care what a user can do in Astro. To manage authorization for a user in Astro, see [User permissions](./user-permissions.md). 

To manage your Astro components using Astro CLI, you must first [log in to Astro](log-in-to-astro.md#log-in-to-the-astro-cli). You can use either of the following methods to authenticate to Astro from Astro CLI:

- Your Astro user credentials, which generates a short-lived authentication token.
- A Deployment API key.
- A Workspace API token.
- An Organization API token.

To access your Deployment manually from your local machine, or to deploy changes to your Deployment, you can use your Astro user credentials. For programmatic access, Astronomer recommends to use the API token or API key method. 

## Benefits of API tokens or API keys

Team leaders and administrators can use Organization and Workspace permissions to give proper authorization to API tokens and keys just like to an Astro user. You can use an API token to complete the following actions without authenticating as a user:

- Deploy code to Astro through CI/CD with tools such as GitHub Actions or Circle CI.
- Create ephemeral Deployments for testing your DAGs before Production deploy.
- Enforce CI/CD for your Production Deployments allowing only API tokens to deploy changes.
- Update Deployment resources, such as changing the executor, changing the number scheduler AUs, etc.
- Fetch a short-lived access token to use Airflow REST API on Astro. This token assumes the permissions of a API token or an API key used in the request. See [Make requests to Airflow REST API](airflow-api.md) for details.

## Astro user based access

Your Astro user *authenticates* to the Astro platform and the permissions assigned to you user in Astro *authorizes* access to the Workspaces and Deployments in your Organization. For example, if your Astro user has permissions of Organization Member and Workspace Viewer for Workspace A, you will not be able to create any Deployments or push changes to any Deployments in Workspace A. Whereas, if your user has permissions of Workspace Editor in Workspace B, you will be able to create Deployments or push changes to Deployments in Workspace B.

To login to the Astro platform using your user credentials, use Astro CLI command [`astro login`](log-in-to-astro.md#log-in-to-the-astro-cli). If you do not have access to a browser, you can use [browserless authentication](log-in-to-astro.md#browserless-authentication).

## API based access

Astronomer provides API based access to authorize to your Astro platform. Astro API tokens enable you to easily automate critical functions, at the Deployment, Workspace, and Organization level. You can create API tokens with granular access permissions, ensuring these tokens are not over-provisioned for their intended use.

### A Deployment API key

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


### A Workspace API token

A Workspace API token is strictly scoped to a Workspace. You can use Workspace API tokens to automate actions you perform on a Workspace or the Deployments in a Workspace. 

To use a Workspace API token as an authentication method, export the following environment variable in your local or CI/CD environment:

```bash

ASTRO_API_TOKEN=<your-api-token>

```

### An Organization API token

To use a Workspace API token as an authentication method, export the following environment variable in your local or CI/CD environment:

```bash

ASTRO_API_TOKEN=<your-api-token>

```