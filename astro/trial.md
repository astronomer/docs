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

After Astronomer creates your cluster, you're ready to start deploying and running DAGs on Astro. Complete the following tasks to get your first DAG up and running on Astro: 

1. [Create a Deployment](create-deployment.md). A Deployment is an Astro Runtime environment that is powered by the core components of Apache Airflow and where you can run DAGs.
2. [Install the Astro CLI](cli/install-cli.md). The Astro CLI is an open source command line interface for developing Airflow DAGs on your local machine and deploying them to Astro
3. [Run your first DAG on Astro](create-first-dag.md). You'll create a local Astro project, then push that project to your Astro Deployment. The entire process takes about 5 minutes. 

## Trial limitations

Astro trials have some limitations that aren't present in the paid product:

- You can only create Deployments in standard clusters, which are clusters that are shared with other Astro users. 
- You can only have up to two Deployments at any given time.
- You can only configure the `default` worker queue, and you can only have a maximum worker count of two.
   
## After your trial

After your 14-day trial ends, you can no longer access your Deployments and Workspaces from the Cloud UI. You can still access your user account page and Astronomer support forms. Any DAGs you deployed will continue to run for an additional 7-day grace period.

After the 7-day grace period, your cluster and all Deployments within it are automatically deleted. Any code that you deployed to Astro will be lost. If you need additional time to evaluate Astro, or you need to copy your configuration for future use, you can:

- Schedule a call with your point of contact from Astronomer.
- Go to the Cloud UI and schedule a 15 minute call with an Astronomer engineer. This option is available only after your 14-day trial ends.
- Contact [Astronomer support](https://cloud.astronomer.io/support).
