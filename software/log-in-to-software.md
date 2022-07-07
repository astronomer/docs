---
sidebar_label: 'Log in to Astronomer Software'
title: "Log in to Astronomer Software"
id: log-in-to-software
description: Log in to Astronomer Software to access Astronomer Software features and functionality.
---

You can use the Astronomer Software UI and the Astro CLI to view and modify your workspaces, clusters, environment variables, tasks, and users. Your user credentials need to be authenticated before you can use the Astronomer Software UI or the Astro CLI. User authentication prevents unauthorized access to organizational data and ensures you have the correct permissions to perform specific tasks.

## Log in to the Astronomer Software UI

In the Astronomer Software UI you can create and manage workspaces, manage users, add and remove environment variables, view metrics, and view logs.

1. Go to https://cloud.astronomer.io/ and create an Astronomer account.

2. Open a browser and go to `<basedomain>.astronomer.io`.

3. Select one of the following options to access the Astronomer Software UI:

    - To authenticate with with your Auth0 account, click **Log in with Auth0**, and then follow the prompts.
    - To authenticate with your Google account, click **Log in with Google**, choose an account, enter your username and password, and then click **Sign In**.
    - To authenticate with your Okta account, click **Log in with Okta**, enter your username and password, and then click **Sign In**. 
    - To authenticate with with your custom Oauth account, click **Log in with Custom Oauth**, and then follow the prompts.
    - To authenticate with with your Azure AD account, click **Log in with Azure AD**, and then follow the prompts.
    - To authenticate with your internal Okta account, click **Log in with InternalOkta**, enter your username and password, and then click **Sign In**. 
    - To authenticate with your GitHub account, click **Log in with GitHub**, and then follow the prompts.
    - Enter your username and password and click **Log in**.

## Log in to the Astro CLI

Use the Astro CLI to [deploy code to Astro](deploy-code.md) and create and manage Deployments.

1. Install and configure the Astro CLI. See [Get started with the Astro CLI](https://docs.astronomer.io/software/install-cli).

2. Run the following command:

    ```sh
    astro login <basedomain>
    ```
3. Enter your email address and press **Enter**.

4. Press **Enter** to connect your account to Astronomer.

## Access a different base domain

A base domain or URL (Uniform Resource Locator) is the static element of a website address. For example, when you visit the Astronomer website, the address bar always displays https://www.astronomer.io no matter what page you access on the Astronomer website. The base domain or URL allows computers to quickly identify and access resources in other domains.

Every cluster is assigned a base domain. If your organization has multiple clusters, you can run Astro CLI commands to quickly move from one base domain to another. This can be useful when you're authenticated on one cluster, but you need to perform tasks on another cluster.

You can authenticate to multiple domains from a single base domain. You run the `astro login x` command to authenticate to a base domain, and then run the `astro context switch x` command to define the default base domain on your computer. 

1. In the Astro CLI, run the following command to re-authenticate to the target base domain:

    ```
    astro login
    ```
2. Run the following command to define the default base domain on your computer:

    ```
    astro context switch <basedomain>
    ```

3. Run the following command to view a list of base domains for all Astronomer installations that you can access and to confirm your default base domain:

    ```
    astro context list
    ```