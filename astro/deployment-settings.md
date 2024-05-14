---
sidebar_label: 'Overview'
title: 'Overview'
id: deployment-settings
description: "Manage Deployment settings to customize your Deployment for your use case."
---

After you create an Astro Deployment, you can modify its settings using the Astro UI and Astro CLI to tailor its performance. There are two categories of Deployment configurations: Deployment _details_ and _resources_.

## Deployment details

[Deployment details](deployment-details.md) are high level settings that define how users can interact with the Deployment. These settings include:

- Deployment names and descriptions.
- Deployment contact emails.
- Rules for what types of deploys are allowed.
- Your Deployment's current Workspace.

## Deployment resources

[Deployment resources](deployment-resources.md) let you customize the resource use, infrastructure, and performance of your Deployment. Use these settings to optimize Deployment processing, optimize compute resources and cost, and enable advanced use cases with intensive workloads. The following configuration options are available for customizing your resource use:

- Change the Deployment executor.
- Configure Kubernetes Pod resources.
- Change Scheduler resources.
- Enforce CI/CD Deploys.
- Enable High Availability.
- Customize your Airflow environment using environment variables.

For advanced Deployment resource configurations, see [Manage Airflow executors on Astro](executors-overview.md) and [Configure worker queues](configure-worker-queues.mdx).

:::cli

These documents focuses on configuring Deployments through the Astro UI. To configure Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::

## See also

- [Set environment variables on Astro](environment-variables.md)
- [Authenticate an automation tool to Astro](automation-authentication.md)
- [Manage Deployments as Code](manage-deployments-as-code.md)
