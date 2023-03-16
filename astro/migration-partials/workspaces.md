
Astro has Workspaces - which are collections of Airflow Deployments that can be accessed by a specific group of users.

Follow the [Manage Workspaces](manage-workspaces.md#add-a-user-to-a-workspace) documentation to create a workspace in the Astro UI to hold your migrated Airflow Deployments.

Afterwards, add users to your new Workspace by referring to [Manage Astro users](add-user.md).
More details on user permissions can be found at [Manage Astro user permissions](user-permissions.md#workspace-roles)

:::tip

Both Astro Workspaces and Organizations have Role-based Access Control. 
You can refer to [Manage Astro users](add-user.md) for information on inviting others teammates to your 
Organization, or use an Identity Provider (e.g. Okta) if you have one already to manage access to Astro.

:::