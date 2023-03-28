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

astro login --token-login eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRmeDJYNVFNa2o3Q25ycVNyX1ZuTyJ9.eyJodHRwczovL2FzdHJvbm9tZXIuaW8vand0L2F1dGhfY29ubmVjdGlvbiI6eyJpZCI6ImNvbl9VazNBeTNDZGZ4Q1J5Z3BmIiwibmFtZSI6Imdvb2dsZS1vYXV0aDIiLCJzdHJhdGVneSI6Imdvb2dsZS1vYXV0aDIifSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmFzdHJvbm9tZXIuaW8vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTYzNjEzNTExNTY5MTg0ODg0MzEiLCJhdWQiOlsiYXN0cm9ub21lci1lZSIsImh0dHBzOi8vYXN0cm9ub21lci1wcm9kLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NzkzODc3NDAsImV4cCI6MTY3OTQ3NDE0MCwiYXpwIjoiWXE5YXRZWFRlZjZ0ZVpZSlhrd2xRbDZsWHBOS2t6OHUiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwicGVybWlzc2lvbnMiOltdfQ.mk5nkukONLjmayTL5RLytLAYO7w6PU-0PeCyNmyP7LNUBgPGlG22m3PzJ3jaLFRiIy-8sG0nJ_vmjPhBYYI_61WEFdVj3oGmIbHXc4gVlICaTn_MbbchVDFRVzp09akYcjWvD4TeXpIAp9Fc0-4b-FbCAxryETmS5W8JxyRscp1n9lOFia_yYgWXbXrETs9Guz_z6ErfYmGA71XiihJcy41ccGnb4Agf_aEn-Dwh3tCaKRJ-Mxb_yLKSZHKRyjNfZH9v_ZW1eDPfkF3oV0c4qFCIx8vHryK3q3h2jpsDw_r-_VmuNqSRxrY8ms0ixtq98PmjQ0vDvmiUYZPXnxBNOw
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
