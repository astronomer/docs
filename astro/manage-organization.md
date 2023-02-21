---
sidebar_label: "Manage Organization settings"
title: "Manage Organization settings"
id: manage-organization
description: Configure details about your Astro Organization including user authentication methods and Organization membership
---

Organizations are the highest level user group on Astro. All Astro users belong to at least one Organization and have an Organization role. See [Manage user permissions](user-permissions.md#organization-roles)

As an Organization Owner, you can manage Organization authentication and users in the Cloud UI and by contacting [Astronomer support](https://cloud.astronomer.io/support). This document explains how to configure Organization settings. To manage Organization users, see [Manage Astro users](add-user.md).

## Configure just-in-time provisioning for single sign-on

Astro supports just-in-time provisioning by default for all [single sign-on (SSO) integrations](configure-idp.md). This means that if someone without an Astronomer account tries logging into Astronomer with an email address from a domain that you manage, they are automatically granted a default role in your Organization without needing an invite. Users with emails outside of this domain need to be invited to your Organization to access it. 

Contact [Astronomer support](https://astronomer.io/support) for assistance with the following just-in-time provisioning settings:

- Enabling or disabling just-in-time provisioning.
- Adding or removing a managed domain.

## Bypass single sign-on

:::warning

Do not share your single sign-on (SSO) bypass link. With an SSO bypass link, anyone with an email and a password can access your Organization. 

:::

An SSO bypass link allows you to authenticate to an Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to an issue with Astro or your identity provider.

1. In the Cloud UI, click the **Settings** tab.
   
2. In the **SSO Bypass Link** field, click **Copy**.

3. Optional. When you finish using the bypass link, Astronomer recommends clicking **Regenerate** to create a new bypass link and void the old one. 

    If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 

## Restrict authentication options 

<PremiumBadge />

By default, users have access to all possible authentication methods when logging into Astro. You can remove specific authentication options so that users can use only the methods that your Organization wants to support, such as your third party identity provider.

To restrict which authentication options are available on Astro for your organization, contact [Astronomer support](https://cloud.astronomer.io/support).