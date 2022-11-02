---
title: 'Manage users and roles on Astronomer Software'
sidebar_label: 'Manage users and roles'
id: manage-platform-users
description: Add and customize user permissions on Astronomer Software.
---

This is where you'll find information about role management and guidelines around public signups, role customization, and adding System Admins.

## Add users to Astronomer

When Astronomer Software is first deployed, the first user to log in is granted System Admin permissions by default. From there, a user can be created on Astronomer Software through one of the following methods:

- Invitation to a Workspace by a Workspace Admin
- Invitation to Astronomer by a System Admin
- Signing up through the Software UI without an invitation. See [Enable public signups](#enable-public-signups)
- Imported to Astronomer through an [IdP group](import-idp-groups.md)

New users appear under a System Admin's **Users** tab only after the new user has successfully logged in for the first time.

:::tip 

You can bypass the email verification process for new users through a Houston API mutation. For the format of this mutation, see [Sample Mutations](houston-api.md#sample-mutations).

:::

### Enable public signups

Public signups allow any user with access to the platform URL (the Software UI) to create an account. If public signups are disabled, users that try to access Astronomer without an invitation from another user receive an error.

In cases where SMTP credentials are difficult to acquire, enabling this flag might facilitate initial setup, as disabling public signups requires that a user accept an email invitation. Public signups can be enabled in the `config.yaml` file of your Helm chart.

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

Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

## User roles on Astronomer

System Admins can customize permissions across teams. On Astronomer, users can be assigned roles at 2 levels:

- Workspace Level (Viewer, Editor, Admin)
- System Level (Viewer, Editor, Admin)

Workspace roles apply to all Deployments within a single Workspace, while system roles apply to all Workspaces across a single cluster. For a detailed breakdown of the three Workspace-level roles on Astronomer Software (Viewer, Editor and Admin), see [Manage user permissions on an Astronomer Workspace](workspace-permissions.md).

## Customize user role permissions

Permissions are defined on Astronomer as `scope.entity.action`, where:

- `scope`: The layer of our application to which the permission applies
- `entity`: The object or role being operated on
- `action`: The verb describing the operation being performed on the `entity`

For example, the `deployment.serviceAccounts.create` permission translates to the ability for a user to create a Deployment-level Service account. To view all available platform permissions and default role configurations, see [Reference: System permissions](manage-platform-users.md#reference-system-permissions).

To customize permissions, follow the steps below.

### Identify a permission change

<!--- Version-specific -->

Before customizing role permissions, review [default Houston API configuration](https://github.com/astronomer/docs/tree/main/software_configs/0.29/default.yaml) and then answer the following questions:

- What role do you want to configure? For example, `DEPLOYMENT_EDITOR`.
- What permission(s) do you want to add to or remove from the role? For example, `deployment.images.push`.

For example, you might want to block a `DEPLOYMENT_EDITOR` (and therefore `WORKSPACE_EDITOR`) from deploying code to all Airflow Deployments within a Workspace and instead limit that action to users assigned the `DEPLOYMENT_ADMIN` role. 

### Role permission inheritance 



### Limit Workspace creation

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

Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

## System roles

The System Admin role on Astronomer Software brings a range of cluster-wide permissions that supersedes Workspace-level access and allows a user to monitor and take action across Workspaces, Deployments, and Users within a single cluster.

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

<!--- Version-specific -->

In addition to the commonly used System Admin role, the Astronomer platform also supports both a System Editor and System Viewer permission set.

No user is assigned the System Editor or Viewer Roles by default, but they can be added by System Admins via our API. Once assigned, System Viewers, for example, can access both Grafana and Kibana but don't have permission to delete a Workspace they're not a part of.

All three permission sets are entirely customizable on Astronomer Software. For a full breakdown of the default configurations attached to the System Admin, Editor and Viewer Roles, refer to the [Houston API source code](https://github.com/astronomer/docs/tree/main/software_configs/0.29/default.yaml).

For guidelines on assigning users any System Level role, read below.

#### Assign users system-level roles

System Admins can be added to Astronomer Software via the 'System Admin' tab of the Software UI.

Keep in mind that:
- Only existing System Admins can grant the SysAdmin role to another user
- The user must have a verified email address and already exist in the system

> **Note:** If you'd like to assign a user a different System-Level Role (either `SYSTEM_VIEWER` or `SYSTEM_EDITOR`), you'll have to do so via an API call from your platform's GraphQL playground. For guidelines, refer to our ["Houston API" doc](houston-api.md).

#### Verify SysAdmin access

To verify a user was successfully granted the SysAdmin role, ensure they can do the following:

- Navigate to `grafana.BASEDOMAIN`
- Navigate to `kibana.BASEDOMAIN`
- Access the 'System Admin' tab from the top left menu of the Software UI

