---
sidebar_label: "Set Up an Identity Provider"
title: "Set Up an Identity Provider for Astro"
id: configure-idp
description: Configure federated authentication from a variety of third party identity providers on Astro.
---

## Overview

This guide provides setup steps for integrating various third party identity providers (IdP) with Astro.

Identity Providers (IdPs) are services that manage user accounts. As organizations grow, it's common for teams to integrate internal tooling with a third-party IdP. This allows administrators to monitor application access, user permissions, and security policies from a single place. It also makes it easy for individual users to access the tools they need.

Astro supports integrations with the following IdPs:

- [Okta](https://www.okta.com/)
- [Azure Active Directory (AD)](https://azure.microsoft.com/en-us/services/active-directory/)

This guide provides setup steps for integrating both of these identity providers on Astro. Once you complete the integration for your organization:

- Users will automatically be authenticated to Astro if they're already logged in to your IdP.
- Users will no longer have to repeatedly login and remember credentials for their account.
- You will have complete ownership over credential configuration and management on Astro.

:::info

Astro only supports Service Provider (SP)-initiated SSO. Users are required to log in via the [Cloud UI](https://cloud.astronomer.io/)

:::

## Configure Okta as Your Identity Provider

This section provides setup steps for setting up Okta as your IdP on Astro. After completing this setup, all users in your organization can use Okta to log in to Astro.

### Prerequisites

To integrate Okta as your IdP for Astro, you must have an [Okta account](https://www.okta.com/) with administrative access.

### Step 1: Reach out to Astronomer

Reach out to [Astronomer Support](https://support.astronomer.io) with a request to integrate Okta as an IdP on Astro. From here, an Astronomer Representative will provide you with two things:

- A Single Sign-On (SSO) URL
- An Audience URI

Save these values for Step 2.

### Step 2: Configure Okta

1. Follow the [Okta documentation](https://help.okta.com/en/prod/Content/Topics/Apps/Apps_App_Integration_Wizard_SAML.htm) to create a SAML App Integration via Okta's Admin Console. Configure the following SAML settings:

    - **Single sign on URL**: `<your-sso-url>`
    - **Audience URI (SP Entity ID)**: `<your-audience-uri>`
    - **Name ID format**: `Unspecified`
    - **Application username**: `Email`
    - **Update application username on**: `Create and update`

2. In the **Advanced Settings** section of your configuration, set the following values:

    - **Response**: `Signed`
    - **Assertion Signature**: `Signed`
    - **Signature Algorithm**: `RSA-SHA256`
    - **Digest Algorithm**: `SHA256`
    - **Assertion Encryption**: `Unencrypted`

3. In the **Attribute Statements** section of your configuration, create the following four attribute statements, making sure to use the exact capitalization as shown:

    | Name      | Name Format | Value            |
    | --------- | ----------- | ---------------- |
    | email     | Unspecified | user.email       |
    | firstName | Unspecified | user.firstName   |
    | lastName  | Unspecified | user.lastName    |
    | name      | Unspecified | user.displayName |

  :::info

  These values might be different if Okta is connected to an Active Directory. In this case, replace each `Value` with the equivalent Active Directory values for a user's first name, last name, and full email address.

  :::

4. Complete the remainder of the setup as documented in Okta until you finish creating your integration.

### Step 3: Provide Astronomer with your integration information

On the page for your Okta app integration, click **View Setup Instructions**. Copy the values for `Single Sign-on URL` and `X.509 Certificate` that appear and send them to Astronomer Support.

From here, Astronomer will finalize your organization's integration with Okta.

### Step 4: Assign users to your Okta application

On the page for your Okta app integration, open the **Assignments** tab. Ensure that all users who will use Astro are assigned to the integration. For more information, read [Okta Documentation](https://help.okta.com/en/prod/Content/Topics/users-groups-profiles/usgp-assign-apps.htm).

When a user assigned to the integration accesses Astro, they will be brought automatically to Okta after entering their email in the Cloud UI.

## Configure Azure AD as your Identity Provider

This section provides setup steps for setting up Azure AD as your IdP on Astro. After completing this setup, your organization's users can use Azure AD to log in to Astro.

### Prerequisites

To integrate Azure as your IdP for Astro you must have:

- An Azure subscription.
- An [Azure AD tenant](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-create-new-tenant) with `Global Administrator` privileges.

### Step 1: Register Astro as an application on Azure

Follow [Microsoft Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) to register a new app. When configuring the application, set the following values:

- **Name** and **Supported account types**: Set these according to your organization's needs.
- **Redirect URI**: Select **Web** and specify `https://auth.astronomer.io/login/callback`.

### Step 2: Create a client secret

Follow [Microsoft' documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a client secret for your new application. Make note of the secret value for Step 4.

:::caution

If you configure an expiring secret, make sure to record the expiration date and renew the secret before this date to avoid interruptions to your service.

:::

### Step 3: Configure API permissions

Follow [Microsoft's documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis#add-permissions-to-access-web-apis) to add the following **Delegated** permissions to **Microsoft Graph**:

- `OpenId.email`
- `OpenId.openid`
- `OpenId.profile`
- `User.Read`

:::info

If your Azure Active Directory is configured to require admin approval on API permissions, make sure to also click the **Grant admin consent** button at the top of your permissions list.

:::

### Step 4: Provide Astronomer with your Azure AD app information

Reach out to [Astronomer Support](https://support.astronomer.io) and provide the following information from your Azure AD application:

- **Microsoft Azure AD Domain**: Retrieve this from your Azure AD directory's overview page in the Microsoft Azure portal.
- **Application (client) ID**: Retrieve this from the **Overview** page of your application.
- **Client secret**: Use the value of your client secret from Step 2.

From here, Astronomer will complete the integration and add Azure as your organization's IDP.

### Step 5: Assign users to your Azure AD application

Follow [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/assign-user-or-group-access-portal) to assign users from your organization to your new application.

When a user assigned to the application accesses Astro, they will be brought automatically to Azure AD after entering their email in the Cloud UI.
