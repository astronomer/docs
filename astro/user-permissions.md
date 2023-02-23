---
sidebar_label: "User permissions"
title: "Manage Astro user permissions"
id: user-permissions
description: Learn about Astronomer's RBAC system and how to assign roles to users.
---

To better protect your data pipelines and cloud infrastructure, Astro provides role based access control for Organizations and Workspaces. Each Astro user has a Workspace role in each Workspace they belong to, plus a single Organization role. Role based access control is not available for Deployments.

Astro has hierarchical role based access control. Within a given Workspace or Organization, users with senior roles have their own permissions in addition to the permissions granted to lower roles. For example, users with Organization Owner permissions inherit Organization Billing Admin and Organization Member permissions because the roles are lower in the hierarchy. 

The Astro role hierarchies in order of inheritance are: 

- Organization Owner > Organization Billing Admin > Organization Member 
- Workspace Admin > Workspace Editor > Workspace Viewer

Users with Organization Owner permissions also inherit Workspace Admin permissions on all Workspaces.

## Organization roles

An Organization role grants a user some level of access to an Astro Organization, including all of the Workspaces within that Organization. All users have an Organization role regardless of whether they belong to a Workspace. The following table lists the available Organization roles:

| Permission                                                       | **Organization Member** | **Organization Billing Admin** | **Organization Owner** |
| ---------------------------------------------------------------- | ----------------------- | ------------------------------ | ---------------------- |
| View Organization details and user membership                    | ✔️                       | ✔️                              | ✔️                      |
| View lineage data in the **Lineage** tab                         | ✔️                       | ✔️                              | ✔️                      |
| Create a new Workspace                                           | ✔️                       | ✔️                              | ✔️                      |
| Update Organization billing information and settings             |                         | ✔️                              | ✔️                      |
| View usage for all Workspaces in the **Usage** tab               |                         | ✔️                              | ✔️                      |
| Workspace Admin permissions to all Workspaces                    |                         |                                | ✔️                      |
| Update roles and permissions of existing Organization users      |                         |                                | ✔️                      |
| Invite a new user to an Organization                             |                         |                                | ✔️                      |
| Remove a user from an Organization                               |                         |                                | ✔️                      |
| Access, regenerate, and delete single sign-on (SSO) bypass links |                         |                                | ✔️                      |

To update user Organization roles, see [Manage users](add-user.md).

## Workspace roles

A Workspace role grants a user some level of access to a specific Workspace. The following table lists the available Workspace roles:

| Permission                                          | **Workspace Viewer** | **Workspace Editor** | **Workspace Admin** |
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
| Create, Update and Delete API Keys                  |                      |                      | ✔️                   |
| View Airflow connections and Variables              |                      |                      | ✔️                   |
| Update user roles and permissions                   |                      |                      | ✔️                   |
| Update Airflow connections and Variables            |                      |                      | ✔️                   |
| Invite users to a Workspace                         |                      |                      | ✔️                   |

To update user Workspace roles, see [Manage users](add-user.md).
