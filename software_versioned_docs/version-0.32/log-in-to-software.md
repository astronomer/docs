---
sidebar_label: 'Log in to Astronomer Software'
title: "Log in to Astronomer Software"
id: log-in-to-software
description: Log in to Astronomer Software to access Astronomer Software features and functionality.
---

You can use the Astronomer Software UI and the Astro CLI to view and modify your Workspaces, Deployments, environment variables, tasks, and users. You need to authenticate your user credentials when you're using the Astronomer Software UI or the Astro CLI for development on Astro.

## Prerequisites

- An Astronomer account.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Log in to the Astronomer Software UI

1. Go to `<basedomain>.astronomer.io`.

2. Log in to the Software UI using one of the authentication methods that has been configured by your organization. To integrate an identity provider (IdP) with Astronomer Software, see [Integrate an auth system on Astronomer Software](integrate-auth-system.md).

## Log in to the Astro CLI

Developing locally with the Astro CLI does not require an Astro account. This includes commands such as `astro dev start` and `astro dev pytest`. If you want to use functionality specific to Astronomer Software, including managing users and [deploying DAGs](deploy-cli.md), you must first log in to Astro with the Astro CLI.

1. In the Astro CLI, run the following command:

    ```sh
    astro login <basedomain>
    ```
2. Enter your username and password or use an OAuth token for authentication:

    - Press **Enter**.
    - Copy the URL in the command prompt, open a browser, paste the URL in the address bar, and then press **Enter**. If you're not taken immediately to the Astronomer Auth Token page, log in to Astronomer Software, paste the URL in the address bar, and press **Enter**.
    - Copy the OAuth token, paste it in the command prompt after **oAuth Token**, and then press **Enter**.

    :::info

    If you can't enter your password in the command prompt, your organization is using an alternative authentication method. Contact your administrator, or use an OAuth token for authentication.

    :::     

## Access a different base domain

When you need to access multiple installations of Astronomer Software with the Astro CLI at the same time or you need to use Astro and Astronomer Software at the same time, you need to authenticate to each cluster individually by specifying its base domain.

A base domain or URL is the static element of a website address. For example, when you visit the Astronomer website, the address bar always displays `https://www.astronomer.io` no matter what page you access on the Astronomer website.

For Astronomer Software, every cluster has a base domain that you must authenticate to in order to access it. If your organization has multiple clusters, you can run Astro CLI commands to quickly move from one base domain to another. This can be useful when you need to move from an Astronomer Software installation to Astro and are using the Astro CLI to perform actions on both accounts.

1. Run the following command to view a list of base domains for all Astronomer installations that you can access and to confirm your default base domain:

    ```
    astro context list
    ```

2. In the Astro CLI, run the following command to re-authenticate to the target base domain:

    ```
    astro login
    ```

3. Run the following command to switch to a different base domain:

    ```
    astro context switch <basedomain>
    ```
