---
sidebar_label: 'astro login'
title: 'astro login'
id: astro-login
description: Reference documentation for astro login.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Authenticate to Astro. After you run this command, the CLI prompts you for your login email address. Using the provided email address, the CLI assumes your organization and redirects you to a web browser where you can log in to the Cloud UI. After you log in, the CLI automatically recognizes this and authenticates your account.

## Usage


```sh
astro login
```

## Options

| Option                | Description                                                                                                            | Possible Values |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------- |
| `-l`, `--login-link`  | The CLI will provide you with a URL to the log in page of the Cloud UI instead of automatically opening your browser. Use this link to manually authenticate | None            |
| `-t`, `--token-login` | Log in by manually specifying an authentication token. Use this command when you can't access a web browser from the machine running the CLI | A valid authentication token from `cloud.astronomer.io/token` |

## Examples

```sh
astro login
# The CLI automatically opens the Cloud UI in a web browser, which prompts you to log in.

astro login --login-link
# The CLI provides a link to the Cloud UI that you can manually open in a web browser.

astro login --token-login <auth-token>
# Copy a generated token from the UI (cloud.astronomer.io/token) and use it with this command for browserless login.
```

</TabItem>
<TabItem value="software">

Authenticate to Astronomer Software. After you run this command, the CLI prompts you to either enter a username and password or retrieve an OAuth token from `<basedomain>/token`.

## Usage


```sh
astro login <basedomain>
```

## Options

| Option                | Description                                                                              | Possible Values |
| --------------------- | ---------------------------------------------------------------------------------------- | --------------- |
| `--l`, `--login-link` | Generate a login link to login on a separate device for cloud CLI login                  | None            |
| `-o`, `--oauth`       | Skip the prompt for local authentication, proceed directly to OAuth token authentication | None            |


## Examples

```sh
astro login mycompany.astromomer.io
# The CLI prompts you for a username and password, or to leave the prompt empty for OAuth authentication

astro login mycompany.astromomer.io -o
# The CLI does not prompt you for a username and password and instead directly prompts you for an OAuth login token
```


</TabItem>
</Tabs>

### Related commands

- [`astro logout`](cli/astro-logout.md)
- [`astro deploy`](cli/astro-deploy.md)
