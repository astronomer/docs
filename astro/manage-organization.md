---
sidebar_label: "Manage an Organization on Astro"
title: "Manage an Organization"
id: manage-organization
description: Configure details about your Astro Organization including user authentication methods and Organization membership
---

Organizations are the highest level user group on Astro. All Astro users belong to at least one Organization and have an Organization role. See [Manage user permissions](user-permissions.md#organization-roles)

As an Organization Owner, you can manage Organization authentication and users from the Astro UI and through Astronomer support. This document explains how to configure Organization details. To manage Organization users, see [Manage Astro users](add-user.md).

## Configure just-in-time provisioning for single sign-on

Astro supports just-in-time provisioning by default for all [single sign-on (SSO) integrations](configure-idp.md). This means that if someone without an Astronomer account tries logging into Astronomer with an email address from a domain that you manage, they are automatically granted a default role in your Organization without needing an invite. Users with emails outside of this domain still need to be invited to your Organization before they can access it. 

Contact [Astronomer support](https://astronomer.io/support) to configure the following for just-in-time provisioning:

- Enable or disable just-in-time provisioning.
- Add or remove a managed domain.

## Bypass single sign-on

:::warning

Do not share your SSO bypass link with anyone for general purpose use. An SSO bypass link allows anyone to access your Organization using only their email and a password regardless of whether they belong to your Organization. 

:::

An SSO bypass link allows you to authenticate to an Organization without using SSO. This link should be used to access your Organization only when you can't access Astro due to a bug in Astro or your identity provider.

1. In the Cloud UI, click **Settings**.
   
2. In the **SSO Bypass Link** field, click **Copy**.

3. Optional. When you finish using the bypass link, Astronomer recommends clicking **Regenerate** to create a new bypass link and void the old one. 

    If you don't want to maintain an SSO bypass link, click **Delete**. You can always regenerate a link if you need one in the future. 