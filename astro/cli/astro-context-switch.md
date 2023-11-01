---
sidebar_label: "astro context switch"
title: "astro context switch"
id: astro-context-switch
description: Switch to an Astronomer product context.
hide_table_of_contents: true
---

Switch to a different Astronomer installation. You can switch to a given Astronomer installation only if you have authenticated to it at least once using `astro login`. If you have not authenticated, run `astro login <base-domain>` instead.

Note that after switching to a different Astronomer installation, you might have to re-authenticate to the installation using `astro login`.  

## Usage

```sh
astro context switch <basedomain>
```

## Related Commands

- [astro context list](cli/astro-context-list.md)
- [astro context delete](cli/astro-context-delete.md)
