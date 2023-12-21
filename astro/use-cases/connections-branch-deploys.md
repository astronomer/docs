---
title: 'Manage Astro connections in branch-based deploy workflows'
sidebar_label: 'Connections and branch-based deploys'
id: connections-branch-deploys
---

Airflow DAGs often interact with a multitude of external systems, such as data warehouses and APIs. DAGs access these systems using [Airflow connections](manage-connections-variables.md). A common logistical consideration when running Airflow at scale is deciding how to manage connections between development and production environments. Different environment types require different levels of access to external resources. 

Astro's [branch-based development](automation-overview.md) and [connection management](manage-connections-variables.md) features allow you to automatically share specific Airflow connections with Astro Deployments based on their development context. 

When you combine branch-based deploys and connection management, you can:

- Automatically create Deployments for development branches with a set of development Airflow connections.
- Override preset Airflow connections on a per-Deployment basis to troubleshoot or customize your development environment.
- Promote a Deployment to production as an admin by updating its Airflow connections to access production resources.

## Feature overview

This use case depends on the following Astro features to create a fully integrated CI/CD pipeline:

- Configuring Airflow connections in the [Astro Environment Manager](manage-connections-variables.md).
- Branch-based, or multi-branch Deployments using [CI/CD](set-up-ci-cd.md#multiple-environments).

## Prerequisites

This use case assumes you have:

- At least two Astro Deployments, one for development and one for production.
- A Git-based repository where you manage an Astro project.
- A configured multi-branch CI/CD pipeline. See [CI/CD templates](ci-cd-templates/template-overview.md).

However, you can extend this use case to encompass multiple development or production environments.

## Implementation

To implement this use case:

1. As a Workspace Operator or Admin, create connections in the Astro Environment manager to your development-level resources. See [Create a connection](create-and-link-connections.md#create-a-connection).
2. Set these connections to be available to all Deployments in the Workspace by default. See [Configure connection sharing for a Workspace](create-and-link-connections.md#configure-connection-sharing-for-a-workspace). Your DAG authors can now access external development and testing resources across all Deployments.
3. Choose a Deployment in your Workspace that you want to run your production workflows. In the Deployment, override the connections you configured to instead connect to your production resources. See [Override connection fields](create-and-link-connections.md#override-connection-fields).
4. In the Git repository for your Astro project, define a multi-branch CI/CD pipeline for deploying to Astro. For an example of how to do this in GitHub, see [CI/CD templates](/ci-cd-templates/github-actions.md?tab=multibranch#deploy-action-templates).

Now, when a DAG author deploys to either a production or development Deployment through CI/CD, they can run their DAGs in Astro without needing to configure connections. Additionally, because your production connection shares the same connection ID as your default development connection, DAG authors don't have to update their code to point towards different connections when promoting their code to production.

## Explanation

Using branch-based Deployments with the Astro Environment Manager allows your team to focus on the parts of Astro that matter most for their roles. For example, using the Astro Environment Manager means that you only need one administrative user to manage connections across multiple Deployments:  

- A Workspace Owner [creates an Airflow connection](create-and-link-connections.md#create-a-connection) in the Astro Environment Manager that connects to external development resources. They share this connection to all Deployments by default by turning on the [**Linked to all Deployments** setting](https://docs.astronomer.io/astro/create-and-link-connections#configure-connection-sharing-for-a-workspace).
- In the production Deployment, the Workspace Owner [overrides the linked connection](create-and-link-connections.md#override-connection-fields) to instead connect to production resources on the same external system. Because the connection ID and code are the same, this override requires no updates at the DAG level. 

After a Workspace Owner creates connections, DAG authors can develop DAGs without needing to reconfigure connections between development and production:

- A DAG author creates a new development branch of an Astro project. The CI/CD pipeline for the repository deploys their branch to the development Deployment on Astro. This is known as a [multi-branch CI/CD pipeline](set-up-ci-cd.md#multiple-environments).
- While the DAG author is testing in Astro, they have access to the development resources because the Workspace Author configured a default Airflow connection for the Deployment. The author can [pull this connection onto their local machine](import-export-connections-variables.md#from-the-cloud-ui) for testing purposes, or test by deploying to the development Deployment on Astro.
- When the DAG author finishes development, they merge their development branch into production. The CI/CD pipeline deploys this change to the production Deployment.
- When the DAG author's code runs in the production Deployment, it now accesses production resources based on the overrides configured by the Workspace Owner. 

This use case provides several benefits for both Workspace managers and DAG authors:

- When you use branch-based deploys, your CI/CD pipeline automatically deploys your branches to development Deployments. This saves resources and reduces the complexity of development for DAG authors.
- Workspace Operators and Owners can manage connections without needing access to DAG code.
- DAG authors only need a connection ID to connect their DAGs, meaning they can focus on data engineering instead of connection configuration.
- Connection IDs don't need to be updated when you promote code to production, reducing development timelines and reducing the number of resources to manage. 

## See also

- [Manage Airflow connections and variables](manage-connections-variables.md)
- [Automate actions on Astro](automation-overview.md)
