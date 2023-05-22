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

An **Organization** is the highest management level on Astro. An Organization contains **Workspaces**, which are collections of Deployments, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels.

To start your trial, Astronomer recommends using the name of your company as the name of your Organization and naming your first Workspace after your data team or initial business use case with Airflow. You can update these names in the Cloud UI after you finish activating your trial. 

## Next steps

You're now ready to start deploying and running DAGs on Astro. See [Run your first DAG on Astro](create-first-dag.md) for a detailed quickstart. You'll create a local Astro project, then push that project to your Astro Deployment. The entire process takes about 5 minutes. 


## Trial limitations

Astro trials have some limitations that aren't present in the paid product:

- You can only create Deployments in standard clusters, which do not support VPC Peer network configurations for access to your internal data sources
- You can only have up to two Deployments at any given time.
- For each of your Deployments, you have the following usage limits on executors:
    - Celery executor: 4vCPU and 8G RAM.
    - Kubernetes executor: 12vCPU and 24G RAM.
- You can only configure the `default` worker queue, and you can only have a maximum worker count of two.
   
## After your trial

After your 14-day trial ends, you can no longer access your Deployments and Workspaces from the Cloud UI. You can still access your user account page and Astronomer support forms. Any DAGs you deployed will continue to run for an additional 7-day grace period.

After the 7-day grace period, your cluster and all Deployments within it are automatically deleted. Any code that you deployed to Astro will be lost. If you need additional time to evaluate Astro, or you need to copy your configuration for future use, you can:

- Schedule a call with your point of contact from Astronomer.
- Go to the Cloud UI and schedule a 15 minute call with an Astronomer engineer. This option is available only after your 14-day trial ends.
- Contact [Astronomer support](https://cloud.astronomer.io/support).
