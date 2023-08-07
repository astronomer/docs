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

This section of documentation covers how to automate processes on Astro using Astro CLI. To start automating, you'll first [programmatically authenticate to Astro](automation-authentication.md) using an API key or token. Then, you'll write and run a script to complete the workflow for your use case.


## Automation best practices

- Always give your API token or key the minimum permissions required to perform an action. This improves control and security over your Astro components.
- Always set an expiration date for your API tokens.
- Always rotate your API tokens for enhanced security.
- Avoid giving users direct access to production Deployments or Workspaces. See [Astro's hierarchical role-based access control (RBAC)](astro-architecture.md#access-control-architecture) model.
- [Enforce CI/CD deploys](configure-deployment-resources.md#enforce-cicd-deploys) for your production Deployments to avoid accidental deploys by users while testing.

## Common automation use cases

### Deployment actions

- Deploy code to your Deployment using [CI/CD](set-up-ci-cd.md).
- Update your Deployment using a Deployment file.  
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

