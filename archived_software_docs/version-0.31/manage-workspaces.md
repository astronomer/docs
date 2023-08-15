---
title: 'Manage Workspaces and Deployments on Astronomer'
sidebar_label: 'Create a Workspace'
id: manage-workspaces
description: Manage Astronomer Workspaces and Airflow Deployments via the Software UI.
---

A Workspace is the highest level of organization on Astronomer. From a Workspace, you can manage a collection of Airflow Deployments and a set of users with varying levels of access to those Deployments.

If you're not a member of any Workspaces already, you'll be prompted to create one as soon as you log in to the Software UI. If you already have access to at least 1 Workspace, you can create a new one using the **New Workspace** button in the sidebar of the Software UI.

This guide walks through the best practices for creating and managing Workspaces as a Workspace admin. It's organized by the 4 tabs you can access from a Workspace's menu in the Software UI:

* Deployments
* Settings
* Users
* Service Accounts

![Workspace configuration tab location](/img/software/v0.23-workspace.png)

## Deployments

The most important function of Workspaces is creating and managing access to one or more Airflow Deployments. An Airflow Deployment is an instance of Apache Airflow that consists of a scheduler, webserver, and one or more workers if you're running the Celery or Kubernetes executors.

To create a new Deployment, click the **New Deployment** button in the **Deployments** tab or use the Astro CLI as described in [CLI Quickstart](https://docs.astronomer.io/astro/cli/install-cli). For more information on configuring Deployment settings and resources, read [Configure a Deployment](configure-deployment.md).

The **Deployments** tab also contains information on all of your existing Deployments, including name, executor type, and Deployment status. A blue dot next to a Deployment's name indicates that the Deployment is still spinning up, while a green dot indicates that the Deployment is fully operational:

![Deployment Tab](/img/software/v0.12-deployments.png)

Deployments cannot be used or shared across Workspaces. While you’re free to push local DAGs and code anywhere you wish at any time, there is currently no way to move an existing Airflow Deployment from one Workspace to another once created.

## Settings

You can rename your Workspace or rewrite its description in the **Settings** tab. While these fields have no effect on how tasks are executed, we recommend configuring them to give users an idea of the Workspace's purpose and scope.

## Users

You can see who has access to the Workspace in the **Users** tab.

If you'd like to share access to other members of your organization, invite them to a Workspace you're a part of. Once your team members are part of your Workspace, Deployment admins can grant them varying levels of access to Airflow Deployments within the Workspace. Likewise, Workspace admins can grant them varying levels of access to the entire Workspace.

An exact breakdown of user roles and their respective levels of access can be found in [Manage User Permissions on an Astronomer Workspace](workspace-permissions.md).

In addition, Software system admins can add or remove specific permissions for each type of user role. For more information on this feature, read [Customize Permissions](manage-platform-users.md#customize-permissions).

## Service accounts

Use the **Service Accounts** tab to create a Workspace-level service account. Service accounts generate a permanent API key that you can use automate any action at the Workspace level, such as deploying to your Workspace's Airflow Deployments via a CI/CD tool of your choice.

To automate actions at the Deployment level, create a Deployment service account. For more information on this feature, read [Deploy via CI/CD](ci-cd.md).
