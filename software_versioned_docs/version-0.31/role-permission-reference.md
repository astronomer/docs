---
title: 'Astronomer Software user role and permission reference'
sidebar_label: 'User roles and permissions'
id: role-permission-reference
description: A list of all default permissions for each role on Astronomer Software. 
---

This is where you'll find information about Astronomer Software default user role permissions. To modify these default permissions, see [Customize role permissions](manage-platform-users.md#customize-role-permissions).

## System roles

System roles apply to all Workspaces, users, and Deployments within a single Astronomer Software installation.

### System Viewer

The System Viewer has the following permissions by default:

- `system.airflow.get`: View the Airflow UI for any Deployment
- `system.deployment.variables.get`: View [environment variables](environment-variables.md) for any Deployment
- `system.deployments.get`: View any setting for any Deployment in the Software UI
- `system.invites.get`: View all pending user invites in the **System Admin** tab of the Software UI
- `system.invite.get`: View information for any pending user invite
- `system.monitoring.get`: Access to [Grafana](grafana-metrics.md) and [Kibana](kibana-logging.md) for system-level monitoring
- `system.serviceAccounts.get`: View [service accounts](ci-cd.md#step-1-create-a-service-account) for any Deployment or Workspace
- `system.updates.get`: View the newest platform release version number
- `system.users.get`: View information for any user on the platform, including their email address, the list of Workspaces that user has access to, and their user role
- `system.workspace.get`: View information for any Workspace

### System Editor

The System Editor has the same default permissions as the System Viewer, plus:

- `system.deployment.variables.update`: Modify [environment variables](environment-variables.md) for any Deployment
- `system.iam.update`: Modify [IAM](integrate-iam.md) roles for any Deployment
- `system.serviceAccounts.update`: Modify [service accounts](ci-cd.md#step-1-create-a-service-account) for any Workspace or Deployment
- `deployment.airflow.user`: Airflow [user permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) for all Deployments
- `system.registryBaseImages.push`: Modify base layer Docker images for Airflow

### System Admin

The System Admin has the same default permissions as the System Viewer and System Editor for a given cluster, plus:

- `system.deployments.create`: Create a Deployment on any Workspace
- `system.deployments.update`: Modify any Deployment
- `system.deployments.delete`: Delete any Deployment
- `system.deployments.images.push`: Deploy code to any Deployment
- `system.deployments.logs`: View logs for any Deployment
- `system.deployments.metrics`: View metrics for any Deployment
- `system.invites.get`: View pending user invites in all Workspaces
- `system.serviceAccounts.create`: Create a service account at any level
- `system.serviceAccounts.delete`: Delete any service account
- `system.serviceAccounts.update`: Modify any service account
- `system.teams.remove`: Delete any Team
- `system.user.invite`: Invite a user
- `system.user.delete`: Delete any user
- `system.user.verifyEmail`: Bypass email verification for any user
- `system.workspace.delete`: Delete any Workspace
- `system.workspace.update`: Modify the name or description of any Workspace
- `system.airflow.admin`: Airflow admin permissions on any Deployment, including permission to configure:

    - Pools
    - Configuration
    - Users
    - Connections
    - Variables
    - XComs

## Workspace roles

Workspace roles apply to a single Workspace within a single Astronomer Software installation.

### Workspace Viewer

The Workspace Viewer has the following default permissions for a given Workspace:

- `workspace.config.get`: View the Workspace
- `system.deployments.get`: View all settings and configuration pages of any Deployment
- `workspace.serviceAccounts.get`: View any Deployment or Workspace-level [service account](ci-cd.md#step-1-create-a-service-account)
- `workspace.users.get`: View information for all users with access to the Workspace
- `workspace.teams.get`: View Teams belonging to the Workspace
- `workspace.taskUsage.get`: View task usage in the Workspace

### Workspace Editor

For a given Workspace, the Workspace Editor has the same default permissions as the Workspace Viewer, plus:

- `workspace.config.update`: Modify the Workspace, including Workspace Name, Description, and user access
- `workspace.deployments.create`: Create a Deployment in the Workspace
- `workspace.serviceAccounts.create`: Create a Workspace-level service account
- `workspace.serviceAccounts.update`: Modify a Workspace-level service account
- `workspace.serviceAccounts.delete`: Delete a Workspace-level service account

### Workspace Admin

For a given Workspace, the Workspace Admin has the same default permissions as the Workspace Viewer and Workspace Editor, plus:

- `workspace.invites.get`: View pending user invites for the Workspace
- `workspace.config.delete`: Delete the Workspace
- `workspace.iam.update`: Update [IAM](integrate-iam.md) for the Workspace
- `workspace.teams.getAll`: View all users in Teams belonging to the Workspace
- `workspace.users.getAll`: View all users in the Workspace

In addition, Workspace Admins have Deployment Admin permissions for all Deployments within the Workspace.

## Deployment roles

Deployment roles apply to a single Deployment within a single Astronomer Software installation.

### Deployment Viewer

For a given Deployment, a Deployment Viewer has the following permissions:

- `deployment.airflow.get`: View the Airflow UI
- `deployment.config.get`: View the Deployment's settings
- `deployment.logs.get`: View the Deployment's logs
- `deployment.images.pull`: Access the Deployment's running Docker image
- `deployment.metrics.get`: View the Deployment's **Metrics** tab in the Software UI
- `deployment.serviceAccounts.get`: View any [service account](ci-cd.md#step-1-create-a-service-account) for the Deployment
- `deployment.variables.get`: View the Deployment's [environment variables](environment-variables.md)
- `deployment.users.get`: View the list of users with access to the Deployment
- `deployment.teams.get`: View all Teams belonging to the Deployment
- `deployment.taskUsage.get`: View task usage information for the Deployment

A Deployment Viewer can't push code to a Deployment or modify Deployment configurations. These actions can be completed only by a Deployment Editor or a Deployment Admin.

### Deployment Editor

For a given Deployment, the Deployment Editor has the same default permissions as the Deployment Viewer, plus:

- `deployment.airflow.user`: Airflow [user permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) for all Deployments, including modifying task runs and DAG runs
- `deployment.config.update`: Modify the Deployment's settings
- `deployment.images.push`: Push code to the Deployment using the Astro CLI
- `deployment.images.pull`: Pull image from the Deployment using the Astro CLI
- `deployment.serviceAccounts.create`: Create a Deployment-level service account
- `deployment.serviceAccounts.update`: Modify a Deployment-level service account
- `deployment.serviceAccounts.delete`: Delete a Deployment-level service account
- `deployment.variables.update`: Update the Deployment's [environment variables](environment-variables.md)

A Deployment Editor cannot make changes to certain configurations in the Airflow UI, such as connections and variables. These actions can only be completed by a Deployment Admin.

### Deployment Admin

For a given Deployment, the Deployment Admin has the same default permissions as the Deployment Viewer and the Deployment Editor, plus:

- `deployment.airflow.admin`: Airflow [admin permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#admin), including permission to configure:

    - Pools
    - Configuration
    - Users
    - Connections
    - Variables
    - XComs

- `deployment.config.delete`: Delete the Deployment
- `deployment.userRoles.update`: Update Deployment-level permissions for users within the Deployment
- `deployment.teamRoles.update`: Update Deployment-level permissions for Teams within the Deployment

### Root user

A root user is assigned all available Astronomer Software permissions. There can only be one root user for each Software installation. See [Manage the root user](https://docs.astronomer.io/software/0.31/manage-root-user#log-in-as-the-root-user).
