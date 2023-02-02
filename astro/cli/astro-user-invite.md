---
sidebar_label: 'astro user invite'
title: 'astro user invite'
id: astro-user-invite
description: Reference documentation for astro user invite.
hide_table_of_contents: true
---

Invite a new user to the Organization you're currently authenticated to. You must have Organization Owner permissions to run this command. This command is identical to to [`astro organization user invite`](cli/astro-organizatin.md).

## Usage

```sh
astro user invite <user-email> <flags>
```

## Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-r`, `--role` | Force the user to manually access the Cloud UI to log in instead of opening the browser automatically from the CLI.           | `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, `ORGANIZATION_OWNER`|

## Examples

```sh
$ astro user invite
# CLI prompts you for a user's email and assigns them the `ORGANIZATION_MEMBER` role by default

$ astro user invite user@company.com --role ORGANIZATION_BILLING_ADMIN
# Invite a user as an Organization Billing Admin
```

## Related Commands

- [`astro login`](cli/astro-login.md)