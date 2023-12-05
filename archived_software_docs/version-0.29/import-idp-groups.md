---
sidebar_label: 'Import IdP groups'
title: 'Import identity provider groups into Astronomer Software'
id: import-idp-groups
description: Import your identity provider's organization structure into Astronomer Software.
---

You can import existing identity provider (IdP) groups into Astronomer Software as Teams, which are groups of Astronomer users that have the same set of permissions for a specific Workspace or Deployment. Importing existing IdP groups as Teams lets you quickly onboard staff to Astronomer and provides better control of multiple user permissions.

Astronomer Teams function similar to users. You can:

- Assign Teams to both Workspaces and Deployments.
- Assign Viewer, Editor, or Admin roles to a Team.
- View information about users and permissions from the Astronomer UI.

## Implementation considerations

Before you implement Teams, consider the following:

- By default, the first user to log in to your Astronomer platform is automatically granted `SYSTEM ADMIN` permissions. If you are configuring Teams for a new Astronomer installation, we recommend first logging in as the user who will be responsible for importing your IdP groups using Astronomer's default login flow.
- Teams are based solely on the IdP group they were configured from, meaning that you cannot configure Team membership from Astronomer.
- If a user is added or removed from your original IdP group, that change applies to the related Astronomer Team only after the user logs back in to Astronomer.

:::warning "Most Permissive" Role Priority

Astronomer user roles function on a "most permissive" policy: If a user has roles defined at both the Workspace and the Team level, then that user will continue to have the most permissive role between the two contexts. This policy has a few implications for implementing Team:

- If a user's most permissive role comes from a Workspace configuration, there is no way to override/ remove this permission from a Team configuration.
- If a user's most permissive role comes from a Team configuration, then there is no way to override/ remove this permission from a Workspace configuration.
- Importing a Team from an IdP has no effect on existing Astronomer user roles. Users will continue to have permissions from both contexts, with the most permissive role defining how they interact with a given Workspace or Deployment.

For example, consider a user who has been a Workspace Editor in `Production Workspace` via Astronomer's default authentication for the last year. Your organization recently implemented Okta as your authentication system for Astronomer and added this user to a Team with Workspace Viewer permissions in `Production Workspace`. Because the user still has Workspace Editor permissions from their original account, they will continue to have Workspace Editor permissions in `Production Workspace`. The only way to remove their Editor permissions is to have a Workspace Admin remove them through Workspace settings.  

:::

## Prerequisites

To complete this setup, you need:

- A configured third party identity provider. See [Integrate an auth system](integrate-auth-system.md).
- System Admin permissions for configuring the feature. 
- Workspace or Deployment Admin permissions for managing Teams.
- An OAuth authorization code flow. See [Configure a custom OAuth flow](integrate-auth-system.md#configure-a-custom-oauth-flow).
- An IdP group.

## Step 1: Enable Astronomer teams

In your `config.yaml` file, set the following value.

```yaml
# Auth configuration.
auth:
  openidConnect:
    idpGroupsImportEnabled: true
```

Save this configuration and push it to your platform as described in [Apply a Platform Config Change](apply-platform-config.md).

## Step 2: Add a group claim to your IdP group

To add your IdP group to Astronomer as a Team, Astronomer needs to be able to recognize the IdP group through a group claim and assign members from the group through tokens.

If you haven't already, add group claims to the IdP groups that you're importing to Astronomer through your configured [third party identity provider](integrate-auth-system.md). Refer to your IdP's documentation for information on how to complete this step. For example, for Okta you can refer to [Customize tokens returned from Okta with a Groups claim](https://developer.okta.com/docs/guides/customize-tokens-groups-claim/main).

By default, Astronomer assumes that the name of your group claim is `groups`. If you named your group claim something other than `groups`, complete the following setup:

1. In your `config.yaml` file, set `houston.config.auth.openidConnect.<idp-provider>.claimsMapping` to the custom name of your group claim.
2. Save this configuration and push it to your platform. See [Apply a Platform Config Change](apply-platform-config.md).

## Step 3: Add Teams to Workspaces and Deployments

After configuring user groups on your IdP, Workspace Admins and Deployment Admins can configure those groups as Teams via the Astronomer UI. To learn more about adding and setting permissions for Teams via the Astronomer UI, read [User Permissions](workspace-permissions.md#via-teams).
