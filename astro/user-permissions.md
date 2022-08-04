---
sidebar_label: "User permissions"
title: "Manage user permissions in Astro"
id: user-permissions
description: Learn about Astronomer's RBAC system and how to assign roles to users.
---

To better protect your data pipelines and cloud infrastructure, Astro offers role-based access control for Organizations and Workspaces. Each Astro user has a Workspace role in each Workspace they belong to, plus a single Organization role. Role-based access control is not available for Deployments.

## Organization roles

An Organization role grants a user some level of access to an Astro Organization, including all of the Workspaces within that Organization. All users have an Organization role regardless of whether they belong to a Workspace. The following table lists the available Organization roles:

## Organization Roles

An Organization role grants a user some level of access to an Astro Organization, including all of the Workspaces within that Organization. All users have an Organization role regardless of whether they belong to a Workspace. The following Organization roles are available:

| Permission                                                  | **Organization Member** | **Organization Billing Admin** | **Organization Owner** |
| ----------------------------------------------------------- | ----------------------- | ------------------------------ | ---------------------- |
| View Organization details and user membership               | ✔️                       | ✔️                              | ✔️                      |
| View lineage data in the **Lineage** tab                    | ✔️                       | ✔️                              | ✔️                      |
| Update Organization billing information and settings        |                         | ✔️                              | ✔️                      |
| View usage for all Workspaces in the **Usage** tab          |                         | ✔️                              | ✔️                      |
| Workspace Admin permissions to all Workspaces               |                         |                                | ✔️                      |
| Create a new Workspace                                      |                         |                                | ✔️                      |
| Update roles and permissions of existing Organization users |                         |                                | ✔️                      |
| Invite new user to Organization                             |                         |                                | ✔️                      |
| Remove a user from an Organization                          |                         |                                | ✔️                      |

### Update Organization roles

1. In the Cloud UI, go to the **People** tab. This tab is available in the Organization view of the UI.
2. Find the user in the table and click **Edit** next to their entry. The **Members** table lists all users that have been added to a Workspace in your Organization. If you can't find a user, it might be because they haven't been invited to a Workspace or accepted their invite.

## Workspace roles

A Workspace role grants a user some level of access to a specific Workspace. The following table lists the available Workspace roles:

| Permission                               | **Workspace Viewer** | **Workspace Editor** | **Workspace Admin** |
| ---------------------------------------- | -------------------- | -------------------- | ------------------- |
| View Workspace users                     | ✔️                    | ✔️                    | ✔️                   |
| View all Deployments in the Cloud UI     | ✔️                    | ✔️                    | ✔️                   |
| View DAGs in the Airflow UI              | ✔️                    | ✔️                    | ✔️                   |
| View Airflow task logs                   | ✔️                    | ✔️                    | ✔️                   |
| Update Deployment configurations         |                      | ✔️                    | ✔️                   |
| Edit task instance and DAG state         |                      | ✔️                    | ✔️                   |
| Push code to Deployments                 |                      | ✔️                    | ✔️                   |
| Create and Delete Deployments            |                      | ✔️                    | ✔️                   | 
| View Airflow connections and Variables   |                      |                      | ✔️                   |
| Update user roles and permissions        |                      |                      | ✔️                   |
| Update Airflow connections and Variables |                      |                      | ✔️                   |
| Invite users to a Workspace              |                      |                      | ✔️                   |

### Update Workspace roles

Workspace Admins can set user roles on the **Access** tab in the Cloud UI. See [Manage Workspaces](manage-workspaces.md#manage-workspace-users).
