---
sidebar_label: "Allowlist Astro domains"
title: "Add Astro domains to your network's allowlist"
id: allowlist-domains
description: A list of Astro domains to add to your organization's network allowlist.
---

To use Astro in a network that requires you to allowlist new domains, make a request to allowlist the following domains on your network:

- `https://cloud.astronomer.io/`
- `https://api.astronomer.io/`
- `https://images.astronomer.cloud/`
- `https://auth.astronomer.io/`
- `https://updates.astronomer.io/`
- `https://install.astronomer.io/`
- `https://astro-<organization-short-name>.datakin.com/`
- `https://<organization-short-name>.astronomer.run/`

To locate the value for `<organization-short-name>` in the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. Copy the value listed under **Organization Short Name**.

To build and deploy Astro project images, additionally allowlist the following domains:

- `https://quay.io`
- `https://pip.astronomer.io`
- `https://install.astronomer.io`
- `https://raw.githubusercontent.com`
- `https://pypi.org`
