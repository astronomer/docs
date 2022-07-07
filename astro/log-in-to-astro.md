---
sidebar_label: 'Log in to Astro'
title: "Log in to Astro"
id: log-in-to-astro
description: Log in to Astro to access Astro features and functionality.
---

You can use the Cloud UI and the Astro CLI to view and modify your workspaces, clusters, environment variables, tasks, and users. Your user credentials need to be authenticated before you can use the Cloud UI or the Astro CLI. User authentication prevents unauthorized access to organizational data and ensures you have the correct permissions to perform specific tasks.

## Log in to the Cloud UI

In the Cloud UI you can create and manage workspaces, manage users, view your clusters, view lineage data, view task data, and view organization information.

1. Go to https://cloud.astronomer.io/ and create an Astronomer account.

2. Go to `https://account.astronomer.io/`, enter your email address, and then click **Continue**.

3. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**. 
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support.

## Log in to the Astro CLI

Using the Astro CLI you can [deploy code to Astro](deploy-code.md). You can also create and manage Deployments as you would in the Cloud UI.

1. Install and configure the Astro CLI. See [Get started with the Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

2. Run the following command:

    ```sh
    astro login
    ```
3. Enter your email address and press **Enter**.

4. Press **Enter** to connect your account to Astronomer.

    If this is your first time logging in, the Astronomer Authorize App dialog appears. Click **Accept** to allow Astronomer to access your profile and email and allow offline access.

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