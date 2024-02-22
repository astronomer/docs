---
title: "Create and assign custom roles for Astro Deployments"
id: deployment-role-reference
unlisted: true
description: Learn about each possible permission that you can assign to custom Deployment roles
---

:::caution

This feature is in [Private Preview](feature-previews.md).

:::

This doc contains all available permissions that you can assign to a [custom Deployment role](customize-deployment-roles). Permissions are organized by the object that the permissions belong to.

## Deployment Airflow AdminMenu

- `deployment.airflow.adminMenu.get`: View the **Admin** menu in the Airflow UI.

### Deployment Airflow Connection

- `deployment.airflow.connection.get`: View connections in the Airflow UI.
- `deployment.airflow.connection.create`: Create connections in the Airflow UI.
- `deployment.airflow.connection.update`: Update connections in the Airflow UI.
- `deployment.airflow.connection.delete`: Delete connections in the Airflow UI.

