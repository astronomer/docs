---
sidebar_label: 'astro login'
title: 'astro login'
id: astro-login
description: Reference documentation for astro login.
---

Authenticate to Astro. After you run this command, the CLI prompts you for your login email address. Using the provided email address, the CLI assumes your organization and redirects you to a web browser where you can log in via the Cloud UI. Once you are logged in via the web browser, the CLI automatically recognizes this and authenticates to your account.

## Usage

```sh
astro login
```

## Options

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `--l`, `--login-link` | Get a login link to copy and paste into a browser to skip automatic browser login           | N/A |
| `-t`, `--token-login` | Login with a token for browserless Astro login                                          | N/A    |

## Related Commands

- [`astro logout`](cli/astro-logout.md)
- [`astro deploy`](cli/astro-deploy.md)
