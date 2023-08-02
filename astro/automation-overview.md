---
sidebar_label: 'Overview'
title: 'Automate operational workflows on Astro'
id: automation-overview
description: Learn how you can automate various actions on Astro to quickly build and manage your data ecosystem. 
---

Astro has various components such as, Organization, Workpsace, Deployments, users, Teams, tokens, etc. You can manage these using Astronomer's [Cloud UI](log-in-to-astro.md#log-in-to-the-cloud-ui) or [Astro CLI](cli/overview.md). By default every Astro user can access Astro components programmatically using Astro CLI. The scope of this access is based on the [permissions](user-permissions.md) assigned to a user at the Organization and Worksapce level.

Though, Cloud UI is self-explanatory and easy to use, programmatic access to your Astro components is required for various use-cases. This typically includes, [deploying your local Astro project](./deploy-code.md), for automated [deploys using CI/CD](./set-up-ci-cd.md), or to automate common processes to manage your other Astro components. 

While your [Astro user credentials](./log-in-to-astro.md#log-in-to-the-astro-cli) can be used for programmatic access to Astro, API tokens are recommended to be used for CI/CD and other common processes for production-grade Deployments. Astronomer recommends not to give direct access to users for deploying code to your production Deployments. You can implement appropriate controls for users using [Astro's heirarchical role-based access control (RBAC)](./astro-architecture.md#access-control-architecture) for Astro Organization and Workspaces, and also [enforce CI/CD deploys](./configure-deployment-resources.md#enforce-cicd-deploys) for your Deployments.

## Common use-cases to automate

| API token scope | Use-cases                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deployment      | - Deploy code to your Deployment [using CI/CD tools](set-up-ci-cd.md). <br /> - Update your Deployment using the Deployment file. <br /> - [Update your Deployment](cli/astro-deployment-update.md), such as changing the executor or number scheduler AUs, etc. <br /> - [Enforce CI/CD](configure-deployment-resources.md#enforce-cicd-deploys) or [enable DAG-only deploys](deploy-dags.md#enable-dag-only-deploys-on-a-deployment) for your Deployment <br /> - Fetch a short-lived access token to use [Airflow REST API](airflow-api.md) for your Deployment. This assumes the same permissions as your API key. <br /> |
| Workspace       | - Create and update Deployments in your Workspace using a Deployment file. <br /> - [Manage users, teams, and tokens](cli/astro-workspace-team.md) in your Workspace. <br /> - Create ephemeral Deployments in your Workspace using your CI/CD process. <br /> - Perform all Deployment-level actions in any Deployment in your Workspace. <br />                                                                                                                                                                                                                   |
| Organization    | - [Manage Workspaces](cli/astro-workspace-create.md), such as creating, deleting, and switching Workspaces. <br /> - [Manage users, teams, and tokens](cli/astro-organization-list.md), such as inviting new users, rotating existing tokens, etc. <br /> - [Exporting audit logs](audit-logs.md#export-audit-logs). <br /> - Perform all Workspace-level actions in any Workspace in your Organization <br />   

## Best Practices

- Always use the least-privilege approach to automate your processes using the API keys or tokens to ensure secure and fine-grained control over your Astro components.
- Always set an expiration date for your API tokens.
- Always rotate your API tokens for enhanced security.
- Avoid giving direct access to individual users to production Deployments or Workspaces.
- Enforce CI/CD deploys for your production Deployments to avoid accidental deploys by users while testing.