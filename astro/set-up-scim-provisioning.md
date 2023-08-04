---
sidebar_label: "Set up SCIM provisioning"
title: "Set up SCIM provisioning on Astro"
id: set-up-scim-provisioning
description: Configure SCIM provisioning to import groups of users from your identity provider to Astro as Teams.
toc_max_heading_level: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

:::caution

This feature is in [Public Preview](https://docs.astronomer.io/astro/feature-previews).

:::

Astro supports integration with the open standard System for Cross-Domain Identity Management (SCIM). Using the SCIM protocol with Astro allows you to automatically provision and deprovision users and [Teams](manage-teams.md) based on templates for access and permissions. It also provides better observability through your identity provider for when users and Teams are created or modified across your organization. Specifically, you can utilize SCIM provisioning to complete the following Astro actions from your identity provider platform:

- Create and remove users in your Organization.
- Update user profile information.
- Create and remove Astro Teams.
- Add and remove Team members.
- Retrieve user and Team information.

:::info

Some user management features on Astro behave differently after you set up SCIM provisioning. See [Manage Teams](manage-teams.md#teams-and-scim-provisioning) for more information.

:::

## Supported SSO identity providers

Astro supports SCIM provisioning with the following IdPs:

- [Azure Active Directory (AD)](https://azure.microsoft.com/en-us/services/active-directory/)
- [Okta](https://www.okta.com/)

### Supported Okta features

Okta's Astro integration supports the following SCIM actions:

- Create users
- Update user attributes
- Deactivate users
- Group push

## Prerequisites

- A configured identity provider. See [Set up SSO](configure-idp.md).

## Setup 

<Tabs
    defaultValue="Okta"
    groupId= "setup"
    values={[
        {label: 'Okta - Astro integration (Recommended)', value: 'Okta'},
        {label: 'Okta - Manual', value: 'OktaManual'},
        {label: 'Azure AD', value: 'Azure'},
    ]}>
<TabItem value= "Okta">

1. Create an Organization API token with Organization Owner permissions. See [Organization API tokens](organization-api-tokens.md). Copy the token to use later in this setup.
2. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **General**.
3. Copy your **Organization ID** to use later in this setup.
4. Go to **Settings > Authentication**. In the **Advanced Settings** menu, click **Edit Settings**, then click the **SCIM integration** toggle to on.
5. In the Okta admin dashboard, open your Astro app integration and click **Provisioning**.
6. Click **Configure API integration**, check **Enable API integration**, then configure the following values:

    - **Organization ID**: Enter your **Organization ID**.
    - **API token**: Enter your Organization API token.
  
7.  Test your API credentials, then click **Save**.
8.  In the **Provisioning** menu, click **To App** and configure the following:

    - **Provisioning to App**: Select only **Create Users**, **Update User Attributes**, and **Deactivate Users**. 
  
    See [Okta documentation](https://developer.okta.com/docs/guides/scim-provisioning-integration-connect/main/#to-app) for more information on configuring these values.

9.  Create user groups and push them to Astro. User groups pushed to Astro appear as [Teams](manage-teams.md) in the Cloud UI. See [Okta documentation](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) for setup steps.

</TabItem>
<TabItem value="OktaManual">

Complete the manual setup if you configured your existing Astro app without using the Okta app catalogue.

1. Create an Organization API token with Organization Owner permissions. See [Organization API tokens](organization-api-tokens.md). Copy the token to use later in this setup.
2. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Authentication**.
3. In the **Advanced Settings** menu, click **Edit Settings**, then click the **SCIM integration** toggle to on.
4. Copy the **SCIM Integration URL** that appears.
5. In the Okta admin dashboard, add SCIM provisioning to your existing Astro app integration. Then, open your app in Okta and go to **Provisioning** > **Integration** to configure the following values: 

    - **Supported provisioning actions**: Select **Push New Users**, **Push Profile Updates**, and **Push Groups**.
    - **SCIM connector base URL**: Enter the SCIM integration URL you copied from the Cloud UI.
    - **Unique identifier field for users**: `email`.
    - **Authentication Mode**: Choose **HTTP Header** and paste your Organization API token in the **Bearer** field.
  
    See [Okta documentation](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm) for more information about setting up SCIM provisioning. 

6. In the **Provisioning** menu, click **To App** and configure the following:

    - **Provisioning to App**: Select **Create Users**, **Update User Attributes**, and **Deactivate Users**.
    - **Astro Attribute Mappings**: Configure the following mappings:

    | Attribute                    | Attribute Type | Value                          | Apply On          |
    | ---------------------------- | -------------- | ------------------------------ | ----------------- |
    | Username (`userName`)        | Personal       | Configured in sign-on settings |                   |
    | Given name  (`givenName`)    | Personal       | user.firstName                 | Create and update |
    | Family name (`familyName`)   | Personal       | user.lastName                  | Create and update |
    | Email  (`email`)             | Personal       | user.email                     | Create and update |
    | Display name (`displayName`) | Personal       | user.displayName               | Create and update |
    | Profile Url  (`profileUrl`)  | Personal       | user.profileUrl                | Create and update |

    See [Okta documentation](https://developer.okta.com/docs/guides/scim-provisioning-integration-connect/main/#to-app) for more information on configuring these values.

7. Create user groups and push them to Astro. User groups pushed to Astro appear as [Teams](manage-teams.md) in the Cloud UI. See [Okta documentation](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) for setup steps.

</TabItem>
<TabItem value="Azure">

1. Create an Organization API token with Organization Owner permissions. See [Organization API tokens](organization-api-tokens.md). Copy the token to use later in this setup.
2. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Authentication**.
3. In the **Advanced Settings** menu, click **Edit Settings**, then click the **SCIM integration** toggle to on.
4. Copy the **SCIM Integration URL** that appears.
5. Append the [Azure AD feature flag parameter](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/application-provisioning-config-problem-scim-compatibility#flags-to-alter-the-scim-behavior) `?aadOptscim062020` to your **SCIM Integration URL** and recopy it. For example, if your SCIM Integration URL is `https://api.astronomer.io/scim/v2/cknaqyipv05731evsry6cj4n0`, your final URL would be `https://api.astronomer.io/scim/v2/cknaqyipv05731evsry6cj4n0?aadOptscim062020`. The feature flag is required for fully compliant SCIM behavior in Azure AD.
6. In the Azure AD management dashboard, [create a new enterprise application](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/add-application-portal#add-an-enterprise-application).
7. In the menu for your new application, click **Provisioning** and configure the following values:

    - **Provisioning mode**: Set to **Automatic**.
    - **Admin Credentials** > **Tenant URL**: Enter the **SCIM integration URL** including the Azure AD feature flag parameter.
    - **Secret Token**: Enter your Organization API token. 
    - **Mappings**: Configure the following mappings:

    | Azure Active Directory Attribute | Astro Attribute |
    | -------------------------------- | --------------- |
    | userPrincipalName                | userName        |
    | displayName                      | displayName     |
    | givenName                        | name.givenName  |
    | surname                          | name.familyName |

  :::caution

  This setup assumes that `userPrincipalName` contains your users' email. If you use a field other than `userPrincipalName` to define your user email, replace `userPrincipalName` with the attribute you use.

  ::: 

1. Click **Test connection** in the Azure AD application management menu to confirm your connection to the SCIM endpoint.

</TabItem>
</Tabs>

## Frequently asked questions

### What if an Okta group is out of sync with an Astro Team?

1. In the Okta dashboard, open the Astro application and click **Push Groups**.
2. Click the value in **Push Status** for the group that's out of sync, then click **Push now**.

### What if an Okta user is out of sync with their Astro user account?

If you removed an Okta user but their Astro account remains, [delete the account from Astro](manage-organization-users.md#update-or-remove-an-organization-user).

If an Astro user is not appearing for an Okta user as expected, remove and re-assign the user in Okta.
