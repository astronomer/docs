---
sidebar_label: 'Log in to Astro'
title: "Log in to Astro"
id: log-in-to-astro
description: Log in to Astro to access Astro features and functionality.
---

You can use the Cloud UI and the Astro CLI to view and modify your workspaces, clusters, environment variables, tasks, and users. Your user credentials need to be authenticated before you can use the Cloud UI or the Astro CLI.

## Log in to the Cloud UI

1. Go to `https://account.astronomer.io/`, enter your email address, and then click **Continue**.

2. Enter your password and click **Continue**, or select one of the authentication methods used by your organization.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support.

## Log in to the Astro CLI

Use the Astro CLI to [deploy code to Astro](deploy-code.md) and create and manage Deployments.

1. Install and configure the Astro CLI. See [Get started with the Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

2. Run the following command:

    ```sh
    astro login
    ```
3. Enter your email address and press **Enter**.

4. Press **Enter** to connect your account to Astronomer.

    If this is your first time logging in, the Astronomer Authorize App dialog appears. Click **Accept** to allow Astronomer to access your profile and email and allow offline access.

## Access a different base domain

A base domain or URL (Uniform Resource Locator) is the static element of a website address. For example, when you visit the Astronomer website, the address bar always displays `https://www.astronomer.io` no matter what page you access on the Astronomer website.

Every cluster is assigned a base domain. If your organization has multiple clusters, you can run Astro CLI commands to quickly move from one base domain to another. This can be useful when you need to move from Astro to an Astronomer Software installation.

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