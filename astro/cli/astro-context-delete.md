---
sidebar_label: "astro context delete"
title: "astro context delete"
id: astro-context-delete
description: Delete an Astronomer product context.
hide_table_of_contents: true
---

Delete the locally stored information for a given Astronomer installation or base domain. After running this command, the domain for the installation that you specify will no longer appear when you run `astro context list`, and you will not be able to use `astro context switch` to switch to the installation.

If you re-authenticate to an installation that you previously deleted with this command, its information will again be available from `astro context list` and `astro context switch`.

## Usage

```sh
astro context delete <basedomain>
```

## Related Commands

- [astro context list](cli/astro-context-list.md)
- [astro context switch](cli/astro-context-switch.md)
