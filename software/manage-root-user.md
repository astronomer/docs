---
title: 'Manage the root user on Astronomer Software'
sidebar_label: 'Manage the root user'
id: manage-root-user
description: Learn how to manage the root user role with all permissions on Astronomer Software
---

When you install Astronomer Software, a root user with all permissions is automatically created. The root user's username is `root@<your-basedomain>`, and the password is stored as a Kubernetes secret on your installation.

## Log in as the root user

By default, Astronomer generates a password for your root user. The password is stored as a Kubernetes secret on your Astronomer installation.

To retrieve the password, run the following command: 

```sh
kubectl get secret astronomer-root-admin-credentials -o jsonpath='{.data.password}' -n <your-platform-namespace> | base64 --decode
```

To log in to Astronomer Software as the root user, retrieve the password and click **Root Admin Login** on the Software login page.

## Customize the root user's password

You might want to use a custom root user password to ensure that someone who has recently left your organization no longer has access to the root user. 

To configure a custom password for the root user, run the following command: 

```sh
kubectl patch secret -n <your-platform-namespace> astronomer-root-admin-credentials --type=json -p='[{ "op" : "replace" , "path" : "/data/password" , "value" : "'$(echo -n "<your-new-password>" | base64)'"}]' && kubectl create job --from=cronjob/<your-release-name>-update-root-admin-password-cronjob manual3 -n <your-platform-namespace>
```

## Limit System-level user creation

A common use case for having a root user is to limit system-level user creation to a single user. To configure your system this way, add the following lines to your `config.yaml` file:

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

To learn more about customizing role permissions, see [Customize role permissions](manage-platform-users.md#customize-role-permissions) .
