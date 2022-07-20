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
| `--l`, `--login-link` | Force the user to manually access the Cloud UI to log in instead of opening the browser automatically from the CLI.           | ``|
| `-t`, `--token-login` | Force the user to manually enter a token generated in the Cloud UI. This flag is used primarily for browserless login.                                        | ``    |

## Examples

```sh
astro login
# The CLI automatically opens the Cloud UI in a web browser, which prompts you to log in.

astro login --login-link
# The CLI provides a link to the Cloud UI that you can manually open in a web browser.

astro login --token-login
# The CLI provides a link to the Cloud UI that you can manually open in a web browser. You then copy a generated token from the UI and enter it in the CLI. For a browserless login, you can open the link and copy the token on a separate machine from the one running the Astro CLI.
```


## Related Commands

- [`astro logout`](cli/astro-logout.md)
- [`astro deploy`](cli/astro-deploy.md)
