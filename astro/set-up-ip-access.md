---
sidebar_label: "Set up IP Access List"
title: "Set up IP Access List on Astro"
id: set-up-ip-access-list
description: Configure IP Access list to control the IP addresses from where your users can log in to Astro.
toc_max_heading_level: 3
---

import EnterpriseBadge from '@site/src/components/EnterpriseBadge';

</EnterpriseBadge>

You can restrict which IP addresses or IP address ranges can access the Astro service for your specific implementation. This means that if your organization uses a VPN or other mechanism that limits the IP addresses your users might have, you can restrict access to your Astro Deployments to your organization's IP addresses that you define in the the Astro UI.

After you enable the IP Access List, neither Airflow API no Astro API requests can access the Astro Organization.

