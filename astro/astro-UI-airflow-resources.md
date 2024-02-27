---
sidebar_label: 'How the Astro UI stores and fetches details'
title: 'How the Astro UI stores and fetches Airflow connection and variable details'
id: astro-UI-airflow-resources
description: "Learn about how the Astro UI allows you to create Airflow connections and variables, then link them across Deployments."
---

import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

You can create and manage Airflow connections or variables for Deployments in the Astro UI, using an Astro-managed secrets backend to store connection and variable configurations as Kubernetes Secrets.

The Astro UI allows you to quickly and securely create connections or variables once and then share them to multiple Deployments without needing to set up your own secrets backend. You can also create a connection or variable once and use it across multiple Airflow Deployments.

Workspace Owners and Operators can create and assign connections or variables, while Workspace Authors can view configured connections or variables and use them in Deployments. If your Organization has [**Environment Secrets Fetching**](organization-settings.md#configure-environment-secrets-fetching-for-the-astro-environment-manager) enabled, you can additionally use configured connections, including ones that contain secrets, in local development environments. See [Import and export connections and variables](cli/local-connections.md).

![Example of the Connections tab in the Astro Environment Manager page](/img/docs/connections-env-mgmt.png)

## How information is stored

When you create an Airflow connection or variable in the Environment Manager, Astro stores Airflow connection or variable details in an Astronomer-hosted secrets manager, and then applies connections and variables to Deployments as Kubernetes Secrets. Specifically the following steps occur:

- Astro stores the connection or variable details in a secure secrets manager hosted by Astronomer.
- When a connection or variable is assigned to a Deployment, Astro uses Airflow's provided [local filesystem secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/local-filesystem-secrets-backend.html) to mount your connections and variables as Kubernetes Secrets.
- When your DAGs use your connections or variables, Airflow reads the details from the filesystem using the Airflow local filesystem secrets backend.

This process occurs every time you create or update a connection or variable.

When you use connections or variables for local development, the Astro CLI reads the connections from the Astro API and injects them into the local Airflow instance's metadata database.

### Fetching environment secrets

The Astro CLI can automatically retrieve connections and variables from the Cloud UI when you start your local Airflow instance, which means you can use your connection details or variables without needing to manage credentials between local and deployed environments. Local environments fetch information the same way as for Deployments, so they require an active internet connection and for you to be logged in with the Astro CLI. You can only fetch environment secrets from Deployments that belong to Workspaces where you are at least a Workspace Member.

:::tip

By default, connections can't be exported locally. However, if you want to work with connections locally, the Organization Owner can enable [**Environment Secrets Fetching**](organization-settings.md#configure-environment-secrets-fetching-for-the-astro-environment-manager) in the Cloud UI.

:::

## Related topics

- [Create Airflow connections in the Astro UI](create-and-link-connections.md)
- [Create Airflow variables in the Astro UI](create-airflow-vars-in-astro.md)
- [Manage Astro connections in branch-based deploy workflows](best-practices/connections-branch-deploys.md)