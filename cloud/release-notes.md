---
sidebar_label: 'Astronomer Cloud'
title: 'Astronomer Cloud Release Notes'
id: release-notes
description: A real-time reference of the latest features and bug fixes in Astronomer Cloud.
---

## Overview

Astronomer is committed to continuous delivery of both features and bug fixes to Astronomer Cloud. To keep your team up to date on what's new, this document will provide a regular summary of all changes officially released to Astronomer Cloud.

If you have any questions or a bug to report, don't hesitate to reach out to [Astronomer Support](https://support.astronomer.io).

**Latest Runtime Version**: 4.0.8 ([Release notes](runtime-release-notes.md))

**Latest CLI Version**: 1.0.0 ([Release notes](cli-release-notes.md))

## February 3, 2022

### Support for Third-Party Identity Providers

You can now integrate both Azure AD and Okta as identity providers (IdPs) for federated authentication on Astronomer Cloud. By setting up a third-party identity provider, a user in your organization will be automatically logged in to Astronomer Cloud if they're already logged in via your IdP. By adding new Astronomer users through your IdP's own user management system, Workspace admins can automatically add new users to their Workspace without those users needing to individually sign up for Astronomer.

For more information about this feature read [Set Up an Identity Provider](configure-idp.md).

### Support for the Astronomer Cloud CLI

The Astronomer Cloud CLI (`astrocloud`) is now generally available as the official command-line tool for Astronomer Cloud. It is a direct replacement of the previously released `astro` executable and comes with various significant improvements. We encourage all customers to upgrade.

For more information on the Astronomer Cloud CLI, see [CLI Release Notes](cli-release-notes.md). For install instructions, read [Install the CLI](install-cli.md).

### Multiple Authentication Methods for a Single User Account

Astronomer now supports multiple authentication methods for a single user account. This means that as long as you're using a consistent email address, you now have the flexibility to authenticate with GitHub, Google, username/password, and/or [an external identity provider (idP)](configure-idp.md) at any time. Previously, a single user account could only be associated with one authentication method, which could not be changed after the account was created.

This also means that all Organizations now have GitHub, Google, and username/password authentication methods enabled by default for all users.

### Additional Improvements

- Changed the default RDS instance type for new Clusters from `db.r5.xlarge` to `db.r5.large`, which represents a monthly cost reduction of ~50% for newly provisioned clusters. Customers with existing clusters will need to request a downscale via [Astronomer Support](https://support.astronomer.io)

## January 13, 2022

### Identity-Based Login Flow

Astronomer Cloud now utilizes an identity-based login flow for all users. When you first log in via the Astronomer UI, you now only need to enter the email address for your account. Astronomer assumes your Organization and brings you directly to your Astronomer Organization's login screen.

This change serves as a foundation for future SSO and authentication features. In upcoming releases, users will be able to authenticate via custom identity providers like Okta and Azure Active Directory.

### Additional Improvements

- Significant improvements to the load times of various Astronomer UI pages and and elements.
- In the Astronomer UI, the tooltips in the **Resource Settings** section of a Deployment's page now show the definition of 1 AU. This should make it easier to translate AU to CPU and Memory.
- Scheduler logs in the Astronomer UI no longer show `DEBUG`-level logs.
- To ensure that all Workers have enough resources to run basic workloads, you can no longer allocate less than 10 AU to **Worker Resources**.

## January 6, 2022

### Improvements to "Scheduler Logs" in the Astronomer UI

The **Scheduler Logs** tab in the Astronomer UI has been updated to make logs easier to read, separate, and parse. Specifically:

- You can now filter logs by type (`DEBUG`, `INFO`, `WARN`, and `ERROR`).
- The page now shows logs for the past 24 hours instead of the past 30 minutes.
- The page now shows a maximum of 500 logs instead of a lower maximum.
- When looking at a Deployment's logs, you can return to the Deployment's information using the **Deployment Details** button.

![Logs page in the UI](/img/release-notes/log-improvements.png)

### Removal of Worker Termination Grace Period

The **Worker Termination Grace Period** setting is no longer available in the Astronomer UI or API. Previously, users could set this to anywhere between 1 minute and 24 hours per Deployment. This was to prevent running tasks from being interrupted by a code push. Today, however, existing Celery Workers don't have to terminate in order for new Workers to spin up and start executing tasks. Instead, existing Workers will continue to execute running tasks while a new set of Workers gets spun up concurrently to start executing most recent code.

To simplify Deployment configuration and reflect current functionality:

- The Worker Termination Grace Period was removed from the Astronomer UI
- This value was permanently set to 24 hours for all Deployments on Astronomer Cloud

This does not change or affect execution behavior for new or existing Deployments. For more information, read [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Additional Improvements

- Removed _Kubernetes Version_ column from the **Clusters** table. This value was previously inaccurate and is not needed. The Kubernetes version of any particular Astronomer Cluster is set and modified exclusively by Astronomer as part of our managed service.

## December 16, 2021

### View Scheduler Error Logs from the Astronomer UI

The new **Logs** tab in the Astronomer UI shows Scheduler error and warning logs for all Deployments in your Workspace. When you select a Deployment in this menu, all error logs generated over the last 30 minutes appear in the UI.

![Logs page in the UI](/img/release-notes/logs-page.png)

To access logs directly for a given Deployment, click the new **Logs** button on the Deployment's page or in the **Deployments** table.

![Logging direct access button](/img/release-notes/logs-button.png)

For more information on how to view logs, read [Deployment Logs](scheduler-logs.md).

### Bug Fixes

Fixed various bugs in the Astronomer UI to better handle nulls and unknowns in Deployment metrics

## December 9, 2021

### Additional Improvements

- In the Astronomer Cloud UI, the **Open Airflow** button now shows more specific status messages when a Deployment's Airflow UI is inaccessible.

### Bug Fixes

- Fixed Deployment table scrolling and alignment issues in the UI

## December 6, 2021

### New "Usage" Tab in the Astronomer UI

Total task volume for your Organization is now available in a new **Usage** tab in the Astronomer Cloud UI. Astronomer Cloud is priced based on successful task runs, so this view can help you monitor both Astronomer cost as well as Airflow usage in aggregate and between Deployments.

![Usage tab in the Astronomer UI](/img/docs/usage.png)

For more information about the **Usage** tab, read [Deployment Metrics](deployment-metrics.md#usage).

### New AWS Regions Available

You can now create new Clusters in:

- `us-west-1`
- `ap-northeast-1 `
- `ap-southeast-1`
- `ap-northeast-2`
- `ap-southeast-2`
- `ap-south-1`
- `us-west-1`
- `us-west-2`

For a full list of AWS regions supported on Astronomer Cloud, see [AWS Resource Reference](https://docs.astronomer.io/resource-reference-aws.md#aws-region).

### Additional Improvements

- You can now see your Deployment's **Namespace** in the **Deployments** menu and on the Deployment information screen in the Astronomer UI. Namespace is a required argument to run tasks with the KubernetesPodOperator. It is also required to submit an issue to [Astronomer Support](https://support.astronomer.io).

    ![Deployment namespace available on a Deployment's information page](/img/docs/namespace.png)

- The Astronomer UI now shows a warning if you attempt to exit Environment Variable configuration without saving your changes.
- A Deployment's health status is now based on the health of both the Airflow Webserver and Scheduler. Previously, a Deployment's health status was only based on the health of the Webserver. Now, the Astronomer UI will show that your Deployment is "Healthy" only if both components are running as expected.

### Bug Fixes

- The Astronomer UI now has error handling for attempts to access a Deployment that does not exist.
- If you attempt to modify an existing secret environment variable, the **Value** field is now blank instead of showing hidden characters.

### Data Plane Improvements

- Amazon EBS volumes have been upgraded from gp2 to [gp3](https://aws.amazon.com/about-aws/whats-new/2020/12/introducing-new-amazon-ebs-general-purpose-volumes-gp3/) for improved scale and performance.
- EBS volumes and S3 buckets are now encrypted by default.
- The ability to enable public access to any Amazon S3 bucket on an Astronomer Cloud data plane is now blocked per a new AWS account policy. Previously, public access was disabled by default but could be overridden by a user creating a new S3 bucket with public access enabled. This AWS account policy could be overriden by AWS account owners, but Astronomer strongly recommends against doing so.

## November 19, 2021

### Secret Environment Variables

You can now set secret environment variables via the Astronomer Cloud UI. The values of secret environment variables are hidden from all users in your Workspace, making them ideal for storing sensitive information related to your Astronomer projects.

![Secrets checkbox available in the Astronomer UI](/img/release-notes/secrets-feature.png)

For more information, read [Set Environment Variables via the Astronomer UI](environment-variables.md#set-environment-variables-via-the-astronomer-ui).

### Additional Improvements

- You can now create new Clusters in AWS `sa-east-1`.
- Extra whitespace at the end of any environment variable that is set via the Astronomer UI is now automatically removed to ensure the variable is passed correctly.

## November 11, 2021

### Deployment Metrics Dashboard

In the Astronomer UI, your Deployment pages now show high-level metrics for Deployment health and performance over the past 24 hours.

<div class="text--center">
  <img src="/img/docs/deployment-metrics.png" alt="New metrics in the Cloud UI" />
</div>

For more information on this feature, read [Deployment Metrics](deployment-metrics.md).

### Bug Fixes

- Resolved a security vulnerability by setting `AIRFLOW__WEBSERVER__COOKIE_SECURE=True` as a global environment variable

## November 5, 2021

### Bug fixes

- Fixed an issue where a new user could not exit the Astronomer UI "Welcome" screen if they hadn't yet been invited to a Workspace

## October 29, 2021

### Astronomer UI Redesign

The Astronomer UI has been redesigned so that you can more intuitively manage Organizations, Workspaces, and your user profile.

To start, the homepage is now a global view. From here, you can now see all Workspaces that you have access to, as well as information and settings related to your **Organization**: a collection of specific users, teams, and Workspaces. Many features related to Organizations are coming soon, but the UI now better represents how Organizations are structured and what you can do with them in the future:

<div class="text--center">
  <img src="/img/docs/ui-release-note1.png" alt="New global menu in the UI" />
</div>

You can now also select specific Workspaces to work in. When you click in to a Workspace, you'll notice the lefthand menu bar is now entirely dedicated to Workspace actions:

- The Rocket icon brings you to the **Deployments** menu.
- The People icon brings you to the **Workspace Access** menu.
- The Gear icon brings you to the **Workspace Settings** menu.

To return to the global menu, you can either click the Astronomer "A" or click the Workspace name to produce a dropdown menu with your Organization.

<div class="text--center">
  <img src="/img/docs/ui-release-note2.png" alt="New Workspace menu in the UI" />
</div>

All user configurations can be found by clicking your user profile picture in the upper righthand corner of the UI. From the dropdown menu that appears, you can both configure user settings and access other Astronomer resources such as documentation and the Astronomer Registry.

<div class="text--center">
  <img src="/img/docs/ui-release-note3.png" alt="New profile menu in the UI" />
</div>

### Additional Improvements

- You can now create new Clusters in `us-east-2` and `ca-central-1`.
- In the Deployment detail page, **Astronomer Runtime** now shows the version of Apache Airflow that the Deployment's Astronomer Runtime version is based on.
- You can now create or modify an existing Astronomer Cluster to run any size of the `t2`,`t3`, `m5`, or `m5d` [AWS EC2 instances](resource-reference-aws.md).

### Bug Fixes

- Fixed an issue where a new Deployment's health status did not update unless you refreshed the Cloud UI

## October 28, 2021

### Bug Fixes

- Fixed an issue where you couldn't push code to Astronomer with a Deployment API Key via a CI/CD process
- Fixed an issue where you couldn't update or delete an API key after creating it

## October 25, 2021

### Additional Improvements

- When deleting a Deployment via the UI, you now have to type the name of the Deployment in order to confirm its deletion.

### Bug Fixes

- Fixed an issue where you could not access Airflow's REST API with a Deployment API key
- Fixed an issue where calling the `imageDeploy` API mutation with a Deployment API key would result in an error

## October 15, 2021

### Additional Improvements

- When creating a new Deployment, you can now select only the latest patch version for each major version of Astronomer Runtime.
- When creating a new Deployment in the Astronomer UI, the cluster is pre-selected if there is only one cluster available.
- The name of your Astronomer Deployment now appears on the main DAGs view of the Airflow UI.
- You can now see the health status for each Deployment in your Workspace on the table view of the **Deployments** page in the Astronomer UI:

   <div class="text--center">
     <img src="/img/docs/health-status-table.png" alt="Deployment Health statuses visible in the Deployments table view" />
   </div>

- In the Astronomer UI, you can now access the Airflow UI for Deployments via the **Deployments** page's card view:

    <div class="text--center">
      <img src="/img/docs/open-airflow-card.png" alt="Open Airflow button in the Deployments page card view" />
    </div>

- The Astronomer UI now saves your color mode preference.

## October 1, 2021

### Additional Improvements

- In the Astronomer UI, the **Open Airflow** button is now disabled until the Airflow UI of the Deployment is available.
- Workspace Admins can now edit user permissions and remove users within a given Workspace.

## September 28, 2021

:::danger

This release introduces a breaking change to code deploys via the Astronomer Cloud CLI. Starting on September 28, you must upgrade to v1.0.0 of the CLI to deploy code to Astronomer. [CI/CD processes](ci-cd.md) enabled by Deployment API keys will continue to work and will not be affected. For more information, read the [CLI release notes](cli-release-notes.md).

:::

### Additional Improvements

- In the Astronomer UI, a new element on the Deployment information screen shows the health status of a Deployment. Currently, a Deployment is considered unhealthy if the Airflow Webserver is not running and the Airflow UI is not available:

    <div class="text--center">
      <img src="/img/docs/deployment-health.png" alt="Deployment Health text in the UI" />
    </div>

- The documentation home for Astronomer Cloud has been moved to `docs.astronomer.io`, and you no longer need a password to access the page.

### Bug Fixes

- The Astronomer UI now correctly renders a Deployment's running version of Astronomer Runtime.

## September 17, 2021

### Support for Deployment API Keys

Astronomer Cloud now officially supports Deployment API keys, which you can use to automate code pushes to Astronomer and integrate your environment with a CI/CD tool such as GitHub Actions. For more information on creating and managing Deployment API keys, see [Deployment API keys](api-keys.md). For more information on using Deployment API keys to programmatically deploy code, see [CI/CD](ci-cd.md). Support making requests to Airflow's REST API using API keys is coming soon.

## September 3, 2021

### Bug Fixes

- Added new protections to prevent S3 remote logging connections from breaking
- Fixed an issue where environment variables with extra spaces could break a Deployment
- Fixed an issue where Deployments would occasionally persist after being deleted via the UI
- In the UI, the **Organization** tab in **Settings** is now hidden from non-admin users
- In the UI, the table view of Deployments no longer shows patch information in a Deployment's **Version** value

## August 27, 2021

### Additional Improvements

- You can now remain authenticated to Astronomer across multiple active browser tabs. For example, if your session expires and you re-authenticate to Astronomer Cloud on one tab, all other tabs running Astronomer Cloud will be automatically updated without refreshing.
- If you try to access a given page on Astronomer Cloud while unauthenticated and reach the login screen, logging in now brings you to the original page you requested.

### Bug Fixes

- Fixed an issue where an incorrect total number of team members would appear in the **People** tab

## August 20, 2021

### Support for the Airflow REST API

You can now programmatically trigger DAGs and update your Airflow Deployments on Astronomer by making requests to Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html). Currently this feature works only with temporary tokens, which are available at `cloud.astronomer.io/token`. Support for Deployment API keys is coming soon. For more information on using this feature, read [Airflow API](airflow-api.md).

### Additional Improvements

- Set `AIRFLOW_HOME = 'usr/local/airflow'` as a permanent global environment variable
- In the Astronomer UI, long environment variable keys and values now wrap to fit the screen
- Added links for the Astronomer Registry and certification courses to the left-hand navbar
- Moved the **Teams** and **People** tabs into the **Settings** page of the UI
- Added **Cluster** information to the metadata section of a Deployment's information page in the UI
- Renamed various UI elements to better represent their functionality
- Increased the maximum **Worker Termination Grace Period** from 600 minutes (10 hours) to 1440 minutes (24 hours)

### Bug Fixes

- The left-hand navbar in the UI is no longer cut off when minimized on smaller screens
- Fixed an issue where you could not delete a Workspace via the UI
- Fixed an issue where expired tokens would occasionally appear on `cloud.astronomer.io/token`
- Fixed an issue where the UI would initially load an inaccurate number of team members on the **Access** page
- Fixed alphabetical sorting by name in the **People** tab in the UI
- Removed placeholder columns from various tables in the UI

## August 6, 2021

### Additional Improvements

- Informational tooltips are now available on the **New Deployment** page.

### Bug Fixes

- Fixed an issue where adding a user to a Workspace and then deleting the user from Astronomer made it impossible to create new Deployments in that Workspace
- Improved error handling in the Airflow UI in cases where a user does not exist or does not have permission to view a Deployment

## July 30, 2021

### Improvements

- Increased the limit of **Worker Resources** from 30 AU to 175 AU (17.5 CPU, 65.625 GB RAM). If your tasks require this many resources, reach out to us to make sure that your Cluster is sized appropriately
- Collapsed the **People** and **Teams** tabs on the left-hand navigation bar into a single **Access** tab
- Added a **Cluster** field to the Deployments tab in the Astronomer UI. Now, you can reference which Cluster each of your Deployments is in
- Replaced our white "A" favicon to one that supports color mode
- Informational tooltips are now available in **Deployment Configuration**

### Bug Fixes

- Fixed an issue where a deleted user could not sign up to Astronomer Cloud again
- Removed Deployment-level user roles from the Astronomer UI. Support for them coming soon
- Fixed an issue where a newly created Deployment wouldn't show up on the list of Deployments in the Workspace
