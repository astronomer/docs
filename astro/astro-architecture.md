---
sidebar_label: 'Architecture'
title: 'Astro architecture'
id: astro-architecture
description: Learn about how Astro is structured to maximize the power of Apache Airflow.
---

Astro is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Your Airflow infrastructure is managed entirely by Astronomer, enabling you to shift your focus from infrastructure to data. 

## General architecture

There are two ways to run Astro:

- _Astro Hosted_ is a version of Astro that's hosted and managed on Astronomer's Cloud. This version of Astro is ideal if you want to run Airflow with as little friction as possible.
- _Astro Hybrid_ is a version of Astro that's managed by Astronomer, but your Airflow infrastructure is hosted in your company's cloud. This version of Astro is ideal for companies that want more control over their cloud infrastructure. 

Astro Hosted consists of three core components for managing Airflow, all hosted on Astronomer's cloud:

- The _Astro control plane_ is Astronomer's interface for managing your Airflow environments in the cloud. It includes the Cloud UI, the Astro CLI, and Cloud API.
- An _Astro cluster_ comprises all the components necessary to host multiple Airflow Deployments, including the network, database, and compute resources.
- A _Deployment_ is an Airflow environment running on Astro. Each Deployment includes all of the core Airflow components, plus additional Astronomer tooling that help you optimize resource usage, observability, and security.

Astro Deployments can securely connect to external data services so that you can place Airflow at the heart of your data ecosystem. 

![Astro Hosted architecture overview](/img/docs/architecture-overview.png)

To learn more about Astro Hybrid architecture and features, see [Astro Hybrid overview](hybrid-overview.md)

## Role based access control (RBAC) architecture

Astro implements role-based access control for Airflow environments. User roles are scoped to both a Workspace and an Organization:

- A [_Workspace_](manage-workspaces.md) is a collection of Deployments that can be accessed by a specific group of users. Workspaces can be used to group Deployments that share a business use case or environment trait.
- An _Organization_ is a collection of Workspaces. 

Each Astro user has a Workspace role in each Workspace they belong to, plus a single Organization role. Users can also belong to [Teams](add-user.md#make-a-team), which apply the same role across a group of users. You can create API keys with specific roles to automate most actions on Astro, such as deploying code or managing users. 

Use the following diagram as a reference for how all of these entities interact with each other in Astro.

![A diagram showing how all Astro RBAC components fit together](/img/docs/rbac-overview.png)