---
sidebar_label: "astro organization switch"
title: "astro organization switch"
id: astro-organization-switch
description: Reference documentation for astro organization switch.
hide_table_of_contents: true
---

Switch to a different Organizaton. You can switch to a different organization only if you have already authenticated to your primary organization using `astro login`. If you have not authenticated, run `astro login <base-domain>` first.

Note that switching to a different organization will trigger a new browser login. If browser login does not work on your machine use the `--login-link` flag with `organization switch`.

## Usage

```sh
astro organization switch <organization name or id>
```

## Related Commands

- [astro organization list](cli/astro-organization-list.md)
- [astro context delete](cli/astro-context-delete.md)
