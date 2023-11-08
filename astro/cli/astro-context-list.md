---
sidebar_label: "astro context list"
title: "astro context list"
id: astro-context-list
description: List available Astronomer product contexts.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

View a list of domains for all Astronomer installations that you have access to. An Astronomer installation will appear on this list if you have authenticated to it at least once using `astro login`.

If you're an Astro user, you should only see `astronomer.io` on this list.

## Usage

```sh
astro context list
```

## Output

| Output | Description                                                      | Data Type |
| ------ | ---------------------------------------------------------------- | --------- |
| `NAME` | The names of the domains that you have logged into from the CLI. | String    |

## Related Commands

- [astro context switch](cli/astro-context-switch.md)
- [astro context delete](cli/astro-context-delete.md)
