---
sidebar_label: "astro organization switch"
title: "astro organization switch"
id: astro-organization-switch
description: Reference documentation for astro organization switch.
hide_table_of_contents: true
---

Switch to a different Organization that you have access to in Astro.

## Usage

```sh
astro organization switch <your-organization-name-or-id>
```

You can switch to a different Organization only if you have already authenticated to your primary Organization using `astro login`. If you have not authenticated, run `astro login <base-domain>` first.

Switching to a different organization triggers a new browser login. If browser login does not work on your machine, use the `--login-link` flag with `organization switch`.

## Options

| Option               | Description                                                                                                        | Possible Values |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------- |
| `-l`, `--login-link` | Forces a user to manually access the Cloud UI to log in instead of opening the browser automatically from the Astro CLI. | None            |
| `<organization-id>` | The ID of the Organization to switch to. | Any valid Organization ID            |
| `<organization-name>` | The name of the Organization to switch into. Use as an alternative to `<organization-id>`. | Any valid Organization name            |

## Related Commands

- [astro organization list](cli/astro-organization-list.md)
- [astro context list](cli/astro-context-list.md)
- [astro context switch](cli/astro-context-switch.md)
