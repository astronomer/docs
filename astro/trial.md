---
title: 'Start your Astro trial'
id: trial
sidebar_label: 'Start a trial'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Use this guide to get started with Astro, the best place to run Apache Airflow.

## Start a trial

Go to [Try Astro](https://www.astronomer.io/try-astro/) to activate your free 14-day trial. To create your Astro user account, you'll need to provide a valid email address and create a password.

## Create an Organization and Workspace

After you've created your Astro user account, you'll be asked to create an Organization and your first Workspace. 

An _Organization_ is the highest management level on Astro. An Organization contains _Workspaces_, which are collections of _Deployments_, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels.

To start your trial, Astronomer recommends using the name of your company as the name of your Organization and naming your first Workspace after your data team or initial business use case with Airflow. You can update these names in the Cloud UI after you finish activating your trial. 

## Next steps

You're now ready to start deploying and running DAGs on Astro. See [Run your first DAG on Astro](create-first-dag.md) for a detailed quickstart. You'll create a local Astro project, then push that project to your Astro Deployment. The entire process takes about 5 minutes. 

You have 14 days and $300 to spend in credits before your trial ends. See [Manage billing](manage-billing.md) to view how much credit you've used over the course of your trial. See [Pricing](https://www.astronomer.io/pricing/) for a breakdown of how much it costs to run Airflow on Astro.

## After your trial

After your 14-day trial ends, you can no longer access your Deployments and Workspaces from the Cloud UI. You can still access your user account page and Astronomer support forms.

After your trial ends, all Deployments are automatically deleted. If you created a dedicated cluster, it is also deleted. Any code that you deployed to Astro will be lost. If you need additional time to evaluate Astro, or you need to copy your configuration for future use, you can:

- Contact [sales](https://astronomer.io/contact/) to request a trial extension.
- Run `astro deployment inspect` with the Astro CLI to save your existing Deployment configuration as a JSON or YAML file. See [Astro CLI command reference](cli/astro-deployment-inspect.md).
- Open the Cloud UI and schedule office hours with an Astronomer engineer.