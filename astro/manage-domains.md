---
sidebar_label: 'Manage domains'
title: 'Create and manage domains for your Organization'
id: manage-domains
description: Create and map domains to single sign-on platforms on Astro.
---

Authorization policies in Astro are based on email domains, which ensures that all users with an approved email domain authenticate with a specific authentication method. Domains can be mapped to single sign-on (SSO) methods so that users who have an email with a domain are automatically directed to your SSO platform when they log in to Astro.

You can only configure a single domain for an SSO connection. However, if you have multiple managed domains, then you can set up multiple different SSO connections, with a separate SSO connection for each domain. 

## Create a domain

1. In the Cloud UI, click your Workspace name in the upper left corner, click **Organization Settings**, then click **Authentication**.
2. In the **Managed Domains** menu, click **Managed Domain**.
3. In the **Domain** field, enter the domain that you want to map.
4. Click **Create**. The domain is added to your **Managed Domains** and marked as **Unverified**.
5. In the entry for your domain, click **Verify**.
6. After updating the DNS record, click **Verify** to notify Astro to check your DNS record.

:::info

Typically, a change in the DNS record takes only minutes to propagate; however, there are cases where it may take up to 72 hours.

:::

After your domain is verified, you can map the domain to an SSO connection. Mapping a domain ensures that all users with the same email address domain have the same authentication experience when they log in to Astro. You can later use this mapping to enforce specific login methods for users with emails from a specific domain. See [Configure SSO](configure-idp.md#configure-your-sso-identity-provider).

## Delete a domain

1. In the Cloud UI, click your Workspace name in the upper left corner, click **Organization Settings**, then click **Authentication**.
2. In the **Managed Domains** menu, click the trash bin next to the domain you want to delete. 
3. Follow the prompts to confirm the deletion.

