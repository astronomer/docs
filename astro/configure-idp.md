---
sidebar_label: "Set up an identity provider"
title: "Set up an identity provider (IdP) for Astro"
id: configure-idp
description: Configure federated authentication from a variety of third party identity providers on Astro.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';
import PremiumBadge from '@site/src/components/PremiumBadge';

There are 4 ways users can to authenticate to Astro:

- Basic authentication
- Google social login
- GitHub social login
- 3rd-party identity provider (IdP) login

Identity Providers (IdPs) are services that manage user accounts. As organizations grow, it's common for teams to integrate internal tooling with a third-party IdP. This allows administrators to monitor application access, user permissions, and security policies from a single place. It also makes it easy for individual users to access the tools they need.

Astro supports integrations with the following IdPs:

- [Azure Active Directory (AD)](https://azure.microsoft.com/en-us/services/active-directory/)
- [Okta](https://www.okta.com/)
- [OneLogin](https://www.onelogin.com/)
- [Ping Identity](https://www.pingidentity.com/en.html)

This guide provides setup steps for integrating both of these identity providers on Astro. Once you complete the integration for your organization:

- Users will automatically be authenticated to Astro if they're already logged in to your IdP.
- Users will no longer have to repeatedly login and remember credentials for their account.
- You will have complete ownership over credential configuration and management on Astro.
- You can enforce multi-factor authentication (MFA) for users.
- You can use services such as [Adaptive Authentication](https://www.okta.com/identity-101/adaptive-authentication/) and [Conditional Access](https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/overview) to create advanced access policies that enforce trusted IP ranges or limit access to authorized devices.

:::info

Astro only supports Service Provider (SP)-initiated SSO. Users are required to log in to the [Cloud UI](https://cloud.astronomer.io/).

:::

## Configure your identity provider

<Tabs
    defaultValue="Okta"
    groupId= "configure-your-identity-provider"
    values={[
        {label: 'Okta', value: 'Okta'},
        {label: 'Azure AD', value: 'Azure AD'},
        {label: 'OneLogin', value: 'OneLogin'},
        {label: 'Ping Identity', value: 'Ping Identity'},
    ]}>
<TabItem value="Okta">

This section provides setup steps for setting up Okta as your IdP on Astro. After completing this setup, all users in your organization can use Okta to log in to Astro.

#### Prerequisites

To integrate Okta as your IdP for Astro, you must have an [Okta account](https://www.okta.com/) with administrative access.

#### Step 1: Contact Astronomer support

To set up Okta as your IdP, submit a request to [Astronomer support](https://cloud.astronomer.io/support). After receiving your request, Astronomer support will provide you with the following:

- A Single Sign-On (SSO) URL
- An Audience URI

These values are required for Step 2.

#### Step 2: Configure Okta

1. Create a SAML app integration in the Okta Admin Console. See [Create SAML app integrations using AIW](https://help.okta.com/en/prod/Content/Topics/Apps/Apps_App_Integration_Wizard_SAML.htm). Complete the following fields:

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

#### Step 3: Provide Astronomer support with your integration information

On the page for your Okta app integration, click **View Setup Instructions**. Copy the values for `Single Sign-on URL` and `X.509 Certificate` that appear and send them to Astronomer Support.

From here, Astronomer support will finalize your organization's integration with Okta.

#### Step 4: Assign users to your Okta application

On the page for your Okta app integration, open the **Assignments** tab. Ensure that all users who will use Astro are assigned to the integration. For more information, read [Okta documentation](https://help.okta.com/en/prod/Content/Topics/users-groups-profiles/usgp-assign-apps.htm).

When a user assigned to the integration accesses Astro, they will be brought automatically to Okta after entering their email in the Cloud UI.

</TabItem>

<TabItem value="Azure AD">

This section provides setup steps for setting up Azure AD as your IdP on Astro. After completing this setup, your organization's users can use Azure AD to log in to Astro.

#### Prerequisites

To integrate Azure as your IdP for Astro you must have:

- An Azure subscription.
- An [Azure AD tenant](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-create-new-tenant) with `Global Administrator` privileges.

#### Step 1: Register Astro as an application on Azure

Follow [Microsoft Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) to register a new app. When configuring the application, set the following values:

- **Name** and **Supported account types**: Set these according to your organization's needs.
- **Redirect URI**: Select **Web** and specify `https://auth.astronomer.io/login/callback`.

#### Step 2: Create a client secret

Follow [Microsoft' documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a client secret for your new application. Make note of the secret value for Step 4.

:::caution

If you configure an expiring secret, make sure to record the expiration date and renew the secret before this date to avoid interruptions to your service.

:::

#### Step 3: Configure API permissions

Follow [Microsoft's documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis#add-permissions-to-access-web-apis) to add the following **Delegated** permissions to **Microsoft Graph**:

- `OpenId.email`
- `OpenId.openid`
- `OpenId.profile`
- `User.Read`

:::info

If your Azure Active Directory is configured to require admin approval on API permissions, make sure to also click the **Grant admin consent** button at the top of your permissions list.

:::

#### Step 4: Provide Astronomer with your Azure AD app information

Reach out to [Astronomer support](https://cloud.astronomer.io/support) and provide the following information from your Azure AD application:

- **Microsoft Azure AD Domain**: Retrieve this from your Azure AD directory's overview page in the Microsoft Azure portal.
- **Application (client) ID**: Retrieve this from the **Overview** page of your application.
- **Client secret**: Use the value of your client secret from Step 2.

From here, Astronomer will complete the integration and add Azure as your organization's IdP.

#### Step 5: Assign users to your Azure AD application

Follow [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/assign-user-or-group-access-portal) to assign users from your organization to your new application.

When a user assigned to the application accesses Astro, they will be brought automatically to Azure AD after entering their email in the Cloud UI.

</TabItem>

<TabItem value="OneLogin">

This section provides setup steps for setting up OneLogin as your IdP on Astro. After completing this setup, your organization's users can use OneLogin to log in to Astro.

#### Prerequisites

To integrate OneLogin as your IdP for Astro, you must have a [OneLogin account](https://www.onelogin.com/) with administrative access.

#### Step 1: Contact Astronomer support

To set up OneLogin as your IdP, submit a request to [Astronomer support](https://cloud.astronomer.io/support). After receiving your request, Astronomer support will provide you with the following:

- A Single Sign-On (SSO) URL
- An Audience URI

These values are required for Step 2.

#### Step 2: Create the OneLogin Astro application

1. In the OneLogin administrator dashboard, click **Applications** > **Applications** and then click **Add App**.  

2. In the **Search** field, enter **SAML Custom**, and then select **SAML Custom Connector (Advanced)**.

3. In the **Display Name** field, enter **Astro** and then click **Save**.

4. Click **Configuration** in the left menu and complete the following fields:

    - **Audience (EntityID)**: `<your-audience-uri>`
    - **ACS (Consumer) URL Validator**: `<your-sso-url>`
    - **ACS (Consumer) URL**: `<your-sso-url>`

5. Select the **Sign SLO Request** and **Sign SLO Response** checkboxes. 

6. Click **Save**.

7. Click **Parameters** in the left menu, and add the following four parameters, using the same capitalization shown in the **Value** column:

    | Field name | Value           |
    | ---------  | -----------------| 
    | email      | Email            |
    | firstName  | First Name       |
    | lastName   | Last Name        |
    | name       | Name             |

    Select the **Include in SAML assertion** checkbox for every parameter that you add and then click **Save**.

8. Click **SSO** in the left menu, click **View Details** below the **X.509 Certificate** field and then click **Download**. 

9. Select **SHA-256** in the **SAML Signature Algorithm** list.

10. Copy and save the value displayed in the **SAML 2.0 Endpoint (HTTP)** field.

#### Step 3: Provide Astronomer support with your integration information

Send the X.509 certificate and SAML 2.0 endpoint (HTTP) information you copied in step 2 to [Astronomer support](https://cloud.astronomer.io/support).

Astronomer support will finalize your organization's integration with OneLogin.

#### Step 4: Assign users to your OneLogin Astro application

1. In the OneLogin administrator dashboard, click **Applications** > **Applications** and then click **Astro**.

2. Click **Users** in the left menu.

3. Make sure that all users who are using Astro are assigned to the Astronomer application.

    When a user assigned to the application accesses Astro, they are automatically signed in to OneLogin after entering their email in the Cloud UI.

</TabItem>

<TabItem value="Ping Identity">

This section provides setup steps for setting up Ping Identity as your IdP on Astro. After completing this setup, your organization's users can use Ping Identity to log in to Astro.

#### Prerequisites

To integrate Ping Identity as your IdP for Astro, you must have a [Ping Identity account](https://www.pingidentity.com/) with administrative access.

#### Step 1: Contact Astronomer support

To set up Ping Identity as your IdP, submit a request to [Astronomer support](https://cloud.astronomer.io/support). After receiving your request, Astronomer support will provide you with the following:

- A Single Sign-On (SSO) URL
- An Audience URI

Save these values for Step 2.

#### Step 2: Configure Ping Identity

1. In the PingIdentity Administrator Console, click **Connections** in the left pane, and then click the **+** icon next to **Applications**.

2. In the **Application Name** field, enter `Astro`. Optionally, add a description and an icon.

3. Click **SAML Application**, and then click **Configure**.

4. Click **Manually Enter** and then complete the following fields:

    - **ACS URLs**: `<your-sso-url>`
    - **Entity ID**: `<your-audience-uri>`

5. Click **Save**.

6. Click **Edit** on the **Overview** page, and then enter `<your-sso-url>` in the **Signon URL** field. 

7. Click **Save**.

8. Click the **Configuration** tab, and then click **Edit**.

9. Select **Sign Assertion & Response** and confirm `RSA_SHA256` is selected in the **Signing Algorithm** list.

10. Click **Save**.

11. On the **Configuration** page, click **Download Signing Certificate** and select `X509 PEM (.crt)`.

12. Copy and save the URL in the **Single Signon Service** field.

13. Click the **Attribute Mappings** tab, click **Edit**, and add the following attributes, using the capitalization shown in both columns:

    | Astronomer        | PingOne           |
    | ------------      | ----------------| 
    | saml_subject      | User ID         |
    | email             | Email Address   |
    | firstName         | Given Name      |
    | lastName          | Family Name     |
    | name              | Formatted       |

14. Click **Save**.

15. Click the toggle in the top right to enable the application.

#### Step 3: Provide Astronomer support with your integration information

Send the X.509 certificate and the single sign on service URL you copied in step 2 to [Astronomer support](https://cloud.astronomer.io/support).

From here, Astronomer support will finalize your organization's integration with Okta.

#### Step 4: Assign users to your Ping Identity application

Assign users from your organization to your new application. See [Managing user groups](https://docs.pingidentity.com/bundle/pingcentral-19/page/awu1616596133840.html).

When a user assigned to the application accesses Astro, they are automatically signed in to Ping Identity after entering their email in the Cloud UI.

</TabItem>

</Tabs>

## Restrict authentication options 

<PremiumBadge />

By default, users have access to all possible authentication methods when logging into Astro. You can remove specific authentication options so that users can use only the methods that your team wants to support, such as your third party identity provider.

To restrict which authentication options are available on Astro for your organization, contact [Astronomer support](https://cloud.astronomer.io/support).