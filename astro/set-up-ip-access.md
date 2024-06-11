---
sidebar_label: "Set up IP Access List"
title: "Set up IP Access List on Astro"
id: ip-access-list
description: Configure IP Access list to control the IP addresses from where your users can log in to Astro.
---

import EnterpriseBadge from '@site/src/components/EnterpriseBadge';

<EnterpriseBadge/>

You can restrict which IP addresses or IP address ranges can access the Astro service for your specific Organization. This means that if your organization uses a VPN or other mechanism that limits the IP addresses your users might have, you can restrict access to your Astro Deployments to the IP addresses that you define in the the Astro UI.

After you enable the IP Access List, neither Airflow API no Astro API requests can access the Astro Organization, whether by using the Astro UI or programmatically through API requests.

## Prerequisites

- Organization Owner permissions

## Set up IP Access list

1. In the Astro UI, click your Workspace name in the upper left corner, then click **Organization Settings**. This opens the **General** Organization page.
2. Select **Authentication**.
3. In the **IP Access List** section, select **IP Address Range**.
4. Add the IP Adress range or ranges in CIDR format.
    :::danger

    Make sure the first IP range you add is inclusive of the IP you are currently using, or you will be locked out of your organization.

    :::

## Restore access

Because the IP Access List limits access to the Astro UI only to specific IP addresses, you cannot access the Astro UI if you're not connected to a corresponding VPN or authorized network.

To restore access for a user that is blocked, an Organization Owner needs to either:

- Disable the IP Access list setting or
- Add the specific blocked user's IP address to the IP Access list.

If you disable the IP Access List setting to resolve the user's access issue temporarily, remember to enable the setting again to maintain the IP address restrictions.