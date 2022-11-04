---
sidebar_label: "astro organization switch"
title: "astro organization switch"
id: astro-organization-switch
description: Reference documentation for astro organization switch.
hide_table_of_contents: true
---

Switch to a different Organization. 

## Usage

```sh
astro organization switch <your-organization-name-or-id>
```

You can switch to a different Organization only if you have already authenticated to your primary Organization using `astro login`. If you have not authenticated, run `astro login <base-domain>` first.

Switching to a different organization will trigger a new browser login. If browser login does not work on your machine, use the `--login-link` flag with `organization switch`.

## Options

| Option               | Description                                                                                                        | Possible Values |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------- |
| `-l`, `--login-link` | Force the user to manually access the Cloud UI to log in instead of opening the browser automatically from the CLI | None            |

## Related Commands

- [astro organization list](cli/astro-organization-list.md)
- [astro context list](cli/astro-context-list.md)
- [astro context switch](cli/astro-context-switch.md)



