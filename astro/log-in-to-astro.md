---
sidebar_label: 'Log in to Astro'
title: "Log in to Astro"
id: log-in-to-astro
---

<head>
  <meta name="description" content="Learn how you can use the Cloud user interface (UI) and the Astro command-line interface (CLI) to log in to Astro." />
  <meta name="og:description" content="Learn how you can use the Cloud user interface (UI) and the Astro command-line interface (CLI) to log in to Astro." />
</head>

You can use the Cloud UI and the Astro CLI to view and modify your Workspaces, Deployments, environment variables, tasks, and users. You need to authenticate your user credentials when you're using the Cloud UI or the Astro CLI for development on Astro.

## Prerequisites

- An Astronomer account.
- The [Astro CLI](cli/overview.md).
- An email address with a domain that matches the domain configured for your Organization.

## Log in to the Cloud UI

Go to `https://cloud.astronomer.io`, and select one of the following options to access the Cloud UI:

- To authenticate with single sign-on (SSO), enter your email and click **Continue**. If your Organization has SSO enabled, you'll be redirected to your identity provider authentication screen.
- To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**. If your Organization selects this log in option, you’ll receive an email invitation from your Organization Owner. You can't access the Organization without an invitation.
- To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**. If your Organization selects this log in option, you’ll receive an email invitation from your Organization Owner. You can't access the Organization without an invitation.

## Log in to the Astro CLI

Developing locally with the Astro CLI does not require an Astro account. This includes commands such as `astro dev start` and `astro dev pytest`. If you want to use functionality specific to Astro, including managing users and [deploying code](deploy-code.md), you must first log in to Astro with the Astro CLI.

Astronomer uses refresh tokens to make sure that you don’t need to log in to the Astro CLI every time you run a command.

1. In the Astro CLI, run the following command:

    ```sh
    astro login
    ```

2. Enter your email address and press **Enter**.

3. Press **Enter** to connect your account to Astronomer.

    If this is your first time logging in, the Astronomer Authorize App dialog appears. Click **Accept** to allow Astronomer to access your profile and email and allow offline access.

 4. Select one of the following options to access the Cloud UI:

    - Enter your email and click **Continue**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    Confirmation messages appear in the Cloud UI and in the Astro CLI indicating that your login was successful and that your computer is now connected. The name of your default Workspace in the Astro CLI also appears. To switch Workspace contexts after you log in, run [astro workspace switch](cli/astro-workspace-switch.md).

## Log in from a browserless system

The following options are available if you're unable to use a browser for authentication:

- Run `astro login -t` to log in with an authentication token. To obtain an authentication token on a separate machine, go to `https://cloud.astronomer.io/token`.
- Run `astro login -l` to retrieve a Cloud UI log in URL and then copy the URL. In a separate terminal session, run `curl -u <user-email>:<password> <returned-url>`. This option doesn't work if you're using an identity provider (IdP) for account authentication.

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

## Switch Organizations

You can belong to more than one Astro Organization. Having a role in an Organization does not guarantee access to the Organization through the Cloud UI. To access another Organization, you need to be able to authenticate with one of the enabled authentication methods.

1. Log in to the Cloud UI. By default, the Cloud UI opens the first Organization that you joined.
2. In the top navigation bar, click the name of your current Organization.
3. Click **Switch Organization**.
4. Select the Organization that you want to switch to.

## Reset your Astro password

If you log in to Astro with a text password, you can reset your password from the Cloud UI login screen.

1. Go to `cloud.astronomer.io`. If you are logged in, log out.
2. On the login screen, enter your email address, then click **Continue**.
3. Click **Forgot password?**

    ![Button to reset password on the Cloud UI login page](/img/docs/reset-password.png)

4. Confirm your user email address is correct, then click **Continue**. Astronomer sends an email with a password reset option to the user email address.
5. Follow the instructions in the email sent by Astronomer to reset your password. 