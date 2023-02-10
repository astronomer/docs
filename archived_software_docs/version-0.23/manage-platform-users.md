---
title: 'Manage Users on Astronomer Software'
sidebar_label: 'Platform User Management'
id: manage-platform-users
description: Add and customize user permissions on Astronomer Software.
---

## Overview

In addition to Workspace-level [role-based access control (RBAC) functionality](workspace-permissions.md) core to our platform, Astronomer Software allows teams to customize *how* they want users to create accounts on Astronomer and what they're able to do on the platform - both on Astronomer and Airflow.

Read below for a high-level overview of user management and guidelines around public signups, role customization and adding System Admins. For a list of each role's specific permissions, read [Reference: System Permissions](manage-platform-users.md#reference-system-permissions).

## Add Users to Astronomer

When Astronomer Software is first deployed, the first user to log in is granted "System Admin" permissions by default (more on that below). From there, a user is created on Astronomer Software by:

- Invitation to a Workspace by a Workspace Admin
- Invitation to Astronomer by a System Admin
- Signing up via the Software UI without an invitation (requires "Public Signups")

On Astronomer, administrators have the option to either open the platform to public signups or limit account creation to users invited by others.

> **Note:** New users appear under a System Admin's **Users** tab only after the new user has successfully logged in for the first time.

> **Note:** You can bypass the email verification process for new users through a Houston API mutation. For the format of this mutation, see [Sample Mutations](houston-api.md#sample-mutations).

### Enable Public Signups

As noted above, public signups allow any user with access to the platform URL (the Software UI) to create an account. If public signups are disabled, users that try to access Astronomer without an invitation from another user will be met with an error.

In cases where SMTP credentials are difficult to acquire, enabling this flag might facilitate initial setup, as disabling public signups requires that a user accept an email invitation. Public signups are a configuration available in Astronomer's Houston API and can be enabled in the `config.yaml` file of your Helm chart.

To enable public signups, add the following yaml snippet to your `config.yaml` file:

```
astronomer:
  houston:
    config:
      publicSignups: true
      emailConfirmation: false # If you wish to also disable other SMTP-dependent features
```

An example `config.yaml` file would look like:

```
global:
  baseDomain: mybasedomain
  tlsSecret: astronomer-tls
nginx:
  loadBalancerIP: 0.0.0.0
  preserveSourceIP: true

astronomer:
  houston:
    config:
      publicSignups: true
      emailConfirmation: false

```

Then, push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).

### User Roles on Astronomer

Once on the platform, administrators can customize permissions across teams. On Astronomer, users can be assigned roles at 2 levels:

1. Workspace Level (Viewer, Editor, Admin)
2. System Level (Viewer, Editor, Admin)

Workspace roles apply to all Airflow Deployments within a single Workspace, whereas System Roles apply to *all* Workspaces across a single cluster. For a detailed breakdown of the 3 Workspace-level roles on Astronomer (Viewer, Editor and Admin), read [Manage User Permissions on an Astronomer Workspace](workspace-permissions.md).

## Customize Permissions

Permissions are defined on Astronomer as `scope.entity.action`, where:

- `scope`: The layer of our application to which the permission applies
- `entity`: The object or role being operated on
- `action`: The verb describing the operation being performed on the `entity`

For example, the `deployment.serviceAccounts.create` permission translates to the ability for a user to create a Deployment-level Service Account. To view all available platform permissions and default role configurations, see [Reference: System Permissions](manage-platform-users.md#reference-system-permissions).

> **Note:** Higher-level roles by default encompass permissions that are found and explicitly defined in lower-level roles, both at the Workspace and System levels. For example, a `SYSTEM_ADMIN` encompasses all permission listed under its role _as well as_ all permissions listed under the `SYSTEM_EDITOR` and `SYSTEM_VIEWER` roles.

To customize permissions, follow the steps below.

### Identify a Permission Change

First, take a look at the default roles and permissions in the [Houston API configuration](https://github.com/astronomer/docs/tree/main/software_configs/0.23/default.yaml) and identify two things:

1. What role do you want to configure? (e.g. `DEPLOYMENT_EDITOR`)
2. What permission(s) would you like to add to or remove from that role? (e.g. `deployment.images.push`)

For example, you might want to block a `DEPLOYMENT_EDITOR` (and therefore `WORKSPACE_EDITOR`) from deploying code to all Airflow Deployments within a Workspace and instead limit that action to users assigned the `DEPLOYMENT_ADMIN` role.

### Limit Workspace Creation

Unless otherwise configured, a user who creates a Workspace on Astronomer is automatically granted the `WORKSPACE_ADMIN` role and is thus able to create an unlimited number of Airflow Deployments within that Workspace. For teams looking to more strictly control resources, our platform supports limiting the Workspace creation function via a `USER` role.

Astronomer ships with a `USER` role that is synthetically bound to _all_ users within a single cluster. By default, this role includes the `system.workspace.create` permission.

If you're an administrator on Astronomer who wants to limit Workspace Creation, you can:

- Remove the `system.workspace.create` permission from the `USER` role
- Attach it to a separate role of your choice

If you'd like to reserve the ability to create a Workspace _only_ to System Admins who otherwise manage cluster-level resources and costs, you might limit that permission to the `SYSTEM_ADMIN` role on the platform.

To configure and apply this change, follow the steps below.

### Modify your config.yaml file

Now, apply the role and permission change to your platform's `config.yaml` file. Following the `deployment.images.push` example above, that would mean specifying this:

```yaml
astronomer:
  houston:
    config:
      roles:
        DEPLOYMENT_EDITOR:
          permissions:
            deployment.images.push: false
```

In the same way you can remove permissions from a particular role by setting a permission to `:false`, you can add permissions to a role at any time by setting a permission to `:true`.

For example, if you want to allow any `DEPLOYMENT_VIEWER` (and therefore `WORKSPACE_VIEWER`) to push code directly to any Airflow Deployment within a Workspace, you'd specify the following:

```yaml
astronomer:
  houston:
    config:
      roles:
        DEPLOYMENT_VIEWER:
          permissions:
            deployment.images.push: true
```

Then, push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).

## System Roles

### Overview

The System Admin role on Astronomer Software brings a range of cluster-wide permissions that supercedes Workspace-level access and allows a user to monitor and take action across Workspaces, Deployments and Users within a single cluster.

On Astronomer, System Admins specifically can:

- List and search *all* users
- List and search *all* deployments
- Access the Airflow UI for *all* deployments
- Delete a user
- Delete an Airflow Deployment
- Access Grafana and Kibana for cluster-level monitoring
- Add other System Admins

By default, the first user to log into an Astronomer Software installation is granted the System Admin permission set.

### System Editor, Viewer

In addition to the commonly used System Admin role, the Astronomer platform also supports both a System Editor and System Viewer permission set.

No user is assigned the System Editor or Viewer Roles by default, but they can be added by System Admins via our API. Once assigned, System Viewers, for example, can access both Grafana and Kibana but don't have permission to delete a Workspace they're not a part of.

All three permission sets are entirely customizable on Astronomer Software. For a full breakdown of the default configurations attached to the System Admin, Editor and Viewer Roles, refer to the [Houston API source code](https://github.com/astronomer/docs/tree/main/software_configs/0.23/default.yaml).

For guidelines on assigning users any System Level role, read below.

#### Assign Users System-Level Roles

System Admins can be added to Astronomer Software via the 'System Admin' tab of the Software UI.

Keep in mind that:
- Only existing System Admins can grant the SysAdmin role to another user
- The user must have a verified email address and already exist in the system

> **Note:** If you'd like to assign a user a different System-Level Role (either `SYSTEM_VIEWER` or `SYSTEM_EDITOR`), you'll have to do so via an API call from your platform's GraphQL playground. For guidelines, refer to our ["Houston API" doc](houston-api.md).

#### Verify SysAdmin Access

To verify a user was successfully granted the SysAdmin role, ensure they can do the following:

- Navigate to `grafana.BASEDOMAIN`
- Navigate to `kibana.BASEDOMAIN`
- Access the 'System Admin' tab from the top left menu of the Software UI

## Reference: System Permissions

This section contains the specific default permissions for each System user role on Astronomer. System roles apply to all Workspaces, users, and Deployments within a single Astronomer Software installation.

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

The System Editor has all of the same default permissions as the System Viewer, plus:

- `system.deployment.variables.update`: Modify [environment variables](environment-variables.md) for any Deployment
- `system.iam.update`: Modify [IAM](integrate-iam.md) roles for any Deployment
- `system.serviceAccounts.update`: Modify [service accounts](ci-cd.md#step-1-create-a-service-account) for any Workspace or Deployment
- `deployment.airflow.user`: Airflow [user permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) for all Deployments
- `system.registryBaseImages.push`: Modify base layer Docker images for Airflow

### System Admin

The System Admin has all of the same default permissions as the System Viewer and System Editor for a given cluster, plus:

- `system.deployments.create`: Create a Deployment on any Workspace
- `system.deployments.update`: Modify any Deployment
- `system.deployments.delete`: Delete any Deployment
- `system.deployments.logs`: View logging and metrics for any Deployment
- `system.user.invite`: Invite a user
- `system.user.delete`: Delete any user
- `system.user.verifyEmail`: Bypass email verification for any user
- `system.workspace.delete`: Delete any Workspace
- `system.airflow.admin`: Airflow admin permissions on any Deployment, including permission to configure:

    - Pools
    - Configuration
    - Users
    - Connections
    - Variables
    - XComs

### Workspace Viewer

The Workspace Viewer has the following default permissions for a given Workspace:

- `workspace.config.get`: View the Workspace
- `system.deployments.get`: View all settings and configuration pages of any Deployment
- `workspace.serviceAccounts.get`: View any Deployment or Workspace-level [service account](ci-cd.md#step-1-create-a-service-account)
- `workspace.users.get`: View information for all users with access to the Workspace

### Workspace Editor

For a given Workspace, the Workspace Editor has all of the same default permissions as the Workspace Viewer, plus:

- `workspace.config.update`: Modify the Workspace, including Workspace Name, Description, and user access
- `workspace.deployments.create`: Create a Deployment in the Workspace
- `workspace.serviceAccounts.create`: Create a Workspace-level service account
- `workspace.serviceAccounts.update`: Modify a Workspace-level service account
- `workspace.serviceAccounts.delete`: Delete a Workspace-level service account

### Workspace Admin

For a given Workspace, the Workspace Editor has all of the same default permissions as the Workspace Viewer and Workspace Editor, plus:

- `workspace.invites.get`: View pending user invites for the Workspace
- `workspace.config.delete`: Delete the Workspace
- `workspace.iam.update`: Update [IAM](integrate-iam.md) for the Workspace

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

Note that a Deployment Viewer cannot cannot push code to a Deployment or modify Deployment configurations. These actions can be completed only by a Deployment Editor or a Deployment Admin.

### Deployment Editor

For a given Deployment, the Deployment Editor has all of the same default permissions as the Deployment Viewer, plus:

- `deployment.airflow.user`: Airflow [user permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#user) for all Deployments, including modifying task runs and DAG runs
- `deployment.config.update`: Modify the Deployment's settings
- `deployment.images.push`: Push code to the Deployment via the Astronomer CLI
- `deployment.serviceAccounts.create`: Create a Deployment-level service account
- `deployment.serviceAccounts.update`: Modify a Deployment-level service account
- `deployment.serviceAccounts.delete`: Delete a Deployment-level service account
- `deployment.variables.update`: Update the Deployment's [environment variables](environment-variables.md)

Note that a Deployment Editor cannot make changes to certain configurations in the Airflow UI, such as connections and variables. These actions can be completed only by a Deployment Admin.

### Deployment Admin

For a given Deployment, the Deployment Admin has all of the same default permissions as the Deployment Viewer and the Deployment Editor, plus:

- `deployment.airflow.admin`: Airflow [admin permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#admin), including permission to configure:

    - Pools
    - Configuration
    - Users
    - Connections
    - Variables
    - XComs

- `deployment.config.delete`: Delete the Deployment
- `deployment.userRoles.update`: Update Deployment-level permissions for users within the Deployment
