---
sidebar_label: 'Overview'
title: 'Automate workflows on Astro'
id: automation-overview
description: Learn how you can automate various actions on Astro to quickly build and manage your data ecosystem. 
---

You can use the Astro CLI to automate the management of Deployments and Workspaces. Some common actions you can automate include:

- Managing users.
- Deploying code.
- Creating Deployments.

Automating actions allows you to interact with Astro in a reliable, predictable way that improves security and reduces complexity. For example, when you set up CI/CD code deploys, your DAG authors will no longer have to manually deploy code and can focus on working in their version management tool, such as GitHub.

This section of documentation covers how to automate processes on Astro using Astro CLI. To start automating, you'll first [programmatically authenticate to Astro](automation-authentication.md) using an API key or token. Then, you'll write and run a script to complete the workflow for your use case.

## Common automation use cases

### Deployment actions

- Deploy code to your Deployment using [CI/CD](set-up-ci-cd.md).
- Update your Deployment using a [Deployment file](manage-deployments-as-code.md).  
- Use [Airflow REST API](airflow-api.md) for your Deployment. 

### Workspace actions

- [Manage users, Teams, and tokens](cli/astro-workspace-team.md) in your Workspace.
- Create ephemeral Deployments using CI/CD. 
- Perform all Deployment-level actions on any Deployment in a Workspace. 

### Organization actions

- [Manage Organization users, Teams, and tokens](cli/astro-organization-list.md).
- Export [audit logs](audit-logs.md#export-audit-logs). 

## Automation best practices

- Always give your API token or key the minimum permissions required to perform an action. This improves control and security over your Astro components.
- Always set an expiration date for your API tokens.
- Always rotate your API tokens for enhanced security.
- Avoid giving users direct access to production Deployments or Workspaces. See [Astro's hierarchical role-based access control (RBAC)](astro-architecture.md#access-control-architecture) model.
- [Enforce CI/CD deploys](configure-deployment-resources.md#enforce-cicd-deploys) for your production Deployments to avoid accidental deploys by users while testing.