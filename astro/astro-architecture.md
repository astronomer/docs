---
sidebar_label: 'About Astro'
title: 'About Astro'
id: astro-architecture
description: Learn about how Astro is structured to maximize the power of Apache Airflow.
---

Astro is a fully-managed SaaS application for data orchestration that helps teams run data pipelines with Apache Airflow at any level of scale. Your Airflow infrastructure is managed entirely by Astronomer, enabling you to shift your focus from infrastructure to data. 

## Architecture

To run Airflow on Astro, you need to create a [Deployment](#deployment) using either of these two options:

- **Use a Standard cluster**: This is the default and the quickest way to get Airflow environment up and running on Astro. Standard cluster is a pre-configured multi-tenant Kubernetes cluster.

- **Use a Dedicated cluster**: It is a single-tenant Kubernetes cluster dedicated to your team or organization. Choose this option if:
    - You need private networking support.
    - You want to use a specific cloud provider or region.
    - You need to run Airflow environments in separate clusters for business or security reasons.

You can work with Astro using the [Cloud UI](#cloud-ui), the [Astro CLI](#astro-cli), or the Astro API. Your Airflow environments on Astro, called [Deployments](#deployment), securely connect to external data services, so that you can place Airflow at the core of your data ecosystem. The _Astro Hypervisor_ is an Astronomer-managed component of the Astro platform that facilitates operating and optimizing your Deployments. 

![Astro Hosted architecture overview](/img/docs/astro-architecture-lightmode.png)

## Key concepts

Astro includes tools and features that enable you to enrich your Airflow development and maintenance experience beyond the functionality that open source Airflow provides. 

The following sections give a detailed explaination of Astro tools and features as well as key concepts that you need to understand in order to use Astro to work with Airflow and manage your Astro environment. You can find definitions for additional Astro-specific terminology in the [Astro glossary](astro-glossary.md). 


### Astro CLI

The [Astro CLI](cli/overview.md) tool provides an interface to run Airflow locally and deploy Airflow files to Astro from either a local machine or a CI/CD process. The Astro CLI is open source and requires either Docker or an alternative container management tool, like Podman.

An Airflow project created with the Astro CLI is also known as an _Astro project_. It contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. See [Run your first DAG with the Astro CLI](create-first-dag.md) to create your first Astro project locally.

### Cloud UI

The Cloud UI, hosted at `https://cloud.astronomer.io`, is the primary interface for accessing and managing Astro from your web browser. It provides you a serverless Airflow experience from a single screen. You can use the Cloud UI to:

- Access the Airflow UI for your hosted Airflow environments.
- Customize Airflow resources without editing configuration files.
- Allocate infrastructure resources to your Airflow environment.
- Manage users and teams with role-based access control (RBAC).
- Create and edit DAGs in the Astro Cloud IDE.

### Deployment

An Astro _Deployment_ is an Airflow environment hosted on Astro. It encompasses all core Airflow components, including the Airflow webserver, scheduler, and workers, along with additional tools for reliability and observability. It runs in an isolated Kubernetes namespace in an [Astro cluster](#cluster) and has a set of attached resources to run your Airflow tasks.

Compared to an open source Airflow environment, an Astro Deployment is easy to create, delete, and modify through either the Cloud UI or with the Astro CLI. You can [fine-tune resources and settings](deployment-settings.md) directly from the Cloud UI, see metrics and analytics for your DAGs, review your deploy history, and more. The infrastructure required to run a Deployment is managed by Astronomer.

To run DAGs in a Deployment, you must either deploy an Astro project manually from your local machine or configure an automated deploy process using a third-party CI/CD tool with the Astro CLI. Then, you can open the Airflow UI from the Cloud UI and view your DAGs. See [Run your first DAG](create-first-dag.md) to get started with examples of either workflow.

### Astro Runtime

_Astro Runtime_ is a [debian-based Docker image](https://quay.io/repository/astronomer/astro-runtime) that bundles Apache Airflow with optimized configurations and add-ons that make your Airflow experience reliable, fast, and scalable. Astronomer releases an Astro Runtime distribution for each version of Apache airflow.

Every Deployment and Astro project uses Astro Runtime at its core. Astronomer provides [extended support and bug fixes](runtime-version-lifecycle-policy.md) to Astro Runtime versions, so that you can keep your DAGs running for longer without disruption.

See [Astro Runtime Architecture and features](runtime-image-architecture.md) for a complete feature list.

### Workspace

A _Workspace_ is a collection of Deployments that can be accessed by a specific group of users. You can use a Workspace to group Deployments that share a business use case or environment trait. For example, your data science team might have a dedicated Workspace with two Deployments within it. Workspaces don't require any resources to run and are only an abstraction for grouping Deployments and configuring user access to them. All Deployments must belong to a Workspace.

You can assign new users [Workspace roles](user-permissions.md#workspace-roles) that include varying levels of access to your Deployments.

### Cluster

A _cluster_ in Astro is a Kubernetes cluster that hosts the infrastructure required to run your Airflow environments, also known as [Deployments](#deployment) in Astro. There are two types of clusters in Astro:

- *Standard cluster*: It is a multi-tenant pre-configured cluster. Astro allows you to choose a standard cluster, from a supported cloud provider and region, to host your Deployments in isolated Kubernetes namespaces. See [available cloud providers and regions for Standard cluster](resource-reference-hosted.md#standard-cluster-configurations).

- *Dedicated cluster*: It is a single-tenant cluster for exlcusive use by your organization or team. Dedicated clusters provide more configuration options for [cloud providers, regions](resource-reference-hosted.md#dedicated-cluster-configurations), [private network connectivity](https://docs.astronomer.io/astro/category/connect-to-external-resources), and [security](authorize-workspaces-to-a-cluster.md) than standard clusters. To use a Dedicated cluster in your Astro Deployment, you must create it first by selecting the cloud provider and region of your choice. See [Create a Dedicated cluster](create-dedicated-cluster.md). Dedicated cluster has an additional charge.

For both cluster types, Astro manages all underlying infrastructure and provides secure connectivity options to all data services in your ecosystem.

### Organization

An Astro _Organization_ is the highest level entity in Astro and represents a shared space for your company on Astro. An Organization is automatically created when you first sign up for Astronomer. At the Organization level, you can manage all of your users, Deployments, Workspaces, and clusters from a single place in the Cloud UI. 

To securely manage user access, you can [integrate your Organization with an identity provider (IdP)](configure-idp.md) and [set up SCIM provisioning](set-up-scim-provisioning.md) to have new users automatically join Astro with the correct permissions. 

## Access control architecture

Astro uses role-based access control (RBAC) to define which users are permitted to take certain actions or access certain resources. For example, you can assign a user or automation tool permission to deploy DAGs, but not to delete a Deployment. Roles in Astro are defined at the Workspace and Organization levels. 

Each Astro user has a Workspace role in every Workspace they belong to, plus a single Organization role. Users can also belong to [Teams](manage-teams.md), which apply the same role across a group of users. To automate managing user roles or deploying code, you can create API tokens with specific roles to automate most actions on Astro. 

Use the following diagram as a reference for how these components interact with each other in Astro.

![A diagram showing how all Astro RBAC components fit together](/img/docs/rbac-overview.png)