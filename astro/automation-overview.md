---
sidebar_label: 'Overview'
title: 'Automate workflows on Astro'
id: automation-overview
description: Learn how you can automate various actions on Astro to quickly build and manage your data ecosystem. 
---

You can manage different components of Astro using Astro CLI and automate most of the actions, including: 

- Managing users
- Deploying code
- Creating Deployments, etc.

If you need to perform some actions repeatedly, it is beneficial to combine them into workflows and automate these workflows using a tool of your choice. This helps to make your repeated processes more reliable and also allows you to limit permissions for specific actions. One of the most common example is automating your CI/CD workflows.

This section of documentation covers how to automate your common processes on Astro using Astro CLI. Generally speaking, this requires two steps:

- Authenticate to Astro. See [Authenticate to Astro](automation-authentication.md).
- Write and run your script. See the following documents to learn how to write and run scripts for different use cases:

    - [Manage Deployments as code](manage-deployments-as-code.md)
    - [Configure a CI/CD workflow](set-up-ci-cd.md)

By default every Astro user can access Astro components programmatically using Astro CLI. The scope of this access is based on the [permissions](user-permissions.md) assigned to a user at the Organization and Worksapce level. While your [Astro user credentials](./log-in-to-astro.md#log-in-to-the-astro-cli) can be used for programmatic access to Astro using Astro CLI, API tokens are recommended to automate your workslows. 

## Automation best practices

- Always give your API token or key the minimum permissions required to perform an action. This ensures fine-grained control over your Astro components and hence, better security.
- Always set an expiration date for your API tokens.
- Always rotate your API tokens for enhanced security.
- Avoid giving users direct access to production Deployments or Workspaces. See [Astro's heirarchical role-based access control (RBAC)](./astro-architecture.md#access-control-architecture) model.
- [Enforce CI/CD deploys](./configure-deployment-resources.md#enforce-cicd-deploys) for your production Deployments to avoid accidental deploys by users while testing.

## Common automation use cases

### Deployment actions

- Deploy code to your Deployment [using CI/CD tools](set-up-ci-cd.md).
- Update your Deployment using the Deployment file.  
- [Update your Deployment](cli/astro-deployment-update.md), such as changing the executor or number scheduler AUs, etc. 
- [Enforce CI/CD](configure-deployment-resources.md#enforce-cicd-deploys) or [enable DAG-only deploys](deploy-dags.md#enable-dag-only-deploys-on-a-deployment) for your Deployment 
- Fetch a short-lived access token to use [Airflow REST API](airflow-api.md) for your Deployment. This assumes the same permissions as your API key.

### Workspace actions

- Create and update Deployments in your Workspace using a Deployment file. 
- [Manage users, teams, and tokens](cli/astro-workspace-team.md) in your Workspace.
- Create ephemeral Deployments in your Workspace using your CI/CD process. 
- Perform all Deployment-level actions in any Deployment in a Workspace. 

### Organization actions

- [Manage Workspaces](cli/astro-workspace-create.md), such as creating, deleting, and switching Workspaces. 
- [Manage users, teams, and tokens](cli/astro-organization-list.md), such as inviting new users, rotating existing tokens, etc.
- [Export audit logs](audit-logs.md#export-audit-logs). 
- Perform all Workspace-level actions in any Workspace in your Organization.

