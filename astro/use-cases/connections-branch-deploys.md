---
title: 'Manage Astro connections in branch-based deploy workflows'
sidebar_label: 'Connections + branch-based deploys'
id: connections-branch-deploys
---

Airflow DAGs often interact with a multitude of external systems, such as data warehouses and APIs. DAGs access these systems using [Airflow connections](https://docs.astronomer.io/astro/manage-connections-variables). A common logistical consideration when running Airflow at scale is deciding how to manage connections between development and production environments. Different environment types require different levels access to external resources. 

Astro's [branch-based development](https://docs.astronomer.io/astro/automation-overview) and [connection management](https://docs.astronomer.io/astro/manage-connections-variables) features allow you to automatically share specific Airflow connections with Astro Deployments based on their development context. 

When you combine branch-based deploys and connection management, you can:
- Automatically create Deployments for development branches with a set of development Airflow connections.
- Override preset Airflow connections on a per-Deployment basis to troubleshoot or customize your development environment.
- Promote a Deployment to production as an admin by updating its Airflow connections to access production resources.

## Feature overview

This use case depends on three key Astro features to create a fully integrated CI/CD pipeline:

- Configuring Airflow connections in the [Astro Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables).
- Branch-based, or multi-branch Deployments using [CI/CD](https://docs.astronomer.io/astro/set-up-ci-cd.md#multiple-environments).
- Pulling connections into local development branches using [environment secrets fetching](https://docs.astronomer.io/astro/import-export-connections-variables.md#from-the-cloud-ui).

## Prerequisites

This use case assumes you have:

- Two Astro Deployments, one for development and one for production.
- A Git-based repository where you store your Astro project code.
- A configured multi-branch CI/CD pipeline. See [CI/CD templates](ci-cd-templates.md)

However, you can extend this use case to encompass multiple development or production environments.

## Use case

The following workflow is an example of how you can manage Airflow connections between Deployment types using the Astro Environment Manager.

- A Workspace Owner [creates an Airflow connection](https://docs.astronomer.io/astro/create-and-link-connections#create-a-connection) in the Astro Environment Manager that connects to external development resources. They share this connection to all Deployments by default by turning on the [**Linked to all Deployments** setting](https://docs.astronomer.io/astro/create-and-link-connections#configure-connection-sharing-for-a-workspace).
- In the production Deployment, the Workspace Owner [overrides the linked connection](https://docs.astronomer.io/astro/create-and-link-connections#override-connection-fields) to instead connect to production resources on the same external system. Because the connection ID and code are the same, this override requires no updates at the DAG level. 

After the connection is created, DAG authors can develop DAGs without needing to reconfigure connections between development and production.

- A DAG author creates a new development branch of an Astro project. The CI/CD pipeline for the repository deploys their branch to the development Deployment on Astro. This is known as a [multi-branch CI/CD pipeline](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- While the DAG author is testing in Astro, they have access to the development resources because the Workspace Author configured a default Airflow connection for the Deployment. The author can [pull this connection onto their local machine](https://docs.astronomer.io/astro/import-export-connections-variables.md#from-the-cloud-ui) for testing purposes, or test by deploying to the development Deployment on Astro.
- When the DAG author finishes development, they merge their development branch into production. The CI/CD pipeline deploys this change to the production Deployment.
- When the DAG author's code runs in the production Deployment, it now accesses production resources based on the overrides configured by the Workspace Owner. 

This use case provides several benefits for both Workspace managers and DAG authors:

- Workspace Operators and Owners can manage connections without needing access to DAG code.
- DAG authors only need a connection ID to connect their DAGs, meaning they can focus on data engineering instead of connection configuration.
- Connection IDs don't need to be updated when you promote code to Deployment, reducing development timelines and reducing the number of resources to manage. 

## See also

- Documentation: [Manage Airflow connections and variables](https://docs.astronomer.io/astro/manage-connections-variables) on Astro.
- Documentation: [Automate actions on Astro](https://docs.astronomer.io/astro/automation-overview).
- Guide: [Manage Airflow connections](https://docs.astronomer.io/learn/connections).