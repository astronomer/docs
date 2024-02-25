---
sidebar_label: 'Astro Environment Manager'
title: 'Manage shared resources for your Airflow environments'
id: astro-environment-manager
description: "Create Airflow resources and then share them with multiple Deployments using the Astro Environment Manager."
---

import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

The Astro Environment Manager allows you to create Airflow resources in Astro, and then share them to different Workspaces and Deployments.

## Using linked resources

By creating Airflow resources at the Workplace level instead of in the Airflow UI of a specific Deployment, you can create variables or connections once and then link them to multiple Deployments.

For example, you can configure a connection with the credentials for a sandbox or development environment. Then, you can later configure your connection to be applied to all Deployments in the workspace by default. This means that when you create new Deployments, they automatically have access to your development environment. Later, you can edit the connection to point to your production resources by using [field overrides](create-and-link-connections.md#override-connection-fields).

You can read about the best practices for using Astro Connections to take streamline sharing resources when you use [branch-based deploy workflows](best-practices/connections-branch-deploys.md).

## Creating connections

Compared to creating a connection in the Airflow UI, when you create a connection in the Cloud UI, you can:

- Share the connection with multiple Deployments within the Workspace.
- Override fields in the connection for individual Deployments.
- Use configured connections in local Airflow environments. See [Import and export connections and variables](cli/local-connections.md).
- Use connections in branch-based deploys and PR previews.

## Configuring Airflow Variables

Compared to creating an Airflow Variable in the Airflow UI, when you create variable in the Cloud UI, you can:

- Share the variable with multiple Deployments within the Workspace.
- Use variables in local Airflow environments. See [Import and export connections and variables](cli/local-connections.md).