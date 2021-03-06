---
title: "Manage Workspaces and Deployments on Astronomer"
navTitle: "Create a Workspace"
description: "Manage Astronomer Workspaces and Airflow Deployments via the Astronomer UI."
---

## Overview

A Workspace is the highest level of organization on Astronomer. From a Workspace, you can manage a collection of Airflow Deployments and a set of users with varying levels of access to those Deployments.

If you're not a member of any Workspaces already, you'll be prompted to create one as soon as you log in to the Astronomer UI. If you already have access to at least 1 Workspace, you can create a new one using the **New Workspace** button in the sidebar of the Astronomer UI.

This guide walks through the best practices for creating and managing Workspaces as a Workspace admin. It's organized by the 5 tabs you can access from a Workspace's menu in the Astronomer UI:

* Deployments
* Settings
* Users
* Service Accounts
* Billing

![Workspace configuration tab location](https://assets2.astronomer.io/main/docs/astronomer-ui/cloud-workspace.png)

## Deployments

The most important function of Workspaces is creating and managing access to one or more Airflow Deployments. An Airflow Deployment is an instance of Apache Airflow that consists of a Scheduler, Webserver, and one or more Workers if you're running the Celery or Kubernetes Executors.

To create a new Deployment, click the **New Deployment** button in the **Deployments** tab or use the Astronomer CLI as described in [CLI Quickstart](/docs/cloud/stable/develop/cli-quickstart/). For more information on configuring Deployment settings and resources, read [Configure a Deployment](https://www.astronomer.io/docs/cloud/v0.23/deploy/configure-deployment).

The **Deployments** tab also contains information on all of your existing Deployments, including name, Executor type, and Deployment status. A blue dot next to a Deployment's name indicates that the Deployment is still spinning up, while a green dot indicates that the Deployment is fully operational:

![Deployment Tab](https://assets2.astronomer.io/main/docs/astronomer-ui/v0.12-deployments.png)

Deployments cannot be used or shared across Workspaces. While you???re free to push local DAGs and code anywhere you wish at any time, there is currently no way to move an existing Airflow Deployment from one Workspace to another once created.

## Settings

Use the **Settings** tab to rename your Workspace or rewrite its description. While these fields have no effect on how tasks are executed, we recommend configuring them to give users an idea of the Workspace's purpose and scope.

## Users

You can see who has access to the Workspace in the **Users** tab.

If you'd like to share access to other members of your organization, invite them to a Workspace you're a part of. Once your team members are part of your Workspace, Deployment admins can grant them varying levels of access to Airflow Deployments within the Workspace. Likewise, Workspace admins can grant them varying levels of access to the entire Workspace.

An exact breakdown of user roles and their respective levels of access can be found in [Manage User Permissions on an Astronomer Workspace](/docs/cloud/stable/manage-astronomer/workspace-permissions/).

In addition, Enterprise system admins can add or remove specific permissions for each type of user role. For more information on this feature, read [Customize Permissions](https://www.astronomer.io/docs/cloud/stable/manage-astronomer/manage-platform-users#customize-permissions).

## Service Accounts

Use the **Service Accounts** tab to create Service Accounts. Service Accounts can push code and deploy to your Workspace's Airflow Deployments via the CI/CD tool of your choice.

A Service Account created at the Workspace level can deploy to multiple Deployments with one code push, whereas a Service Account at the Deployment level can deploy only to a single Deployment. For more information on this feature, read [Deploy via CI/CD](https://www.astronomer.io/docs/cloud/stable/deploy/ci-cd).

## Billing

Billing for Astronomer Cloud is managed at the Workspace level. Use the **Billing** tab to add or configure your team's payment method. You can specify a billable name, a billing email, and a credit card to use for future payments. The email address you specify here will receive a monthly invoice for resource usage associated with all Airflow Deployments within your Workspace. If you'd like to receive invoices at more than one email address, reach out to [Astronomer Support](https://support.astronomer.io). For more information on billing, read [Cloud Pricing](https://www.astronomer.io/docs/cloud/stable/resources/pricing).
