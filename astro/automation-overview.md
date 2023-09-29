---
sidebar_label: 'Overview'
title: 'Automate actions on Astro'
id: automation-overview
description: Learn how you can automate various actions on Astro to quickly build and manage your data ecosystem. 
---

As an administrator or head of your team, you can use the Astro CLI to automate the management of Deployments and Workspaces. Some common actions you can automate include:

- Managing users.
- Deploying code in a CI/CD pipeline.
- Creating Deployments.

Automating actions allows your team to interact with Astro in a predictable way that improves reliability and security. For example, when you automate code deploys with CI/CD, your can have your users deploy from a source where all of their work is tracked and reviewed, such as GitHub.

This section of documentation covers how to automate processes on Astro using Astro CLI. To start automating, you'll first [programmatically authenticate to Astro](automation-authentication.md) using an API key or token. Then, you'll write and run a script to perform your action.

## Common actions to automate

### Deployment actions

- Deploy code to your Deployment using [CI/CD](set-up-ci-cd.md).
- Update your Deployment using a [Deployment file](manage-deployments-as-code.md).  
- Make a request to your Deployment using the [Airflow REST API](airflow-api.md). 

### Workspace actions

- [Manage users, Teams, and tokens](cli/astro-workspace-list.md) in your Workspace.
- Create [preview Deployments](ci-cd-templates/github-actions.md#deployment-preview-templates) using CI/CD. 
- Perform all Deployment-level actions on any Deployment in a Workspace. 

### Organization actions

- [Manage Organization users, Teams, and tokens](cli/astro-organization-list.md).
- Export [audit logs](audit-logs.md#export-audit-logs). 
