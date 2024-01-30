---
sidebar_label: 'Overview'
title: 'Overview'
id: deployment-settings
description: "Manage Deployment settings to customize your Deployment for your use case."
---

After you create an Astro Deployment, you can modify its settings using the Cloud UI and Astro CLI to tailor its performance. There are two categories of options for configuring your Astro Deployment to best meet your needs: Deployment details and resource configuration.

## Deployment details

Use [Deployment details](deployment-details.md) to manage the administration of your Deployment. This includes includes actions like updating information about your Deployment or transferring it to another Workspace. The following actions allow you to organize and label your Deployments within your Workspace in a way that best fits how your team works with Astro:

- Deployment names and descriptions.
- Deployment contact emails.
- Rules for what types of deploys are allowed.
- Delete a Deployment.

## Deployment resources

You also have [configuration options](deployment-resources.md) that allow you to customize the resource use, infrastructure, and performance of your Deployment. This means you can optimize how your Deployment uses resources, so you can improve the efficiency of your Deployment processing, optimize compute resources and cost, or enable advanced use cases with intensive workloads. The following configuration options enable you to customize your Deployment to get the most out of your resources on Astro:

- Change the Deployment executor.
- Configure Kubernetes Pod resources.
- Change Scheduler resources.
- Enforce CI/CD Deploys.
- Enable High Availability.
- Update your Airflow configuration.

For advanced Deployment resource configurations, see [Manage Airflow executors on Astro](executors-overview.md) and [Configure worker queues](configure-worker-queues.md).

:::cli

This document focuses on configuring Deployments through the Cloud UI. To configure Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::
