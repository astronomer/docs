---
title: "Create and assign custom roles for Astro Deployments"
id: customize-deployment-roles
unlisted: true
description: Customize your users' permissions for Airflow environments on Astro.
---

:::caution

This feature is in [Private Preview](feature-previews.md).

:::

A user entity's Deployment role determines their level of access to a specific Deployment in a Workspace. User entities with Workspace Member permissions or higher have some level of access to all Deployments in a Workspace, and these permissions can be heightened using Deployment roles.

There are some circumstances where users should have limited access to Deployments in a Workspace. For example, all users might need full access to a development Deployment, but only administrative users should have access to a production Deployment.

In situations where you need fine-grained Deployment access, you can create custom Deployment roles and assign them to users with Workspace Accessor or Workspace Member roles. When you grant a user a Deployment role, they have a specific level of access to a specific Deployment. Use custom Deployment roles to enable users to collaborate in the same Workspace only with the minimum permissions they require.

## Prerequisites

- Organization Owner permissions

## Create a custom Deployment role

Custom Deployment roles are created and managed at the Organization level. After you create a custom Deployment role, you can assign users the role from any Deployment in the Organization. 

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
   
2. Go to **Access Management**, then click **Roles**.

3. Click **Custom** then click **+ Add Role**.

4. In the window that appears, give your new role a **Name** and **Description**.

5. In the **Permissions** table, check the boxes of all permissions that you want the new role to have. See [Deployment role permission reference](deployment-role-reference.md) for more information about each available permission. 

    :::tip

    Use the dropdown menu above the permissions table to automatically load the permissions of a templated role or an existing custom role as the basis for your new role. See [Deployment role templates](#deployment-role-templates) for more information about the available default templates.

    :::

6. Click **Create role**.

Your role is now available to assign at the Deployment level. See [Assign users, Teams, and API tokens to Deployments](#assign-users-teams-and-api-tokens-to-deployments).

### Deployment role templates

Astro provides a few Deployment role templates that you can use as the basis for custom roles. These roles are not hard-coded and exist only as templates. 

- **Deployment Viewer**: This is similar to the [Airflow viewer](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#viewer) viewer role. It grants the user entity view-only permissions for the Airflow UI excluding the **Admin** tab.
- **Deployment Author**: This is similar to the [Airflow user](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) role. It grants the user entity permissions to deploy code and manage DAG and task runs from the Airflow UI.
- **Deployment Operator**: This is similar to the [Airflow Op](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#op) role. It grants the user entity permissions to update Deployment API tokens and Airflow objects from both the Airflow UI and the Cloud UI.

## Assign users and Teams to Deployments

Before you assign a custom Deployment role to a user or Team, ensure that the user entity doesn't have Workspace Admin or Workspace Member permissions. Otherwise, the user entity will already have all available Deployment permissions and the Deployment role will have no effect.

1. In the Cloud UI, open the Deployment where you want to assign the user entity.
2. Click **Access**, then click **Users** or **Teams** depending on what kind of user entity you want to assign to the Deployment.
3. Click **+ User**/ **+ Team**.
4. In the window that appears, select the user entity you want to add, then select the role they will have in the Deployment.
5. Click **Add User**/ **Add Team**.

## Create Deployment API tokens with custom Deployment roles

By default, Deployment API tokens have Deployment Admin permissions. You can alternatively create or update Deployment API tokens to use any of your configured custom Deployment roles. 

1. In the Cloud UI, open the Deployment where you want to assign the user entity.
2. Click **Access**, then click **API Tokens**.
3. Click **+ Deployment API Token**.
4. In the window that appears, select give your new Deployment API key a name, custom role, and expiration date.
5. Click **Add User**/ **Add Team**.