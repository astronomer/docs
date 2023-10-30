---
sidebar_label: "User permissions reference"
title: "Astro user permissions reference"
id: user-permissions
description: Learn about Astronomer's RBAC system and how to assign roles to users.
---

To better protect your data pipelines and cloud infrastructure, Astro provides role based access control (RBAC) for Organizations and Workspaces. Each Astro user has a Workspace role in each Workspace they belong to, plus a single Organization role. Users can also belong to [Teams](manage-teams.md), which apply the same Workspace role to a group of users. Role based access control is not available for Deployments.

You can also apply roles to API tokens to limit the scope of their actions in CI/CD and automation pipelines. See [Manage Deployments as code](manage-deployments-as-code.md).

Astro has hierarchical RBAC. Within a given Workspace or Organization, senior roles have their own permissions in addition to the permissions granted to lower roles. For example, a user or API token with Organization Owner permissions inherits Organization Billing Admin and Organization Member permissions because those roles are lower in the hierarchy.

The Astro role hierarchies in order of inheritance are:

- Organization Owner > Organization Billing Admin > Organization Member
- Workspace Owner > Workspace Operator > Workspace Author > Workspace Member

Additionally, Organization Owners inherit Workspace Owner permissions for all Workspaces in the Organization.

## Organization roles

An Organization role grants a user or API token some level of access to an Astro Organization, including all of the Workspaces within that Organization. All users have an Organization role regardless of whether they belong to a Workspace whereas an API token's access is based on it's scope. The following table lists the available Organization roles:

| Permission                                                       | **Organization Member** | **Organization Billing Admin** | **Organization Owner** |
| ---------------------------------------------------------------- | ----------------------- | ------------------------------ | ---------------------- |
| View Organization details and user membership                    | ✔️                      | ✔️                             | ✔️                     |
| View lineage metadata in the **Lineage** tab                     | ✔️                      | ✔️                             | ✔️                     |
| Update Organization billing information and settings             |                         | ✔️                             | ✔️                     |
| View usage for all Workspaces in the **Usage** tab               |                         | ✔️                             | ✔️                     |
| Create a new Workspace                                           |                         |                                | ✔️                     |
| Workspace Owner permissions to all Workspaces                    |                         |                                | ✔️                     |
| Update roles and permissions of existing Organization users      |                         |                                | ✔️                     |
| Invite a new user to an Organization                             |                         |                                | ✔️                     |
| Remove a user from an Organization                               |                         |                                | ✔️                     |
| Create, update, and delete Organization API tokens               |                         |                                | ✔️                     |
| Access, regenerate, and delete single sign-on (SSO) bypass links |                         |                                | ✔️                     |
| Create, update, and delete a Team                                |                         |                                | ✔️                     |

To manage users in an Organization, see [Manage Organization users](manage-organization-users.md). To manage the Organization permissions of your API tokens, see [Organization API tokens](organization-api-tokens.md).

## Workspace roles

A Workspace role grants a user or API token some level of access to a specific Workspace. If a user or API token has some level of access to a Workspace, that access applies to all Deployments in the Workspace.

- A **Workspace Member** has the least permissions in a Workspace and can only view the most basic details about Deployments and DAGs. Give a user this role if they need to be able to monitor a DAG run or view Deployment health, but they shouldn't make any changes to a Deployment themselves.
- A **Workspace Author** has all of the same permissions as a Workspace Member, plus the ability to update DAG code and run DAGs in the Airflow UI, plus limited permissions to configure Deployment-level observability features such as Astro alerts. Give a user this role if they are primarily DAG developers and don't need to manage the environments their DAGs run in.
- A **Workspace Operator** has all the same permissions as a Workspace Author, plus the ability to manage Deployment-level configurations, such as environment variables. Give a user this role if they need to manage the environments that DAGs run in.
- A **Workspace Owner** has all the same permissions as a Workspace Operator, plus the ability to manage user membership in the Workspace. Give a user this role if they need to administrate membership to the Workspace.

The following table lists the specific permissions that each Workspace role has:

| Permission                                                                  | **Workspace Member** | **Workspace Author** | **Workspace Operator** | **Workspace Owner** |
| --------------------------------------------------------------------------- | -------------------- | -------------------- | ---------------------- | ------------------- |
| View Workspace users                                                        | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View all Deployments in the Cloud UI                                        | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View DAGs in the Airflow UI                                                 | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View Airflow task logs                                                      | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View Airflow datasets                                                       | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View Astro Cloud IDE projects                                               | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| View Astro alerts                                                           | ✔️                   | ✔️                   | ✔️                     | ✔️                  |
| Manually trigger DAG and task runs                                          |                      | ✔️                   | ✔️                     | ✔️                  |
| Pause or unpause a DAG                                                      |                      | ✔️                   | ✔️                     | ✔️                  |
| Clear/mark a task run or DAG run                                            |                      | ✔️                   | ✔️                     | ✔️                  |
| Push code to Deployments or Astro Cloud IDE projects                        |                      | ✔️                   | ✔️                     | ✔️                  |
| Create, update, and delete Astro Cloud IDE projects                         |                      | ✔️                   | ✔️                     | ✔️                  |
| Create, update, and delete Astro alerts                                     |                      | ✔️                   | ✔️                     | ✔️                  |
| View Airflow connections, variables, plugins, providers, pools, and XComs   |                      | ✔️                   | ✔️                     | ✔️                  |
| Update Airflow connections, variables, plugins, providers, pools, and XComs |                      |                      | ✔️                     | ✔️                  |
| Update Deployment configurations                                            |                      |                      | ✔️                     | ✔️                  |
| Create and Delete Deployments                                               |                      |                      | ✔️                     | ✔️                  |
| Create, Update and Delete Deployment environment variables                  |                      |                      | ✔️                     | ✔️                  |
| View the **Cluster Activity** tab in the Airflow UI                         |                      |                      |                        | ✔️                  |
| Update user roles and permissions                                           |                      |                      |                        | ✔️                  |
| Invite users to a Workspace                                                 |                      |                      |                        | ✔️                  |
| Assign Teams to or remove from Workspaces                                   |                      |                      |                        | ✔️                  |
| Create, update, and delete Deployment and Workspace API tokens              |                      |                      |                        | ✔️                  |

To manage a user's Workspace permissions, see [Manage Worksapce users](manage-workspace-users.md#add-a-user-to-a-workspace).

## Relationship between user roles and Team roles

There are two ways to define a user's role in a Workspace:

- Define the individual user role when you [add a user](manage-workspace-users.md#add-a-user-to-a-workspace) to a Workspace.
- Assign a Workspace role to a [Team](manage-teams.md#add-a-team-to-a-workspace) and add the user to the Team.

If a user has permissions to a Workspace both as an individual and as a member of a Team, then Astronomer recognizes the more privileged role.

For example, if a user belongs to a Workspace as a **Workspace Member**, but also belongs to a Team in the Workspace with **Workspace Owner** privileges, then the user has **Workspace Owner** privileges in the Workspace.
