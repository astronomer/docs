---
sidebar_label: "Set up SSO"
title: "Set up authentication and single sign on for Astro"
id: configure-idp
description: Configure federated authentication from a variety of third party identity providers on Astro.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Including Single Sign-On (SSO) authorization, there are 4 ways that users can to authenticate to Astro:

- Basic authentication (username and password)
- Google social login
- GitHub social login
- 3rd-party identity provider (IdP) login

This guide provides the steps for integrating identity providers on Astro to enable SSO for your users. After you complete the integration for your organization:

- Users will automatically be authenticated to Astro if they're already logged in to your IdP.
- Users will no longer have to repeatedly login and remember credentials for their account.
- You will have complete ownership over credential configuration and management on Astro.
- You can enforce multi-factor authentication (MFA) for users.
- You can use services such as [Adaptive Authentication](https://www.okta.com/identity-101/adaptive-authentication/) and [Conditional Access](https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/overview) to create advanced access policies that enforce trusted IP ranges or limit access to authorized devices.

To manage Organization users after you have configured SSO, see [Manage Astro users](add-user.md).

## SSO authorization identity providers

Single Sign On (SSO) authorization allows users to log in using their company credentials, managed via an identity provider (IdP). This provides a streamlined login experience for your Astro users, as they are able to leverage the same credentials across multiple applications. In addition, this provides improved security and control for organizations to manage access from a single source. Astro supports integrations with the following IdPs:

- [Azure Active Directory (AD)](https://azure.microsoft.com/en-us/services/active-directory/)
- [Okta](https://www.okta.com/)
- [OneLogin](https://www.onelogin.com/)
- [Ping Identity](https://www.pingidentity.com/en.html)

## Configure your SSO identity provider

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

### Prerequisites

- [Organization Owner](user-permissions.md) privileges in the Organization you're configuring.
- An [Okta account](https://www.okta.com/) with administrative access.
- At least one [verified domain](manage-domains.md).

### Step 1: Create a SAML-based connection to Okta

To set up Okta as your IdP, you will create a Security Assertion Markup Language (SAML) connection to Okta.

1. In the Cloud UI, click **Settings**, then click **Authentication**.
2. In the **SSO Configuration** menu, click **Configure SSO**.
3. Configure the following values for your connection:

    - **Connection type**: Select **SAML**.
    - **SSO Domain(s)**: Enter the verified domain(s) that you want to map to Okta.
    - **Automatic Membership**: Set the default role for users who join your Organization through Okta and without an explicit invite from Astro.

4. Copy the **Single Sign On URL** and **Audience URI (SP ENTITY ID)** for the next step.

5. Open a new tab and go to Okta. In the Okta Admin Console, create a SAML app integration. See [Create SAML app integrations using AIW](https://help.okta.com/en/prod/Content/Topics/Apps/Apps_App_Integration_Wizard_SAML.htm). Complete the following fields:

    - **Single sign on URL**: `<your-sso-url>`
    - **Audience URI (SP Entity ID)**: `<your-audience-uri>`
    - **Name ID format**: `Unspecified`
    - **Application username**: `Email`
    - **Update application username on**: `Create and update`

6. In the **Advanced Settings** section of your configuration, set the following values:

    - **Response**: `Signed`
    - **Assertion Signature**: `Signed`
    - **Signature Algorithm**: `RSA-SHA256`
    - **Digest Algorithm**: `SHA256`
    - **Assertion Encryption**: `Unencrypted`

7. In the **Attribute Statements** section of your configuration, create the following four attribute statements, making sure to use the exact capitalization as shown:

    | Name      | Name Format | Value            |
    | --------- | ----------- | ---------------- |
    | email     | Unspecified | user.email       |
    | firstName | Unspecified | user.firstName   |
    | lastName  | Unspecified | user.lastName    |
    | name      | Unspecified | user.displayName |

  :::info

  These values might be different if Okta is connected to an Active Directory. In this case, replace each `Value` with the equivalent Active Directory values for a user's first name, last name, and full email address.

  :::

8. Complete the remainder of the setup as documented in Okta until you finish creating your integration.
9. On the page for your Okta app integration, click **View Setup Instructions**. Copy the values for **Single Sign-on URL** and **X.509 Certificate** that appear. 
10. Assign yourself to the Astro app integration from Okta. See [Assign an app integration to a user](https://help.okta.com/en-us/Content/Topics/Provisioning/lcm/lcm-assign-app-user.htm).
11. Return to the Cloud UI. In the configuration screen for your SAML connection, configure the following values:

    - **Identity Provider Single Sign-on URL**: Enter your **Single Sign-on URL**.
    - **X.509 Certificate**: Enter your **X.509 Certificate**.

12. Click **Create**. Your Okta integration appears as an entry in **SSO Configuration**.
13. In **SSO Configuration**, click **Activate**. You are redirected to Okta to test your configuration. After you have successfully authenticated, you are redirected to Astro.
14. Click **Activate SSO**.

### Step 2: Copy your SSO bypass link

:::caution

Do not share your single sign-on (SSO) bypass link. With an SSO bypass link, anyone with an email and a password can log in to Astro. Astronomer recommends periodically regenerating the link from the **Settings** tab in the Cloud UI.

:::

An SSO bypass link allows you to authenticate to your Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to an issue your identity provider.

1. In the Cloud UI, click the **Settings** tab.
   
2. In the **SSO Bypass Link** field, click **Copy**. Save this link for when you need to log in to Astro without using SSO.

If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 

### Step 3: Assign users to your Okta application

On the page for your Okta app integration, open the **Assignments** tab. Ensure that all users who will use Astro are assigned to the integration. For more information, see [Assign applications to users](https://help.okta.com/en/prod/Content/Topics/users-groups-profiles/usgp-assign-apps.htm).

</TabItem>

<TabItem value="Azure AD">

This section provides setup steps for setting up Azure AD as your IdP on Astro. After completing this setup, your organization's users can use Azure AD to log in to Astro.

### Prerequisites

To integrate Azure as your IdP for Astro you must have:

- An Azure subscription.
- An [Azure AD tenant](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-create-new-tenant) with `Global Administrator` privileges.
- [Organization Owner](user-permissions.md) privileges in the Organization you're configuring.
- At least one [verified domain](manage-domains.md).

### Step 1: Register Astro as an application on Azure

Follow [Microsoft Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) to register a new app. When configuring the application, set the following values:

- **Name** and **Supported account types**: Set these according to your organization's needs.
- **Redirect URI**: Select **Web** and specify `https://auth.astronomer.io/login/callback`.

### Step 2: Create a client secret

Follow [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials) to create a client secret for your new application. Make note of the client ID and secret value for Step 5.

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

### Step 4: Create an SSO connection to Azure AD

1. Assign yourself to Astro from Azure AD. See [Assign users and groups to an Application](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/assign-user-or-group-access-portal?pivots=portal).
2. In the Cloud UI, click **Settings**, then click **Authentication**.
3. In the **SSO Configuration** menu, click **Configure SSO**.
4. Configure the following values for your connection:

    - **Connection type**: Select **Azure AD**.
    - **SSO Domain(s)**: Enter the verified domain(s) that you want to map to Azure AD.
    - **Automatic Membership**: Set the default role for users who join your Organization through Azure AD and without an explicit invite from Astro.
    - **Microsoft Azure AD Domain**: Retrieve this value from your Azure AD directory's overview page in the Microsoft Azure portal.
    - **Application (client) ID**: Retrieve this from the **Overview** page of your Azure AD application.
    - **Client ID and Client secret**: Enter the values you coped from [Step 3: Create a client secret](#step-3-create-a-client-secret)

5. If you already completed [Step 2: Register Astro as an application on Azure](#step-2-register-astro-as-an-application-on-azure), skip the Cloud UI instructions to configure a Redirect URI.
6. Click **Create**. Your Azure AD integration appears as an entry in **SSO Configuration**.
7. In **SSO Configuration**, click **Activate**. You are redirected to Azure AD to test your configuration. After you have successfully authenticated, you are redirected to Astro.
8. Click **Activate SSO**.

### Step 5: Copy your SSO bypass link

:::caution

Do not share your single sign-on (SSO) bypass link. With an SSO bypass link, anyone with an email and a password can log in to Astro. Astronomer recommends periodically regenerating the link from the **Settings** tab in the Cloud UI.

:::

An SSO bypass link allows you to authenticate to your Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to an issue your identity provider.

1. In the Cloud UI, click the **Settings** tab.
   
2. In the **SSO Bypass Link** field, click **Copy**. Save this link for when you need to log in to Astro without using SSO.

If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 


### Step 6: Assign users to your Azure AD application

Follow [Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/assign-user-or-group-access-portal) to assign users from your organization to your new application.

When a user assigned to the application accesses Astro, they will be brought automatically to Azure AD after entering their email in the Cloud UI.

</TabItem>

<TabItem value="OneLogin">

This section provides setup steps for setting up OneLogin as your IdP on Astro. After completing this setup, your organization's users can use OneLogin to log in to Astro.

### Prerequisites

- A [OneLogin account](https://www.onelogin.com/) with administrative access.
- [Organization Owner](user-permissions.md) privileges in the Organization you're configuring.
- At least one [verified domain](manage-domains.md).

### Step 1: Create a SAML-based connection to OneLogin

To set up OneLogin as your IdP, you will create a Security Assertion Markup Language (SAML) connection to OneLogin.

1. In the Cloud UI, click **Settings**, then click **Authentication**.
2. In the **SSO Configuration** menu, click **Configure SSO**.
3. Configure the following values for your connection:

    - **Connection type**: Select **SAML**.
    - **SSO Domain(s)**: Enter the verified domain(s) that you want to map to OneLogin.
    - **Automatic Membership**: Set the default role for users who join your Organization through OneLogin and without an explicit invite from Astro.

4. Copy the **Single Sign On URL** and **Audience URI (SP ENTITY ID)** for Step 8.

5. Open a new tab and go to OneLogin. In the OneLogin administrator dashboard, click **Applications** > **Applications** and then click **Add App**.  

6. In the **Search** field, enter **SAML Custom**, and then select **SAML Custom Connector (Advanced)**.

7. In the **Display Name** field, enter **Astro** and then click **Save**.

8. Click **Configuration** in the left menu and complete the following fields:

    - **Audience (EntityID)**: `<your-audience-uri>`
    - **ACS (Consumer) URL Validator**: `<your-sso-url>`
    - **ACS (Consumer) URL**: `<your-sso-url>`

9. Select the **Sign SLO Request** and **Sign SLO Response** checkboxes. Then, click **Save**.

10. Click **Parameters** in the left menu, and add the following four parameters, using the same capitalization shown in the **Value** column:

    | Field name | Value           |
    | ---------  | -----------------| 
    | email      | Email            |
    | firstName  | First Name       |
    | lastName   | Last Name        |
    | name       | Name             |

    Select the **Include in SAML assertion** checkbox for every parameter that you add and then click **Save**.

12. Click **SSO** in the left menu, click **View Details** below the **X.509 Certificate** field and then click **Download**. 

13. Select **SHA-256** in the **SAML Signature Algorithm** list.

14. Copy and save the value displayed in the **SAML 2.0 Endpoint (HTTP)** field.

15. Assign yourself to the Astro app integration from OneLogin. See [Assigning apps to users](https://onelogin.service-now.com/kb_view_customer.do?sysparm_article=KB0010387).
    
16. Return to the Cloud UI. In the configuration screen for your SAML connection, configure the following values:

    - **Identity Provider Single Sign-on URL**: Enter the value you copied from **SAML 2.0 Endpoint (HTTP)**.
    - **X.509 Certificate**: Enter the **X.509 Certificate** that you downloaded.

17. Click **Create**. Your OneLogin integration appears as an entry in **SSO Configuration**.
    
18. In **SSO Configuration**, click **Activate**. You are redirected to OneLogin to test your configuration. After you have successfully authenticated, you are redirected to Astro. Then, click **Activate SSO**.
    
### Step 4: Copy your SSO bypass link

:::caution

Do not share your single sign-on (SSO) bypass link. With an SSO bypass link, anyone with an email and a password can log in to Astro. Astronomer recommends periodically regenerating the link from the **Settings** tab in the Cloud UI.

:::

An SSO bypass link allows you to authenticate to your Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to an issue your identity provider.

1. In the Cloud UI, click the **Settings** tab.
   
2. In the **SSO Bypass Link** field, click **Copy**. Save this link for when you need to log in to Astro without using SSO.

If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 

#### Step 5: Assign users to your OneLogin Astro application

1. In the OneLogin administrator dashboard, click **Applications** > **Applications** and then click **Astro**.

2. Click **Users** in the left menu.

3. Make sure that all users who need to use Astro are assigned to the Astronomer application.

</TabItem>

<TabItem value="Ping Identity">

This section provides setup steps for setting up Ping Identity as your IdP on Astro. After completing this setup, your organization's users can use Ping Identity to log in to Astro.

### Prerequisites

- A [Ping Identity account](https://www.pingidentity.com/) with administrative access.
- [Organization Owner](user-permissions.md) privileges in the Organization you're configuring.
- At least one [verified domain](manage-domains.md).

### Step 1: Configure Ping Identity

1. In the Cloud UI, click **Settings**, then click **Authentication**.
   
2. In the **SSO Configuration** menu, click **Configure SSO**.
   
3. Configure the following values for your connection:

    - **Connection type**: Select **SAML**.
    - **SSO Domain(s)**: Enter the verified domain(s) that you want to map to Ping Identity.
    - **Automatic Membership**: Set the default role for users who join your Organization through Ping Identity and without an explicit invite from Astro.

4. Copy the **Single Sign On URL** and **Audience URI (SP ENTITY ID)** for Step 8.

5. Open a new tab and go to PingIdentity. In the PingIdentity Administrator Console, click **Connections** in the left pane, and then click the **+** icon next to **Applications**.

6. In the **Application Name** field, enter `Astro`. Optionally, add a description and an icon.

7. Click **SAML Application**, and then click **Configure**.

8. Click **Manually Enter** and then complete the following fields:

    - **ACS URLs**: `<your-sso-url>`
    - **Entity ID**: `<your-audience-uri>`

9.  Click **Save**.

10. Click **Edit** on the **Overview** page, and then enter `<your-sso-url>` in the **Signon URL** field. Then, click **Save**.

11. Click the **Configuration** tab, and then click **Edit**.

12. Select **Sign Assertion & Response** and confirm `RSA_SHA256` is selected in the **Signing Algorithm** list. Then, click **Save**.

13. On the **Configuration** page, click **Download Signing Certificate** and select `X509 PEM (.crt)` to download the X.509 certificate for your application.

14. Copy and save the URL in the **Single Signon Service** field.

15. Click the **Attribute Mappings** tab, click **Edit**, and add the following attributes, using the capitalization shown in both columns:

    | Astronomer        | PingOne           |
    | ------------      | ----------------| 
    | saml_subject      | User ID         |
    | email             | Email Address   |
    | firstName         | Given Name      |
    | lastName          | Family Name     |
    | name              | Formatted       |

16. Click **Save**.

17. Click the toggle in the top right to enable the application.
    
18. Assign yourself to Astro from Ping Identity. See [Editing a user](https://docs.pingidentity.com/r/en-us/pingone/p1_t_edituser?section=gnn1564020489010).
    
19. Return to the Cloud UI. In the configuration screen for your SAML connection, configure the following values:

    - **Identity Provider Single Sign-on URL**: Enter the value you copied from the **Single Signon Service** field.
    - **X.509 Certificate**: Enter the X.509 Certificate that you downloaded.

20. Click **Create**. Your Ping Identity integration appears as an entry in **SSO Configuration**.
    
21. In **SSO Configuration**, click **Activate**. You are redirected to Ping Identity to test your configuration. After you have successfully authenticated, you are redirected to Astro.
    
22. Click **Activate SSO**.
    
### Step 2: Copy your SSO bypass link

:::caution

Do not share your single sign-on (SSO) bypass link. With an SSO bypass link, anyone with an email and a password can log in to Astro. Astronomer recommends periodically regenerating the link from the **Settings** tab in the Cloud UI.

:::

An SSO bypass link allows you to authenticate to your Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to an issue your identity provider.

1. In the Cloud UI, click the **Settings** tab.
   
2. In the **SSO Bypass Link** field, click **Copy**. Save this link for when you need to log in to Astro without using SSO.

If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 

### Step 3: Assign users to your Ping Identity application

Assign users from your organization to your new application. See [Managing user groups](https://docs.pingidentity.com/bundle/pingcentral-19/page/awu1616596133840.html).

When a user assigned to the application accesses Astro, they are automatically signed in to Ping Identity after entering their email in the Cloud UI.

</TabItem>

</Tabs>

## Advanced setup

### Disable just-in-time provisioning

Astro supports just-in-time provisioning by default for all [single sign-on (SSO) integrations](configure-idp.md). This means that if someone without an Astronomer account tries logging into Astronomer with an email address from a domain that you manage, they are automatically granted a default role in your Organization without needing an invite. Users with emails outside of this domain need to be invited to your Organization to access it. 

Contact [Astronomer support](https://cloud.astronomer.io/support) for assistance with enabling or disabling just-in-time provisioning.

### Restrict authentication options 

By default, users have access to all possible authentication methods when logging into Astro. You can remove specific authentication options, such as GitHub or Google, so that users can use only the methods that your Organization wants to support, such as your third party identity provider.

To restrict which authentication options are available on Astro for your organization, contact [Astronomer support](https://cloud.astronomer.io/support).

### Regenerate an SSO bypass link

Regenerating your SSO bypass link voids your existing SSO bypass link so that any former users with the existing link can't log in to Astro. 

1. In the Cloud UI, click the **Settings** tab.
   
2. Click **Regenerate** to create a new bypass link and void the old one. 

   

