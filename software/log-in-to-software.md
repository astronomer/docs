---
sidebar_label: 'Log in to Astronomer Software'
title: "Log in to Astronomer Software"
id: log-in-to-software
description: Log in to Astronomer Software to access Astronomer Software features and functionality.
---

You can use the Astronomer Software UI and the Astro CLI to view and modify your workspaces, clusters, environment variables, tasks, and users. Your user credentials need to be authenticated before you can use the Astronomer Software UI or the Astro CLI.

## Prerequisites 

- An Astronomer account.
- The [Astro CLI](cli/get-started.md)

## Log in to the Astronomer Software UI

1. Go to `<basedomain>.astronomer.io`.

2. Select one of the following options to access the Astronomer Software UI:
    
    - Enter your username and password and click **Log in**.
    - To authenticate with with your Auth0 account, click **Log in with Auth0**, and then follow the prompts.
    - To authenticate with your Google account, click **Log in with Google**, choose an account, enter your username and password, and then click **Sign In**.
    - To authenticate with your Okta account, click **Log in with Okta**, enter your username and password, and then click **Sign In**. 
    - To authenticate with with your custom Oauth account, click **Log in with Custom Oauth**, and then follow the prompts.
    - To authenticate with with your Azure AD account, click **Log in with Azure AD**, and then follow the prompts.
    - To authenticate with your internal Okta account, click **Log in with InternalOkta**, enter your username and password, and then click **Sign In**. 
    - To authenticate with your GitHub account, click **Log in with GitHub**, and then follow the prompts.
    
## Log in to the Astro CLI

Use the Astro CLI to [deploy code to Astro](https://docs.astronomer.io/astro/deploy-code) and create and manage Deployments. Astronomer uses refresh tokens to make sure that you don’t need to log in to the Astro CLI every time you run a command.

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

When you need to access Astro and Astronomer Software with the Astro CLI at the same time, you need to authenticate to each product individually by specifying a base domain for each Astronomer installation.

A base domain or URL is the static element of a website address. For example, when you visit the Astronomer website, the address bar always displays `https://www.astronomer.io` no matter what page you access on the Astronomer website.

For Astro users, the base domain is `cloud.astronomer.io`. For Astronomer Software, every cluster has a base domain that you must authenticate to in order to access it. If your organization has multiple clusters, you can run Astro CLI commands to quickly move from one base domain to another. This can be useful when you need to move from an Astronomer Software installation to Astro and are using the Astro CLI to perform actions on both accounts.

You can authenticate to multiple domains from a single base domain. You run `astro login` to authenticate to a base domain, and then run the `astro context switch <basedomain>` command to switch to a different Astronomer installation.

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