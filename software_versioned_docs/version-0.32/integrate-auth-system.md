---
sidebar_label: 'Integrate an auth system'
title: 'Integrate an auth system on Astronomer Software'
id: integrate-auth-system
description: Integrate your internal authentication server with Astronomer Software.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Astronomer Software by default allows users to create an account with and authenticate using one of the following methods:

- Google OAuth
- GitHub OAuth
- Local username/password

Authentication methods are entirely customizable. In addition to the default methods, Astronomer provides the option to integrate any provider that follows the [Open Id Connect (OIDC)](https://openid.net/connect/) protocol. This includes (but is not limited to):

- [Microsoft Azure Active Directory (AD)](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc)
- [Okta](https://www.okta.com)
- [Auth0](https://auth0.com/)

:::info

The following setups assume that you are using the default Astronomer [implicit flow](https://datatracker.ietf.org/doc/html/rfc6749#section-4.2) as your authorization flow. To implement a custom authorization flow, see [Configure a Custom OAuth Flow](integrate-auth-system.md#configure-a-custom-oauth-flow).

:::

## Local auth

To let users authenticate to Astronomer with a local username and password, follow the steps below.

1. Enable Local Auth in your `config.yaml` file:
```yaml
astronomer:
  houston:
    config:
      auth:
        local:
          enabled: true
```

2. Push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

## General OIDC configuration

If you'd like to integrate an OIDC provider with Astronomer Software, you can enable that configuration in the `config.yaml` file of your `astronomer` directory.

Example:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          clockTolerance: 0 # A field that can optionally be set to adjust for clock skew on the server.
          <provider-name>:
            enabled: true
            discoveryUrl: <provider-discovery-url> # Note this must be a URL that with an https:// prefix
            clientId: <provider-client-id>
            authUrlParams: # Additional required params set on case-by-case basis
```
### Microsoft Entra ID

Replace the values above with those of the provider of your choice. If you want to configure Microsoft Entra ID, Okta or Auth0 read below for specific guidelines.

### AWS Cognito

#### Create a user pool in Cognito

Start by creating a user pool in Cognito. You can either review the default settings or step through them to customize.

Make sure that you create an `App client`, which is the OpenID client configuration that we will use to authenticate against. You do not need to generate a client secret, as Astronomer is a public client that uses implicit flow.

Once the pool and app client are created, head over to the `App integration` >`App client settings` tab and configure these settings:

- Select an identity provider to use (either the built-in cognito user pool or a federated identity provider).
- Set the callback URL parameter to `https://houston.BASEDOMAIN/v1/oauth/redirect/`.
- Enable `Implicit grant` in `Allowed OAuth Flows`. Leave the other settings disabled.
- Enable `email`, `openid`, and `profile` in `Allowed OAuth Scopes`.

Then switch over to the `Domain name` tab and select a unique domain name to use for your hosted Cognito components.

#### Edit your Astronomer configuration

Add the following values to your `config.yaml` file in the `astronomer/` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          cognito:
            enabled: true
            clientId: <client_id>
            discoveryUrl: https://cognito-idp.<AWS-REGION>.amazonaws.com/<COGNITO-POOL-ID>/.well-known/openid-configuration
            authUrlParams:
              response_type: token
```

Your Cognito pool ID can be found in the `General settings` tab of the Cognito portal. Your client ID is found in the `App clients` tab.

Once you've saved your `config.yaml` file with these values, push it to your platform. See [Apply a config change](apply-platform-config.md).

### Microsoft Entra ID

Follow these steps to configure Microsoft Entra ID as your OIDC provider. 

#### Register the Application using `App Registrations` on Azure

1. In Microsoft Entra ID, click **App registrations** > **New registration**. 
2. Complete the following sections:
  
    - **Name**: Any
    - **Supported account types**: Accounts in this organizational directory only (Astronomer only - single tenant)
    - **Redirect URIs**:
        - Web / `https://houston.BASEDOMAIN/v1/oauth/redirect/`.
        - Web / `https://houston.BASEDOMAIN/v1/oauth/callback/`.

    Replace `BASEDOMAIN` with your own. For example, if your base domain is `mycompany.com`, your redirect URIs should be `https://houston.mycompany.com/v1/oauth/redirect/` and `https://houston.mycompany.com/v1/oauth/callback/`.

3. Click **Register**.

4. Click **Authentication** in the left menu.
5. In the **Web** area, confirm the redirect URI is correct.

6. In the **Implicit grant and hybrid flows** area, select **Access tokens** and **ID tokens**.

7. Click **Save**.

![authentication.png](/img/software/azure-authentication.png)

#### Create a client secret (Optional)

Complete this setup only if you want to import Microsoft Entra ID groups to Astronomer Software as [Teams](import-idp-groups.md).

1. In your Microsoft Entra ID application management left menu, click **Certificates & secrets**.
2. Click **New client secret**.
3. Enter a description in the **Description** field and then select an expiry period in the **Expires** list. 
4. Click **Add**.
5. Copy the values in the **Value** and **Secret ID** columns. 
6. Click **API permissions** in the left menu.
7. Click **Microsoft Graph** and add the following minimum permissions for Microsoft Graph:

    - `email`
    - `Group.Read.All`
    - `openid`
    - `profile`
    - `User.Read`
    
    For each of these permissions, select **Grant Admin Consent for Astronomer Data**. Your Microsoft Graph permissions should look similar to the following image:
    
    ![Completed permissions page in Azure](/img/software/azure_api_permissions_consent.png)


8. Click **Token configuration** in the left menu.
9. Click **Add groups claim** and select the following options:

    - In the **Select group types to include in Access, ID, and SAML tokens** area, select every option. 
    - In **Customize token properties by type** area, expand **ID**, **Access**, and **SAML** and then select **Group ID** for each type.
    
10. Click **Add**.
11. Encrypt the secret value you copied as a Kubernetes Secret on your Astronomer installation. See [Store and encrypt identity provider secrets](#store-and-encrypt-identity-provider-secrets).

#### Enable Microsoft Entra ID in your config.yaml file

Add the following values to the `config.yaml` file in your `astronomer` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          flow: "code"
          google:
            enabled: false
          microsoft:
            enabled: true
            clientId: <your-client-id>
            discoveryUrl: https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration
            # Configure a secret only if you're importing Microsoft Entra ID user groups as Teams
            clientSecret: <your-client-secret>
            baseDomain: login.microsoftonline.com
            authUrlParams:
              audience: <your-client-id>
        github:
          enabled: false
```
Push the configuration change to your platform. See [Apply a config change](apply-platform-config.md).

### Okta

To integrate Okta with Astronomer, you'll need to make configuration changes in Okta and Astronomer.


#### Okta configuration

1. If you haven't already, create an [Okta account](https://www.okta.com/).

2. In your Okta account, create a new web app for Astronomer.

3. In Okta, under **General Settings** > **Application**, set `Login redirect URIs` to `https://houston.BASEDOMAIN/v1/oauth/redirect/`, where `BASEDOMAIN` is the domain where you're hosting your Software installation.

4. Under **Allowed grant types**, select `Implicit (Hybrid)`.

5. Save the `Client ID` generated for this Okta app for use in the next steps.

6. Optional. To ensure that an Okta tile appears, set `Initiate Login URI` to `https://houston.BASEDOMAIN/v1/oauth/start?provider=okta`.

#### Enable Okta in your config.yaml file

Add the following to your `config.yaml` file in your `astronomer` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          okta:
            enabled: true
            clientId: "<okta-client-id>"
            discoveryUrl: "https://<okta-base-domain>/.well-known/openid-configuration"
```

Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

> **Note:** `okta-base-domain` will be different from the basedomain of your Software installation. You can read [Okta's docs on finding your domain](https://developer.okta.com/docs/api/getting_started/finding_your_domain/) if you are unsure what this value should be.

### Auth0

#### Create an Auth0 account

You'll need an Auth0 account in order to set up connections with the identity management provider of your choice. [Sign up for an Auth0 account](https://auth0.com/signup) if you need to.

#### Create Auth0 tenant domain

When you log into Auth0 you'll be prompted to create a tenant domain. You can use the default or your own unique `tenant-name`. Your full tenant domain will look something like `astronomer.auth0.com`.

> **Note:** Your full tenant domain may differ if you've created it outside of the United States.

#### Create a connection between Auth0 and your identity management provider

Depending on the Identity Management Provider you'd like to use, the steps required to establish a connection will vary.

For instructions, navigate to Auth0's [connection guides](https://auth0.com/docs/identityproviders) and select the identity provider of your choice. Once your connection is established, read below.

#### Configure Auth0 application settings

**Enable / disable desired connections:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Connections` tab. You should see your connection created in Step 3 listed here. Enable your new connection, and disable any connections that you won't be using.

**Edit the Default App settings:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/applications`.
* Under `Applications`, select `Default App`.
* Click the `Settings` tab.
* Under `Allowed Callback URLs`, add `https://houston.<your-astronomer-base-domain>/v1/oauth/redirect/`.
* Under `Allowed Logout URLs`, add `https://app.<your-astronomer-base-domain>/logout`.
* Under `Allowed Origins (CORS)`, add `https://*.<your-astronomer-base-domain>`.

**Create Auth0 API:**

* Navigate to `https://manage.auth0.com/dashboard/us/<tenant-name>/apis`.
* Click `+ Create API`.
* Under `Name`, enter `astronomer-ee`.
* Under `Identifier`, enter `astronomer-ee`.
* Leave the value under `Signing Algorithm` as `RS256`.

#### Enable Auth0 in your config.yaml file

Add the following to your `config.yaml` file in your `astronomer` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          auth0:
            enabled: true
            clientId: "<default-app-client-id>"
            discoveryUrl: https://<tenant-name>.auth0.com
```
Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

> **Note:** You can find your `clientID` value at `https://manage.auth0.com/dashboard/us/<tenant-name>/applications` listed next to 'Default App'.

## Running behind an HTTPS proxy

### Overview

Integrating an external identity provider with Astronomer requires that the platform's Houston API component is able to make outbound HTTPS requests to those identity providers in order to fetch discovery documents, sign keys, and ask for user profile information upon login/signup.

If your install is configured _without_ a direct connection to the internet you will need to configure an HTTPS proxy server for Houston.

### Configure an HTTPS proxy server for Houston

To configure the proxy server used we need to set the `GLOBAL_AGENT_HTTPS_PROXY` Environment Variable for the Houston deployment.

To do so, add the following to the Houston section of the `config.yaml` file in your `astronomer` directory:

```yaml
astronomer:
  houston:
    config:
      auth:
        openidConnect:
          <provider>:
            enabled: true
            clientId: ...
            discoveryUrl: ...
    env:
      - name: GLOBAL_AGENT_HTTPS_PROXY
        value: http://my-proxy:3129
```

Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

## Configure a custom OAuth flow

Starting with Astronomer v0.27, you can set up a custom OAuth authorization flow as an alternative to Astronomer's default [implicit flow](https://datatracker.ietf.org/doc/html/rfc6749#section-4.2). You can customize Astronomer's existing Okta, Google, and GitHub OAuth flows or import an entirely custom OAuth flow.

:::warning
This setup must be completed only during a scheduled maintenance window. There should be no active users on your installation until the setup has been finalized.
:::

### Step 1: Configure your authorization flow on Astronomer

To use a custom Oauth authorization code flow:

1. In your `config.yaml` file, set the `astronomer.houston.auth.openidConnect.flow` value to `"code"`:

    ```yaml
    auth:
      # Local database (user/pass) configuration.
      local:
        enabled: true

      openidConnect:
        # Valid values are "code" and "implicit"
        flow: "code"
    ```

2. Configure the section of your `config.yaml` file specific to your identity provider with each of the following values:

    - `enabled`: Set this value to `true` under the section for your own identity provider.
    - `clientId` and `clientSecret`: Your [Client ID and Client secret](https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/)
    - `discoveryURL`: Your base [Discovery URL](https://www.oauth.com/oauth2-servers/indieauth/discovery/)
    - `authUrlParams`: Additional [parameters](https://developer.okta.com/docs/guides/add-an-external-idp/saml2/main/#use-the-authorize-url-to-simulate-the-authorization-flow) to append to your discovery URL. At a minimum, you must configure `audience`. Refer to your identity provider's documentation for information on how to find this value (Auth0 maintains this information in their [glossary](https://auth0.com/docs/glossary), for example).

    For example, a custom configuration of Okta might look like the following.

    ```yaml
        okta:
          enabled: true
          clientId: ffhsdf78f734h2fsd
          clientSecret: FSDFSLDFJELLGJLSDFGJL42353425
          # URL works only when IdP group imports are disabled. To import IdP groups from Okta to Software,
          # use "https://<MYIdP>.okta.com/oauth2/default/.well-known/openid-configuration" instead
          discoveryUrl: "https://<MYIdP>.okta.com/.well-known/openid-configuration"
          authUrlParams:
            audience: "GYHWEYHTHR443fFEW"
    ```

    3. Push your configuration changes to your platform as described in [Apply a config change](apply-platform-config.md).

:::tip

You can also pass your auth configurations as environment variables in the Houston section of your `config.yaml` file. If you choose to configure your installation this way, set the following variables in the `astronomer.houston.env` list instead of setting values in `astronomer.auth`:

```yaml
# Replace <idp-provider> with OKTA, AUTH0, or CUSTOM
AUTH__OPENID_CONNECT__<idp-provider>__ENABLED="true"
AUTH__OPENID_CONNECT__<idp-provider>__CLIENT_ID="<client-id>"
AUTH__OPENID_CONNECT__<idp-provider>__CLIENT_SECRET="<client-secret>"
AUTH__OPENID_CONNECT__<idp-provider>__DISCOVERY_URL="<discovery-url>
AUTH__OPENID_CONNECT__<idp-provider>__AUTH_URL_PARAMS__AUDIENCE="<audience>"
AUTH__OPENID_CONNECT__FLOW="implicit" # or "code"
AUTH__OPENID_CONNECT__<idp-provider>__BASE_DOMAIN="<base-domain>"
AUTH__OPENID_CONNECT__CUSTOM__DISPLAY_NAME="Custom OAuth" # Only used for custom flows
```

For further security, you can specify the values of these environment variables as Kubernetes secrets in the `astronomer.houston.secret` list. See [Store and encrypt identity provider secrets](#store-and-encrypt-identity-provider-secrets).

:::

### Step 2: Configure your identity provider

To finalize your configuration, configure the following key values in your identity provider's settings:

- **Grant Code:** Set to "Code" or "Auth Code" depending on your identity provider.
- **Sign-in Redirect URI:** Set to `https://houston.<BASE_DOMAIN>/v1/oauth/callback/`. Be sure to include the trailing `/`.

### Step 3: Confirm your installation

When you complete this setup, you should be able to see the differences in login flow when logging in at `<BASE_DOMAIN>.astronomer.io`.

If you configured a fully custom OAuth flow, you should see a new **Log in with Custom Oauth** button on the Astronomer login screen:

![Custom login button on the Astronomer login screen](/img/software/custom-oauth.png)

You can see the name you configured in `AUTH__OPENID_CONNECT__CUSTOM__DISPLAY_NAME` when authenticating using the Astro CLI.

## Manage users and Teams with SCIM

Astronomer Software supports integration with the open standard System for Cross-Domain Identity Management (SCIM). Using the SCIM protocol with Astronomer Software allows you to automatically provision and deprovision users and Teams based on templates for access and permissions. It also provides better observability through your identity provider for when users and Teams are created or modified across your organization.

<Tabs
    groupId="scim"
    defaultValue="okta"
    values={[
        {label: 'Microsoft Entra ID', value: 'ME-ID'},
        {label: 'Okta', value: 'okta'},
    ]}>
<TabItem value="okta">

This setup assumes that you have already created a web app for Astronomer Software in Okta. See [Okta](#okta).

1. In your Astronomer integration's settings page on Okta, open the **General** tab.

2. Click **Edit**.

3. In the **Provisioning** section, select **SCIM**.

4. Click **Save**.

5. In your Astronomer integration's settings page, open the **Provisioning** tab.

6. Configure the following values for your SCIM integration.

    - **SCIM connector base URL**: `https://BASEDOMAIN.astronomer.io/v1/scim/okta`
    - **Authentication mode**: Basic Auth
        - Username: `<your-provisioning-account-username>`
        - Password: `<your-provisioning-account-password>`

7. Go to **Configure API Integration** and select the **Enable API Integration** checkbox.

8. Go to **Push Groups** page and create a rule for Group Push. See [Group Push](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-about-group-push.htm).

9. On the Assignments tab, ensure that the right users and groups in your org are assigned to the app integration. See [Use the Assign Users to App action](https://help.okta.com/en-us/Content/Topics/Apps/apps-assign-applications.htm?cshid=ext_Apps_Apps_Page-assign).

10. Add the following lines to your `config.yaml` file:

    ```yaml
    astronomer:
      houston:
        config:
          okta:
            scimAuthCode: <your-provisioning-account-username>:<your-provisioning-account-password>
    ```

11. Push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

See [Add SCIM provisioning to app integrations](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_SCIM.htm?cshid=ext_Apps_App_Integration_Wizard-scim) for more information about configuring SCIM within Okta.

</TabItem>

<TabItem value="ME-ID">

1. In your `config.yaml` file, add the following configuration. Replace `<your-generated-secret-code>` with a randomly generated string. 

    ```yaml
    astronomer:
      houston: 
        config:
          auth:
            openidConnect:
              microsoft:
                scimAuthCode: <your-generated-secret-code>
    ```
   
    **Note**: If you have already configured Open ID Connect with Microsoft Entra ID, the `scimAuthCode` key should be on the same level as `clientId` and `discoveryUrl`

2. Push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

3. Sign in to the [Microsoft Entra ID portal](https://aad.portal.azure.com/). 
   
4. In the left menu, select **Enterprise applications**, and then click **New application** > **Create your own application**.
   
5. Enter a name for your application and select **Integrate any other application you don't find in the gallery**.
  
6. Click **Create** to create an app object. Microsoft Entra ID opens the application management menu for your new application.
  
7. In the application management menu for your new application, go to **Manage** > **Provisioning** and click **Get Started**.

8. Click **Provisioning Mode** > **Automatic**.

9. In the **Tenant URL** field, enter `https://houston.BASEDOMAIN/v1/scim/v2/microsoft`. This is the Astronomer SCIM endpoint URL.

10. Paste the `scimAuthCode` generated at step 1 above into the **Secret Token** field.

11. Click **Test connection** in the Microsoft Entra ID application management menu to confirm your connection to the SCIM endpoint.

12. Create mappings for your Astronomer users and roles. See [Tutorial - Customize user provisioning attribute-mappings for SaaS applications in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/customize-application-attributes).

13. Click **Manage** > **Provisioning** > **Settings**.

14. In the **Scope** setting list, select **Sync only assigned users and groups**.
   
15. Click the **Provisioning status** toggle to turn provisioning status on.

16. Click **Save**.

</TabItem>
</Tabs>

## Store and encrypt identity provider secrets

You can prevent your identity provider passwords, authorization tokens, and security keys from being exposed as plain text by encrypting them in Kubernetes secrets.

This setup is primarily used for encrypting the required secrets for [configuring a custom OAuth flow](#configure-a-custom-oauth-flow).
 
1. Create a file named `secret.yaml` that contains the value you want to encrypt as a [Kubernetes secret](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/#create-the-config-file). The following example encrypts the required client secret for [configuring a custom OAuth flow](#configure-a-custom-oauth-flow) for Okta. 

    ```yaml
    # Required configuration for all secrets
    kind: Secret
    apiVersion: v1
    metadata:
         name: okta-secret
         labels:
            release: {{ .Release.Name }}
            chart: {{ .Chart.Name }}
            heritage: {{ .Release.Service }}
            component: {{ template "houston.backendSecret" . }}
    type: Opaque
    # Specify a key and value for the data you want to encrypt
    data:
        okta_client_secret: {{ "<okta-secret-value>" | b64enc | quote }}
    ```

2. Run the following command to apply your secret to your Astronomer cluster:

    ```sh
    kubectl apply -f ./secret.yaml
    ```

3. Reference your secret name, key, and the environment variable you want the key to apply towards in your `config.yaml` file. To configure the example secret from Step 1 as an Okta client secret, you would add the following:

    ```yaml
    astronomer:
        houston:
            secret:
             - envName: "AUTH__OPENID_CONNECT__OKTA__CLIENT_SECRET"
               secretName: "okta-secret"
               secretKey: "okta_client_secret"
    ```

4. Save and push your changes. See [Apply a config change](apply-platform-config.md).
