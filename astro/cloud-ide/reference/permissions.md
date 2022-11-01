---
sidebar_label: Permissions
title: Astro Cloud IDE permissions
id: permissions
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_ and it is available to all Astro customers. It is still in development and features and functionality are subject to change. Creating projects in the Cloud IDE does not affect running tasks on existing Deployments. If you have feedback on the Cloud IDE you'd like to share, you can submit it on the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

The Cloud IDE inherits permissions from the Workspace. Workspaces have three roles that are assignable on the [Workspace Access page](/astro/manage-workspaces.md#manage-workspace-users):

- Workspace Viewers
- Workspace Editors
- Workspace Admins

### Workspace Viewers

Workspace Viewers have general read-only access. They can:

- View and list projects.
- View and list pipelines.

Workspace Viewers cannot:

- Create, edit, or delete projects.
- Create, edit, or delete pipelines.
- Create, edit, or delete cells.
- Run pipelines.

### Workspace Editors and Admins

Workspace Editors and Admins have full access to the workspace. They can:

- View, list, create, edit, and delete projects.
- View, list, create, edit, and delete pipelines.
- View, list, create, edit, and delete cells.
- Run cells and pipelines.
