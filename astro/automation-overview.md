---
sidebar_label: 'Overview'
title: 'Automate workflows on Astro'
id: automation-overview
description: Learn how you can automate various actions on Astro to quickly build and manage your data ecosystem. 
---

You can complete most actions available in Astro using the Astro CLI, including:

- Managing users
- Deploying code
- Creating Deployments

If you use Astro CLI in scripts or automation tools, you can automate most workflows on Astro. This is helpful if you need to complete the same actions many times reliably, or you want to limit permissions for specific actions to a tightly controlled automation tool. 

This section of documentation covers how to automate actions on Astro. Generally speaking, automation on Astro requires two steps:

- Authenticate your automation tool to Astro. See [Authenticate to Astro from an automation tool](automation-authentication.md).
- Write and run your script. See the following documents to learn how to write and run scripts for different use cases:

    - [Manage Deployments as code](manage-deployments-as-code.md)
    - [Configure a CI/CD workflow](set-up-ci-cd.md)

## Automation best practices

- Always give your automation tool the lest permissions required to improve security for your Astro resources.
- Always set an expiration date for your API tokens.
- Always rotate your API tokens for enhanced security.
- Avoid giving users direct access to production Deployments or Workspaces.
- Enforce CI/CD deploys for your production Deployments to avoid accidental deploys by users while testing.

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

