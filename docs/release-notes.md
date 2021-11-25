---
sidebar_label: 'Astronomer Cloud'
title: 'Astronomer Cloud Release Notes'
id: release-notes
---

## Overview

Astronomer is committed to continuous development of Astronomer Cloud. As you grow with us, expect to see bug fixes and improved functionality on a regular basis. To keep your team updated, this document will provide a weekly summary of all changes made and released to Astronomer Cloud.

If you have any questions or a bug to report, don't hesitate to reach out to us via Slack or Intercom. We're here to help.

**Latest Runtime Version**: 4.0.4 ([Release notes](runtime-release-notes))

**Latest CLI Version**: 1.0.3 ([Release notes](cli-release-notes))

## November 19, 2021

### Secret Environment Variables

You can now set secret environment variables via the Astronomer Cloud UI. The values of secret environment variables are hidden from all users in your Workspace, making them ideal for storing sensitive information related to your Astronomer projects. For more information, read [Set Environment Variables via the Astronomer UI](https://docs.astronomer.io/environment-variables#set-environment-variables-via-the-astronomer-ui).

### Minor Improvements

- You can now create new Clusters in AWS `sa-east-1`.
- Extra whitespace at the end of any environment variable that is set via the Astronomer UI is now automatically removed to ensure the variable is passed correctly.

## November 11, 2021

### Deployment Metrics Dashboard

In the Astronomer UI, your Deployment pages now show high-level metrics for Deployment health and performance over the past 24 hours.

<div class="text--center">
  <img src="/img/docs/deployment-metrics.png" alt="New metrics in the Cloud UI" />
</div>

For more information on this feature, read [Deployment Metrics](deployment-metrics).

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

### Minor Improvements

- You can now create new Clusters in `us-east-2` and `ca-central-1`.
- In the Deployment detail page, **Astronomer Runtime** now shows the version of Apache Airflow that the Deployment's Astronomer Runtime version is based on.
- You can now create or modify an existing Astronomer Cluster to run any size of the `t2`,`t3`, `m5`, or `m5d` [AWS EC2 instances](resource-reference-aws).

### Bug Fixes

- Fixed an issue where a new Deployment's health status did not update unless you refreshed the Cloud UI

## October 28, 2021

### Bug Fixes

- Fixed an issue where you couldn't push code to Astronomer with a Deployment API Key via a CI/CD process
- Fixed an issue where you couldn't update or delete an API key after creating it

## October 25, 2021

### Minor Improvements

- When deleting a Deployment via the UI, you now have to type the name of the Deployment in order to confirm its deletion.

### Bug Fixes

- Fixed an issue where you could not access Airflow's REST API with a Deployment API key
- Fixed an issue where calling the `imageDeploy` API mutation with a Deployment API key would result in an error

## October 15, 2021

### Minor Improvements

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

### Minor Improvements

- In the Astronomer UI, the **Open Airflow** button is now disabled until the Airflow UI of the Deployment is available.
- Workspace Admins can now edit user permissions and remove users within a given Workspace.

## September 28, 2021

:::danger

This release introduces a breaking change to code deploys via the Astronomer CLI. Starting on September 28, you must upgrade to v1.0.0 of the CLI to deploy code to Astronomer. [CI/CD processes](ci-cd) enabled by Deployment API keys will continue to work and will not be affected. For more information, read the [CLI release notes](cli-release-notes).

:::

### Minor Improvements

- In the Astronomer UI, a new element on the Deployment information screen shows the health status of a Deployment. Currently, a Deployment is considered unhealthy if the Airflow Webserver is not running and the Airflow UI is not available:

    <div class="text--center">
      <img src="/img/docs/deployment-health.png" alt="Deployment Health text in the UI" />
    </div>

- The documentation home for Astronomer Cloud has been moved to `docs.astronomer.io`, and you no longer need a password to access the page.

### Bug Fixes

- The Astronomer UI now correctly renders a Deployment's running version of Astronomer Runtime.

## September 17, 2021

### Support for Deployment API Keys

Astronomer Cloud now officially supports Deployment API keys, which you can use to automate code pushes to Astronomer and integrate your environment with a CI/CD tool such as GitHub Actions. For more information on creating and managing Deployment API keys, see [Deployment API keys](api-keys). For more information on using Deployment API keys to programmatically deploy code, see [CI/CD](ci-cd). Support making requests to Airflow's REST API using API keys is coming soon.

## September 3, 2021

### Bug Fixes

- Added new protections to prevent S3 remote logging connections from breaking
- Fixed an issue where environment variables with extra spaces could break a Deployment
- Fixed an issue where Deployments would occasionally persist after being deleted via the UI
- In the UI, the **Organization** tab in **Settings** is now hidden from non-admin users
- In the UI, the table view of Deployments no longer shows patch information in a Deployment's **Version** value

## August 27, 2021

### Minor Improvements

- You can now remain authenticated to Astronomer across multiple active browser tabs. For example, if your session expires and you re-authenticate to Astronomer Cloud on one tab, all other tabs running Astronomer Cloud will be automatically updated without refreshing.
- If you try to access a given page on Astronomer Cloud while unauthenticated and reach the login screen, logging in now brings you to the original page you requested.

### Bug Fixes

- Fixed an issue where an incorrect total number of team members would appear in the **People** tab

## August 20, 2021

### Support for the Airflow REST API

You can now programmatically trigger DAGs and update your Airflow Deployments on Astronomer by making requests to Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html). Currently this feature works only with temporary tokens, which are available at `cloud.astronomer.io/token`. Support for Deployment API keys is coming soon. For more information on using this feature, read [Airflow API](airflow-api).

### Minor Improvements

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

### Minor Improvements

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
