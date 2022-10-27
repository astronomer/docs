---
sidebar_label: Permissions
title: Permissions
id: permissions
---

The Cloud IDE inherits permissions from the workspace. Workspaces have three roles that are assignable via the [Workspace Access page](/astro/manage-workspaces.md#manage-workspace-users):

- Workspace Viewers
- Workspace Editors
- Workspace Admins

### Workspace Viewers

Workspace Viewers have general read-only access. They can:

- View and list projects
- View and list pipelines

Workspace Viewers cannot:

- Create, edit, or delete projects
- Create, edit, or delete pipelines
- Create, edit, or delete cells
- Run pipelines

### Workspace Editors & Admins

Workspace Editors and Admins have full access to the workspace. They can:

- View, list, create, edit, and delete projects
- View, list, create, edit, and delete pipelines
- View, list, create, edit, and delete cells
- Run cells and pipelines
