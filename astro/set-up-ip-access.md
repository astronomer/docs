---
sidebar_label: "Set up IP Access List"
title: "Set up IP Access List on Astro"
id: set-up-ip-access-list
description: Configure IP Access list to control the IP addresses from where your users can log in to Astro.
toc_max_heading_level: 3
---

import EnterpriseBadge from '@site/src/components/EnterpriseBadge';

</EnterpriseBadge>

You can restrict which IP addresses or IP address ranges can access the Astro service for your specific implementation. This means that if your organization uses a VPN or other mechanism that limits the IP addresses your users might have, you can restrict access to your Astro Deployments to the IP addresses that you define in the the Astro UI.

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

