---
sidebar_label: 'Concepts'
title: 'Astro concepts and components'
id: concepts
description: Learn about each of the components you can interact with in Astro.
---

Astro is a SaaS application that provides fully managed Airflow environments for teams of all sizes. Astro provides you a true serverless Airflow experience making it more reliable, scalable and easy to use. The Astro platform includes a few concepts and components that don't exist in open source Apache Airflow. 

Use this document to learn about key Astro concepts and how they work together on the platform.

## Astro CLI

The [Astro CLI](cli/overview.md) is the primary interface for running Airflow locally and deploying Airflow files to Astro from a local machine or a CI/CD process. The Astro CLI is open source and requires either Docker or an alternative container management tool.

An Airflow project created with the Astro CLI is also known as an _Astro project_. It contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. See [Run your first DAG](create-first-dag.md) to create your first Astro project.

## Astro Runtime

_Astro Runtime_ is a [debian-based Docker image](https://quay.io/repository/astronomer/astro-runtime) that bundles Apache Airflow with optimized configurations and add-ons that make your Airflow experience reliable, fast, and scalable. Astronomer releases an Astro Runtime distribution for each version of Apache airflow.

Every Deployment and Astro project uses Astro Runtime at its core. Astronomer provides [extended support and bug fixes](runtime-version-lifecycle-policy.md) to Astro Runtime versions so that you can keep your DAGs running for longer without disruption. 

## Cloud UI

The Cloud UI, hosted at `https://cloud.astronomer.io`, is the visual interface for accessing and managing Astro. It provides you a serverless Airflow experience from a single screen. You can use the Cloud UI to:

- Access the Airflow UI for your hosted Airflow environments.
- Customize Airflow resources without editing configuration files.
- Manage users and teams with role-based access control (RBAC).
- Create and edit DAGs in the Astro Cloud IDE.
- View data lineage for your data pipelines.

## Deployment

An Astro _Deployment_ is an Airflow environment hosted on Astro. It encompasses all core Airflow components, including the Airflow webserver, scheduler, and workers, along with additional tools for reliability and observability. It runs in an isolated Kubernetes namespace in an [Astro cluster](#cluster) and has a set of attached resources to run your Airflow tasks.

Compared to an open source Airflow environment, an Astro Deployment is easy to create, delete, and modify. You can [fine-tune resources and settings](deployment-settings.md) directly from the Cloud UI, see metrics and analytics for your DAGs, review your deploy history, and more. The infrastructure required to run a Deployment is managed by Astronomer.

To run DAGs in a Deployment, you must either deploy an Astro project manually from your local machine or configure an automated deploy process using a third-party CI/CD tool with the Astro CLI. Then, you can open the Airflow UI from the Cloud UI and view your DAGs. See [Run your first DAG](create-first-dag.md) to get started.

## Workspace

A _Workspace_ is a collection of Deployments that can be accessed by a specific group of users. You can use a Workspace to group Deployments that share a business use case or environment trait. For example, your data science team might have a dedicated Workspace with two Deployments within it. Workspaces don't require any resources to run and are only an abstraction for grouping Deployments and configuring user access to them. All Deployments must belong to a Workspace.

When more users from your company join Astro, you can assign them [Workspace roles](user-permissions.md#workspace-roles) that include varying levels of access to your Deployments.

### Cluster

A _cluster_ on Astro is a Kubernetes cluster that hosts the infrastructure required to run Airflow environments, also known as [Deployments](#deployment) in Astro. You can either use a pre-configured cluster, known as a standard cluster, or create a cluster for exclusive use by your team, known as a [dedicated cluster](create-dedicated-cluster.md). For both cluster types, Astro manages all underlying infrastructure and provides secure connectivity options to all data services in your ecosystem.

## Organization

An Astro _Organization_ is the highest level entity in Astro and represents a shared space for your company on Astro. An Organization is automatically created when you first sign up for Astronomer. At the Organization level, you can manage all of your users, Deployments, Workspaces, and clusters from a single place in the Cloud UI. To securely manage user access, you can [integrate your Organization with an identity provider (IdP)](configure-idp.md) and [set up SCIM provisioning](set-up-scim-provisioning.md) to have new users automatically join Astro with the correct permissions. 

## See also

- [Astro CLI](cli/overview.md)
- [Create a Deployment](create-deployment.md)
- [Deployment resources](resource-reference-hosted.md)

