---
sidebar_label: 'Log in to Astro'
title: "Log in to Astro"
id: log-in-to-astro
description: Log in to Astro to access Astro features and functionality.
---

You can use the Cloud UI and the Astro CLI to view and modify your workspaces, deployments, environment variables, tasks, and users. You need to authenticate your user credentials when you're using the Cloud UI or the Astro CLI for development on Astro.

## Prerequisites 

- An Astronomer account.
- The [Astro CLI](cli/get-started.md).

## Log in to the Cloud UI

1. Go to `https://cloud.astronomer.io/login`, enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**. 
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Log in to the Astro CLI

Developing locally with the Astro CLI does not require an Astro account. This includes commands like `astro dev start` and `astro dev pytest`. If you want to use functionality specific to Astro, including managing users and [deploying code](deploy-code.md), you must first log in to Astro with the Astro CLI.

Astronomer uses refresh tokens to make sure that you don’t need to log in to the Astro CLI every time you run a command.

1. In the Astro CLI, run the following command:

    ```sh
    astro login
    ```
2. Enter your email address and press **Enter**.

3. Press **Enter** to connect your account to Astronomer.

    If this is your first time logging in, the Astronomer Authorize App dialog appears. Click **Accept** to allow Astronomer to access your profile and email and allow offline access.

 4. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**. 
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    Confirmation messages appear in the Cloud UI and in the Astro CLI indicating that your login was successful and that your computer is now connected. The name of your default Workspace in the Astro CLI also appears. To switch Workspace contexts after you log in, see [astro workspace switch](https://docs.astronomer.io/astro/cli/astro-workspace-switch).

## Access a different base domain

When you need to access Astro and Astronomer Software with the Astro CLI at the same time, you need to authenticate to each product individually by specifying a base domain for each Astronomer installation.

A base domain or URL is the static element of a website address. For example, when you visit the Astronomer website, the address bar always displays `https://www.astronomer.io` no matter what page you access on the Astronomer website.

For Astro users, the base domain is `cloud.astronomer.io`. For Astronomer Software, every cluster has a base domain that you must authenticate to in order to access it. If your organization has multiple clusters, you can run Astro CLI commands to quickly move from one base domain to another. This can be useful when you need to move from an Astronomer Software installation to Astro and are using the Astro CLI to perform actions on both accounts.

1. Run the following command to view a list of Astronomer base domains that you can access. Your current base domain is highlighted.

    ```
    astro context list
    ```
2. In the Astro CLI, run the following command to re-authenticate to the target base domain:

    ```
    astro login <basedomain>
    ```
3. Run the following command to switch to a different base domain:

    ```
    astro context switch <basedomain>
    ```