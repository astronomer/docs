---
sidebar_label: "User permissions reference"
title: "Astro user permissions reference"
id: user-permissions
description: Learn about Astronomer's RBAC system and how to assign roles to users.
---

To better protect your data pipelines and cloud infrastructure, Astro provides role based access control (RBAC) for Organizations and Workspaces. Each Astro user has a Workspace role in each Workspace they belong to, plus a single Organization role. Users can also belong to [Teams](add-user.md#make-a-team), which apply the same Workspace role to a group of users. Role based access control is not available for Deployments.

You can also apply roles to API tokens to limit the scope of their actions in CI/CD and automation pipelines. See [Manage Deployments as code](manage-deployments-as-code.md).

Astro has hierarchical RBAC. Within a given Workspace or Organization, senior roles have their own permissions in addition to the permissions granted to lower roles. For example, a user or API token with Organization Owner permissions inherits Organization Billing Admin and Organization Member permissions because those roles are lower in the hierarchy. 

The Astro role hierarchies in order of inheritance are: 

- Organization Owner > Organization Billing Admin > Organization Member 
- Workspace Admin > Workspace Editor > Workspace Member

Additionally, Organization Owners inherit Workspace Admin permissions for all Workspaces in the Organization.

## Organization roles

An Organization role grants a user or API token some level of access to an Astro Organization, including all of the Workspaces within that Organization. All users have an Organization role regardless of whether they belong to a Workspace whereas an API token's access is based on it's scope. The following table lists the available Organization roles:

| Permission                                                       | **Organization Member** | **Organization Billing Admin** | **Organization Owner** |
| ---------------------------------------------------------------- | ----------------------- | ------------------------------ | ---------------------- |
| View Organization details and user membership                    | ✔️                       | ✔️                              | ✔️                      |
| View lineage metadata in the **Lineage** tab                     | ✔️                       | ✔️                              | ✔️                      |
| Update Organization billing information and settings             |                         | ✔️                              | ✔️                      |
| View usage for all Workspaces in the **Usage** tab               |                         | ✔️                              | ✔️                      |
| Create a new Workspace                                           |                         |                                | ✔️                      |
| Workspace Admin permissions to all Workspaces                    |                         |                                | ✔️                      |
| Update roles and permissions of existing Organization users      |                         |                                | ✔️                      |
| Invite a new user to an Organization                             |                         |                                | ✔️                      |
| Remove a user from an Organization                               |                         |                                | ✔️                      |
| Create, update, and delete Organization API tokens               |                         |                                | ✔️                      |
| Access, regenerate, and delete single sign-on (SSO) bypass links |                         |                                | ✔️                      |
| Create, update, and delete a Team                                |                         |                                | ✔️                      |

To manage users in a organization, see [Manage users](add-user.md). To manage the Organization permissions of your API tokens, see [Organization API tokens](organization-api-tokens.md).

## Workspace roles

A Workspace role grants a user or API token some level of access to a specific Workspace. All Deployments in a Workspace will be accessible to the user or API token based on it's Workspace role. The following table lists the available Workspace roles:

| Permission                                          | **Workspace Member** | **Workspace Editor** | **Workspace Admin** |
| --------------------------------------------------- | -------------------- | -------------------- | ------------------- |
| View Workspace users                                | ✔️                    | ✔️                    | ✔️                   |
| View all Deployments in the Cloud UI                | ✔️                    | ✔️                    | ✔️                   |
| View DAGs in the Airflow UI                         | ✔️                    | ✔️                    | ✔️                   |
| View Airflow task logs                              | ✔️                    | ✔️                    | ✔️                   |
| View Astro Cloud IDE projects                       | ✔️                    | ✔️                    | ✔️                   |
| Update Deployment configurations                    |                      | ✔️                    | ✔️                   |
| Manually trigger DAG and task runs                  |                      | ✔️                    | ✔️                   |
| Pause or unpause a DAG                              |                      | ✔️                    | ✔️                   |
| Clear/mark a task instance or DAG run               |                      | ✔️                    | ✔️                   |
| Push code to Deployments                            |                      | ✔️                    | ✔️                   |
| Create and Delete Deployments                       |                      | ✔️                    | ✔️                   |
| Create, Update and Delete Environment Variables     |                      | ✔️                    | ✔️                   |
| Create, update, and delete Astro Cloud IDE projects |                      | ✔️                    | ✔️                   |
| View Airflow connections and Variables              |                      |                      | ✔️                   |
| Update Airflow connections and Variables            |                      |                      | ✔️                   |
| Create, Update, and Delete API Keys                 |                      |                      | ✔️                   |
| Update user roles and permissions                   |                      |                      | ✔️                   |
| Invite users to a Workspace                         |                      |                      | ✔️                   |
| Assign Teams to or remove from Workspaces           |                      |                      | ✔️                   |
| Create, update and delete Workspace API tokens      |                      |                      | ✔️                   |

To manage a user's Workspace permissions, see [Manage users](add-user.md#add-a-user-to-a-workspace).

## User roles and Team roles

There are two ways to define a user's role in a Workspace:

- Define the individual user role when you [add a user](/astro/add-user.md#add-a-user-to-a-workspace) to a Workspace.
- Assign a Workspace role to a [Team](/astro/add-user.md#add-a-team-to-a-workspace).

If a user has permissions to a Workspace both as an individual and as a member of a Team, then Astronomer recognizes the more privileged role.

For example, if a user belongs to a Workspace as a **Workspace Member**, but also belongs to a Team in the Workspace with **Workspace Admin** privileges, then the user has **Workspace Admin** privileges in the Workspace.