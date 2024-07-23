---
sidebar_label: "astro organization audit-logs"
title: "astro organization audit-logs"
id: astro-organization-audit-logs
description: Reference documentation for the astro organization audit-logs command.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::info

This command is only available on Astro.

:::

Astro audit logs record administrative activities and events in your Organization. You can use the audit logs to determine who did what, where, and when. This command allows you to export audit logs in a GZIP format for your entire Organization.

See [Export Astro audit logs](astro/audit-logs.md) for more information about exporting audit logs as well as a reference describing the different included fields.

## Usage

```bash
astro organization audit-logs <options>
```

Or

```bash
astro organization al <options>
```

## Options

| Option   | Description                                                                          | Valid Values |
| -------- | ------------------------------------------------------------------------------------ | ------------ |
| `export` | Export your Organization audit logs in GZIP. Requires Organization Owner permissions. | N/A          |

## Examples

Export your audit logs. Audit logs include information for all Workspaces in your Organization.

```bash

astro organization audit-logs export

```

## Related commands

- [`astro organization list`](cli/astro-organization-list.md)
- [`astro organization role list`](cli/astro-organization-role-list.md)