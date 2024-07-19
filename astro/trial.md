---
title: 'Start your Astro trial'
id: trial
sidebar_label: 'Start a trial'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Use this guide to get started with Astro, the best place to run [Apache Airflow®](https://airflow.apache.org).

## Start a trial

Go to [Try Astro](https://www.astronomer.io/try-astro/?referral=docs-what-astro-banner&utm_medium=docs&utm_content=astro-trial&utm_source=body) to activate your free 14-day trial. To create your Astro user account, you'll need to provide a valid email address and create a password.

:::tip

If your company uses Azure, Astronomer recommends installing Astro through the Azure marketplace. The Astro Azure Native ISV service includes the same 14-day trial, and you can automatically invite users from your team through the built-in Azure AD integration. See [Install Astro from the Azure Marketplace](install-azure.md).

:::

## Create an Organization and Workspace

After you've created your Astro user account, you'll be asked to create an Organization and your first Workspace.

An _Organization_ is the highest management level on Astro. An Organization contains _Workspaces_, which are collections of _Deployments_, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels. For more information about Astro's key concepts and components, see [About Astro](astro-architecture.md).

To start your trial, Astronomer recommends using the name of your company as the name of your Organization and naming your first Workspace after your data team or initial business use case with Airflow. You can update these names in the Astro UI after you finish activating your trial.

<img src={require("../static/img/docs/start-trial.png").default} alt="Create an Organization and Workspace" style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

## Next steps

You're now ready to start deploying and running DAGs on Astro. See [Run your first DAG on Astro](run-first-dag.md) to choose a detailed quickstart. You'll create a local Astro project, then push that project to your Astro Deployment. The entire process takes about 5 minutes.

You have 14 days and $300 to spend in credits before your trial ends. See [Manage billing](manage-billing.md) to view how much credit you've used over the course of your trial. See [Pricing](https://www.astronomer.io/pricing/) for a breakdown of how much it costs to run Airflow on Astro.

### Trial resources

An Astro trial provides you a level of access to Deployment resources that Astro considers sufficient to run an initial number of Apache Airflow DAGs and ensure that Astro meets the needs of your Organization.

During a 14-day Astro trial, you can:

- Create one Workspace
- Create up to two Deployments
- Configure **Worker Count** to a maximum of 5 workers per worker queue
- Use A5, A10, or A20 workers

You cannot use high-availability (HA) mode during an Astro trial. To access additional resources or functionality, add a credit card number or other payment method to your Organization.

To learn more about Deployment resources and features available to Astro customers, see [Configure Deployment resources](deployment-resources.md). To learn more about Astro pricing, see [Pricing](https://www.astronomer.io/pricing/).

## After your trial

After your 14-day trial ends, you can no longer access your Workspace from the Astro UI and your Deployments enter [hibernation](deployment-resources.md#hibernate-a-development-deployment) for 30 days. You can still access your user account page and Astronomer support forms. To regain access to your Deployments and Workspace, you must enter a payment method or contact Astronomer to extend your trial. After you enter a payment method, you can wake your Deployments from hibernation and continue to run Apache Airflow DAGs.

All Deployment configurations are preserved during hibernation for 30 days from the last day of your Astro trial. After 30 days, your Deployment and all of its metadata are permanently deleted. When your Deployments are deleted, any code that you deployed to Astro will be lost.

If you need additional time to evaluate Astro, or you need to copy your configuration for future use, you can:

- Contact [sales](https://astronomer.io/contact/) to request a trial extension.
- Run `astro deployment inspect` with the Astro CLI to save your existing Deployment configuration as a JSON or YAML file. See [Astro CLI command reference](cli/astro-deployment-inspect.md).
- Open the Astro UI and [schedule office hours](office-hours.md) with an Astronomer engineer.
