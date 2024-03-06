---
title: "Create and assign custom Deployment roles"
sidebar_label: Custom Deployment roles 
id: customize-deployment-roles
description: Customize your users' permissions for Airflow environments on Astro.
---

:::privatepreview
:::

:::info

This feature is available only in the Enterprise tier.

:::

A user entity's Deployment role determines their level of access to a specific Deployment in a Workspace. User entities with [Workspace Member permissions](user-permissions.md#workspace-roles) or higher have some level of access to all Deployments in a Workspace, and these permissions can be increased using Deployment roles.

There are some circumstances where users should have limited access to Deployments in a Workspace. For example, all users might need full access to a development Deployment, but only administrative users need access to a production Deployment.

In situations where you need fine-grained Deployment access, you can create custom Deployment roles and assign them to users with Workspace Accessor or Workspace Member roles. When you grant a user a Deployment role, they have a specific level of access to a specific Deployment. Use custom Deployment roles to enable users to collaborate in the same Workspace with only the minimum permissions they require.

## Prerequisites

- Organization Owner permissions to create, update, and delete custom roles.
- Workspace Owner permissions or Deployment Admin permissions to assign and change Deployment roles for users.

## Create a custom Deployment role

You manage and create custom Deployment roles at the Organization level. After you create a custom Deployment role, you can assign users, teams, and Deployment API tokens the role from any Deployment in the Organization. 

Deployment roles are additive, meaning that a user with multiple Deployment roles has all of the permissions of each Deployment role as well as their Workspace role. For example, if a user belongs to a Team with a custom Deployment role that includes permissions to edit Airflow variables, and they also have a personal custom Deployment role that includes permissions to edit connections, then the user has permissions to edit both Airflow variables and connections in the Deployment. 

1. In the Astro UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Access Management**, then click **Roles**.

3. Click **Custom** then click **+ Add Role**.

4. In the window that appears, give your new role a **Name** and **Description**.

5. In the **Permissions** table, check the boxes of all permissions that you want the new role to have. See [Deployment role permission reference](deployment-role-reference.md) for more information about each available permission. 

    :::tip

    Use the dropdown menu above the permissions table to automatically load the permissions of a templated role or an existing custom role as the basis for your new role. See [Deployment role templates](#deployment-role-templates) for more information about the available default templates.

    :::

6. Click **Create role**.

Your role is now available to assign at the Deployment level. See [Assign users and Teams to Deployments](#assign-users-and-teams-to-deployments) or [Create Deployment API tokens with custom Deployment roles](#create-deployment-api-tokens-with-custom-deployment-roles) for next steps.

### Deployment role templates

Astro provides a few Deployment role templates that you can use as the basis for custom roles. These roles are not hard-coded and exist only as templates. 

- **Deployment Viewer**: This is similar to the [Airflow Viewer](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#viewer) viewer role. It grants the user entity view-only permissions for the Airflow UI excluding the **Admin** tab.
- **Deployment Author**: This is similar to the [Airflow User](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) role. It grants the user entity permissions to deploy code and manage DAG and task runs from the Airflow UI.
- **Deployment Operator**: This is similar to the [Airflow Op](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#op) role. It grants the user entity permissions to update Deployment API tokens and Airflow objects from both the Airflow UI and the Astro UI.

## Assign users and Teams to Deployments

Using Deployment roles, you can add users and Teams directly to Deployments without first assigning them to a Workspace. If they don't already belong to the Workspace, Astro grants them the _Workspace Accessor_ role. A Workspace Accessor only has permissions to access their assigned Deployments within the Workspace. All other Deployments and Workspace settings are hidden.

1. In the Astro UI, open the Deployment where you want to assign the user entity.
2. Click **Access**, then click **Users** or **Teams** depending on what kind of user entity you want to assign to the Deployment.
3. Click **+ User**/ **+ Team**.
4. In the window that appears, select the user entity you want to add, then select the role they will have in the Deployment.
5. Click **Add User**/ **Add Team**.