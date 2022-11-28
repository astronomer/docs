---
title: 'Create a root user on Astronomer Software'
sidebar_label: 'Create a root user'
id: create-a-root-user
description: Learn how to create a root user with all possible permissions on Astronomer Software. 
---

By default, the first user to log in to an Astronomer Software installation becomes a System Admin in that installation. If your organization has strong security requirements, you can create a single root user and give only this user permissions to create new System Admins on your installation. 

## Create the root user 

To create a root user, add the following lines to your `config.yaml` file:

```yaml
global:
   rootAdmin:
          username: <your-root-user-email-address>
```

After saving your changes, apply the configuration change. See [Apply a config change](apply-platform-config.md).

By default, Astronomer generates a password for your root user email address. This password and email address are stored as Kubernetes secrets on your Astronomer installation. 

After you apply the configuration change, Helm provides a command for how to retrieve these the values of these secrets. To log in to Astronomer Software as the root user, retrieve the password and use the new **Root Admin Login** button on the Software login page.

## Customize the root user's password

You might want to use a custom root user password to ensure that someone who has recently left your organization no longer has access to the root user. 

To configure a custom password for the root user, run the following command: 

```sh
kubectl patch secret -n <your-platform-namespace> astronomer-root-admin-credentials --type=json -p='[{ "op" : "replace" , "path" : "/data/password" , "value" : "'$(echo -n "<your-new-password>" | base64)'"}]' && kubectl create job --from=cronjob/<your-release-name>-update-root-admin-password-cronjob manual3 -n <your-platform-namespace>
```

## Limit System-level user creation

A common use case for having a root user is to limit System-level user creation to only a single, tightly-controlled user. To configure your system this way, add the following lines to your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      roles:
        SYSTEM_ADMIN:
          permissions:
            system.iam.updateSystemLevelPermissions: false
        SYSTEM_ROOT_ADMIN:
          permissions:
            system.iam.updateSystemLevelPermissions: true
```

After saving your changes, apply the configuration change. See [Apply a config change](apply-platform-config.md).

See [Customize role permissions](manage-platform-users.md#customize-role-permissions) for how to further customize role permissions.
