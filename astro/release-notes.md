---
sidebar_label: 'Astro'
title: 'Astro release notes'
id: release-notes
description: A real-time reference of the latest features and bug fixes in Astro.
---

## Overview
<!--- Version-specific -->

Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes officially released to Astro.

If you have any questions or a bug to report, don't hesitate to reach out to [Astronomer support](https://support.astronomer.io).

**Latest Astro Runtime Version**: 5.0.4 ([Release notes](runtime-release-notes.md))

**Latest CLI Version**: 1.2.0 ([Release notes](cli/release-notes.md))

## June 30, 2022

### New Google Cloud Platform regions

You can now [create an Astro cluster on GCP](create-cluster.md) in the following regions:

- `asia-northeast1` (Tokyo)
- `asia-northeast2` (Osaka)
- `asia-northeast3` (Seoul)
- `asia-south1` (Mumbai)
- `europe-central2` (Warsaw)
- `europe-west6` (Zurich)
- `northamerica-northeast1` (Montreal)
- `us-west3` (Salt Lake City)

For a list of all Google Cloud Platform (GCP) regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp.md#gcp-region).

### Additional improvements

- You can now search for Organization members by name, email address, and role in the **People** tab of the Organization view in the the Cloud UI. You can also search for members in the **Access** tab of the Workspace view.

### Bug fixes

- Fixed an issue where you could not use the KubernetesPodOperator to execute tasks in a Kubernetes cluster outside of your Astro cluster. See [KubernetesPodOperator](https://docs.astronomer.io/astro/kubernetespodoperator).

## June 23, 2022

### New GCP regions available

You can now [create an Astro cluster on GCP](create-cluster.md) in the following regions:

- `asia-southeast1` (Singapore)
- `australia-southeast1` (Sydney)
- `europe-west1` (Belgium)
- `europe-west2` (England)
- `europe-west3` (Frankfurt)
- `southamerica-east1` (São Paulo)
- `us-west2` (Los Angeles)
- `us-west4` (Nevada)

For a list of all GCP regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp.md#gcp-region).

## June 16, 2022

### Submit Support Requests in the Cloud UI

Support requests can now be created and submitted in the Cloud UI. You no longer need to open an account on the Astronomer support portal to reach the Astronomer team. To streamline the request process, the **Submit Support Request** form auto-populates your currently selected Workspace and Deployment in the Cloud UI.

![Location of the "Submit Support Request" button in the Cloud UI](/img/release-notes/support-form.png)

### Parallelism Now Autoscales with a Deployment's Worker Count

To better scale concurrent task runs, Astro now dynamically calculates [`parallelism`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is an Airflow configuration that determines the maximum number of tasks that can run concurrently within a single Deployment.

A Deployment's `parallelism` is now equal to the current number of workers multiplied by the [`worker_concurrency`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) value. This change ensures that your task runs won't be limited by a static parallelism limit as workers autoscale in your Deployment. See [Worker Autoscaling Logic](configure-deployment-resources.md#worker-autoscaling-logic) for more information.

Note that you can still use a static `parallelism` value by setting `AIRFLOW__CORE__PARALLELISM` as an [environment variable](environment-variables.md).

### Bug Fixes

- Fixed a rare issue where some user emails would be associated with the wrong username.
- Fixed an issue where you could not properly sort entries in the **People** tab by name.

## June 9, 2022

### Update Deployment configurations with the Astro CLI

You can now programmatically update the configurations for your Astro Deployments using Deployment API keys and the Astro CLI. Updating a Deployment with an API key doesn't require manual user authentication, meaning that you can now add Deployment configuration steps to automated processes such as CI/CD pipelines.

Specifically, you can now run the following commands with Deployment API keys:

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment update`](cli/astro-deployment-update.md)
- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)

### Bug fixes

- Fixed an issue where a Deployment's logs wouldn't load in the Cloud UI if it was the only Deployment in the Workspace

## June 2, 2022

### Support for the `us-east4` GCP region

You can now [create an Astro cluster on GCP](create-cluster.md) in the `us-east4` region, which is located in northern Virginia, USA.

For a list of all GCP regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp.md#gcp-region).

## May 26, 2022

### New Datasets page in the Cloud UI

You can now use the new **Datasets** page in the **Lineage** tab to view a table of datasets that your DAGs have read or written to. This information can help you quickly identify dataset dependencies and data pipeline access requirements.

![Datasets page](/img/release-notes/datasets-page.png)

Click the name of a dataset to show its lineage graph. For more information, see [Data lineage on Astro](data-lineage.md#view-recently-accessed-datasets).

### Bug fixes

- Fixed an issue where the **Astro Runtime** field of the Cloud UI listed the running version as **Unknown**  for Deployments using an unsupported version of Astro Runtime

## May 5, 2022

### Data lineage Is now available on Astro

We are excited to introduce data lineage to Astro. You now have access to a new **Lineage** view in the Cloud UI that visualizes data movement across datasets in your Organization based on integrations with Airflow, Apache Spark, dbt, Great Expectations, and more.

Built around the [OpenLineage](https://openlineage.io/) open source standard, the data lineage graphs and metadata in the Cloud UI can help you better understand your ecosystem and diagnose issues that may otherwise be difficult to identify.

![Lineage graph example](/img/release-notes/lineage-example.png)

For example, if an Airflow task failed because the schema of a database changed, you might go to the Lineage page on Astro to determine which job caused that change and which downstream tasks failed because of it.

To learn more about data lineage and how you can configure it on Astro, see:

- [Data lineage Concepts](data-lineage-concepts.md)
- [Enable data lineage for External Services](set-up-data-lineage.md)
- [Data lineage on Astro](data-lineage.md)
- [Data lineage Support and Compatibility](data-lineage-support-and-compatibility.md)

:::info

This functionality is still early access and under active development. If you have any questions or feedback about this feature, reach out to [Astronomer support](https://support.astronomer.io).

:::

### Support for Astro on Google Cloud Platform (GCP)

Astro now officially supports Astro clusters on Google Cloud Platform (GCP). This includes support for an initial set of GCP regions as well as [Workload Identity](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) for secure connection to other GCP data services in your ecosystem.

For more information about the installation process and supported configurations, see [Install Astro on GCP](install-gcp.md) and [Resource Reference GCP](resource-reference-gcp.md).

### Support for Organization-Level user invites

You can now [invite users to an Astro Organization](add-user.md#add-a-user-to-an-organization) without having to first invite them to a specific Workspace. Users invited to an Organization will receive an activation email which brings them directly to the Organization view of the Cloud UI.

### Additional improvements

- Improved the templated emails sent out for user invites with clear instructions for how to get started on Astro
- Improved error messaging behavior on the **DAGs** and **Usage** pages of the Cloud UI
- New user accounts must now be verified via email before they can access Astro

## April 28, 2022

### New AWS node instance types available

To widen our support for various use cases and levels of scale, we've expanded the types of AWS node instances that are supported on Astro. You can now create clusters with:

- [General Purpose M6i instances](https://aws.amazon.com/ec2/instance-types/m6i/)
- [Compute Optimized C6i instances](https://aws.amazon.com/ec2/instance-types/c6i/)
- [Memory Optimized R6i instances](https://aws.amazon.com/ec2/instance-types/r6i/)

For a full list of node instance types that are supported on Astro, see [AWS Resource Reference](resource-reference-aws.md#node-instance-type). To modify an existing Astro cluster to use any of these instance types, see [Modify a Cluster](modify-cluster.md).

### Additional improvements

- Improve the error message that renders in the Cloud UI if you try to create a worker that is too large for the Deployment's node instance type to support. This error message now specifies a clear call to action

## April 21, 2022

### Feedback in Cloud UI on worker size limits

The Cloud UI now renders an error if you try to modify the **Worker Resources**  to a combination of CPU and memory that is not supported by the node instance type of the cluster that the Deployment is hosted on. This validation ensures that the worker size you request is supported by the infrastructure available in your Astro cluster, and minimizes silent task failures that might have occurred due to invalid resource requests.

If your Astro cluster is configured with the `m5d.8xlarge` node type, for example, the Cloud UI will show an error if you try to set **Worker Resources** to 350 AU. This is because the maximum worker size an `m5d.8xlarge` node can support is 307 AU.

![Worker size error](/img/release-notes/worker-size-error.png)

For a reference of all node instance types Astro supports and their corresponding worker size limits, see [AWS Resource Reference](resource-reference-aws.md#node-instance-type).

## April 14, 2022

### Additional improvements

- The data plane now connects to various AWS services via [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-services-overview.html). This ensures that traffic to AWS services is kept private and does not traverse the NAT and Internet gateways, reducing the risk of exposing your resources to the internet.

### Bug fixes

- Fixed an issue where you could not add a new user to a Workspace if the user had an email address that contained uppercase characters

## March 31, 2022

### New analytics page in Cloud UI to monitor Deployments

The Cloud UI now includes a dedicated **Analytics** page that contains various Deployment-level metrics. These metrics are collected in real time and can provide insight into how your data pipelines are performing over time:

![Analytics menu location](/img/docs/access-analytics.png)

For more information about accessing the **Analytics** page and the available metrics, see [Deployment Analytics](deployment-metrics.md#deployment-analytics).

### Lineage backend upgrade scheduled for all Organizations

As part of [Astronomer's acquisition of Datakin](https://www.astronomer.io/blog/astronomer-acquires-datakin-the-data-lineage-tool/), data lineage features are coming soon to Astro. The first step in enabling these features is to implement lineage backends for existing Astro customers.

Starting on March 31st and continuing over the next couple of weeks, all Astro Deployments on Runtime 4.2.0+ will be upgraded to emit lineage events. As a result of this change, you might start seeing lineage-related scheduler logs such as the following:

```text
[2022-03-30, 12:17:39 UTC] {great_expectations_extractor.py:17} INFO - Did not find great_expectations_provider library or failed to import it
[2022-03-24, 23:40:01 UTC] {client.py:74} INFO - Constructing openlineage client to send events to https://api.astro-astronomer.datakin.com
```

A few additional notes about this upgrade:

- You can ignore any lineage logs that indicate an error or failed process, such as the first line in the example logs above. These logs will more accurately reflect the state of your lineage functionality once lineage features are launched on Astro.
- Deployments on Runtime 4.2.0+ will be updated to emit data lineage events only after you [push code](deploy-code.md). Until you do so, this change will not be applied.
- Because Astronomer is upgrading each customer individually over time, the exact date that you will start seeing these logs will vary.
- When you push code to a Deployment on Runtime 4.2.0+ and trigger this update, all other Deployments on Runtime 4.2.0+ in the same Workspace will also restart in order to receive the lineage backend update. If you plan to push code to any Deployment affected by this change, then we recommend doing so at a time where you can tolerate some Airflow components restarting. For more information about expected behavior, see [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

For more information about what to expect when lineage tools go live, read Astronomer's [OpenLineage and Airflow guide](https://www.astronomer.io/guides/airflow-openlineage).

### New AWS regions available

You can now [create new Clusters](create-cluster.md) in:

- `af-south-1` (Cape Town)
- `ap-east-1` (Hong Kong)
- `ap-northeast-3` (Osaka)  
- `me-south-1` (Bahrain)

For a full list of AWS regions supported on Astro, see [AWS Resource Reference](resource-reference-aws.md#aws-region).

### Additional improvements

- The Cloud UI now includes a button that links to Astronomer [support](https://support.astronomer.io/) and [status](https://status.astronomer.io/) pages:

    ![Runtime Tag banner](/img/release-notes/support-button.png)

## March 25, 2022

### Maximum node count is now configurable per Cluster

As of this release, **Maximum Node Count** is now a configurable setting for new and existing clusters. On Astro, maximum node count represents the total number of EC2 nodes that your cluster can support at any given time. For an Astro cluster on AWS, EC2 nodes are the primary unit of infrastructure required to run a Deployment and its components, including workers and the Airflow scheduler. New clusters have a maximum node count of 20 by default, but the setting can be modified to any value from 2 to 100 at any time.

Previously, maximum node count was a fixed, global setting that applied to all customers on Astro and could not be configured per cluster. Now, your organization can modify this setting as your workloads evolve and more Deployments are created. Once the limit is reached, your cluster will not be able to auto-scale and worker pods may fail to schedule.

To update this setting for an existing cluster, reach out to [Astronomer support](https://support.astronomer.io) and provide the name of your cluster and the desired maximum node count.

### Additional improvements

- In **Resource Settings**, the maximum allowed value for **Worker Resources** has been increased to 400 AU.

## March 17, 2022

### Export task usage as a CSV file

In the Cloud UI, you can now export your task usage data from the **Usage** tab as a CSV file to perform more complex data analysis related to your Airflow usage and costs. For example, you can use the file as the basis for a pivot table that shows total task usage by Workspace.

To export your task usage data as a CSV file, click the **Export** button in the **Usage** tab:

![Export as CSV button in Usage tab](/img/release-notes/csv-file.png)

### Bug fixes

- Fixed an issue where saving new environment variables in the Cloud UI would occasionally fail

## March 10, 2022

### Running Docker image tag in Airflow UI

The Docker image that is running on the Airflow webserver of your Deployment is now shown as a tag in the footer of the Airflow UI. Depending on how your team deploys to Astro, this tag is either a unique identifier generated by a CI tool or a timestamp generated by the Astro CLI on `astro deploy`. Both represent a unique version of your Astro project.

![Runtime Tag banner](/img/docs/image-tag-airflow-ui-astro.png)

When you push code to a Deployment on Astro via the Astro CLI or CI/CD, reference this tag in the Airflow UI to verify that your changes were successfully applied.

This feature requires Astro Runtime [4.0.10+](runtime-release-notes.md#4010). To upgrade a Deployment to the latest Runtime version, see [Upgrade Runtime](upgrade-runtime.md).

:::info

While it is a good proxy, the tag shown in the Airflow UI does not forcibly represent the Docker image that is running on your Deployment's scheduler, triggerer, or workers.

This value is also distinct from the **Docker Image** that is shown in the Deployment view of the Cloud UI, which displays the image tag as specified in the Cloud API request that is triggered on `astro deploy`. The image tag in the Airflow UI can be interpreted to be a more accurate proxy to what is running on all components of your Deployment.

If you ever have trouble verifying a code push to a Deployment on Astro, reach out to [Astronomer support](https://support.astronomer.io).

:::

## March 3, 2022

### Additional improvements

- The threshold in order for bars in the **Worker CPU** and **Worker Memory** charts to appear red has been reduced from 95% to 90%. This is to make sure that you get an earlier warning if your workers are close to hitting their resource limits.

### Bug fixes

- Fixed an issue where malformed URLs prevented users from accessing the Airflow UI of some Deployments on Astro
- Fixed an issue where Astro Runtime 4.0.11 wasn't a selectable version in the **Astro Runtime** menu of the Deployment creation view in the Cloud UI

## February 24, 2022

### Bug fixes

- Removed the **Teams** tab from the Cloud UI. This view was not yet functional but coming back soon
- Fixed an issue where the number of users per Workspace displayed in the Organization view of the Cloud UI was incorrect
- Fixed an issue where if a secret environment value was updated in the Cloud UI and no other values were modified, the change was not applied to the Deployment

## February 17, 2022

### Introducing Astro and a new look

This week's release introduces a reimagined Astronomer brand that embraces **Astro** as a rename of Astronomer Cloud. The rebrand includes a new Astronomer logo, color palette, and font.

![New branding](/img/release-notes/new-branding.png)

The new Astronomer brand is now reflected both in the [Cloud UI](https://cloud.astronomer.io) as well as in the main [Astronomer website](https://astronomer.io) and [documentation](https://docs.astronomer.io).

In addition to visual changes, we've renamed the following high-level Astro components:

- **Astronomer Cloud CLI** is now **Astro CLI**
- **Astronomer UI** is now **Cloud UI**
- **Astro Runtime** is now **Astro Runtime**

We hope you find this exciting. We're thrilled.

### New Organization roles for users

The following Organization-level roles are now supported on Astro:

- **Organization Member**: This role can view Organization details and membership. This includes everything in the **People**, **Clusters**, and **Settings** page of the Cloud UI. Organization members can create new Workspaces and invite new users to an Organization.
- **Organization Billing Admin:** This role has all of the Organization Member's permissions, plus the ability to manage Organization-level settings and billing. Organization Billing Admins can access the **Usage** tab of the Cloud UI and view all Workspaces across the Organization.
- **Organization Owner:** This role has all of the Organization Billing Admin's permissions, plus the ability to manage and modify anything within the entire Organization. This includes Deployments, Workspaces, Clusters, and users. Organization Owners have Workspace Admin permissions to all Workspaces within the Organization.

Organization roles can be updated by an Organization Owner in the **People** tab of the Cloud UI. For more information about these roles, see [User permissions](user-permissions.md).

### Create new Workspaces from the Cloud UI

All users can now create a new Workspace directly from the **Overview** tab of the Cloud UI:

![Create Workspace button](/img/release-notes/add-workspace.png)

When you create a new Workspace, you will automatically become a Workspace Admin within it and can create Deployments. For more information about managing Workspaces, see [Manage Workspaces](manage-workspaces.md).

### Bug fixes

- Fixed an issue where authentication tokens to Astro weren't properly applied when accessing the Airflow UI for a Deployment. This would result in an authenticated user seeing `Error: Cannot find this astro cloud user` in the Airflow UI.
- Fixed an issue where long environment variable values would spill out of the **Value** column and onto the **Updated** column in the **Environment Variables** view of a Deployment in the Cloud UI.

## February 11, 2022

### Monitor DAG runs across all Deployments in a Workspace

You can view key metrics about recent DAG runs through the new **DAGs** page in the Cloud UI. Use this page to view DAG runs at a glance, including successes and failures, across all Deployments in a given Workspace. You can also drill down to a specific DAG and see metrics about its recent runs.

![DAGs page](/img/docs/dags-page.png)

For more information about the **DAGs** page, see [Deployment metrics](deployment-metrics.md#dag-runs).

### Additional improvements

- All resource settings in the Deployment view of the Astronomer UI now show exact CPU and Memory usage to the right of every slider, previously shown only in Astronomer Units (AUs). This makes it easy to know exactly how many resources you allocate to each component.
- A banner now appears in the Astronomer UI if a Deployment is running a version of Astro Runtime that is no longer maintained. To make the most of features and bug fixes, we encourage users to upgrade to recent versions as much as possible.
- Added more ways to sort pages that utilize card views, such as the **Deployments** page
- Added user account avatars next to usernames in several places across the Cloud UI

### Bug fixes

- Removed the **Environment** field from the Deployment view of the Astronomer UI. This field is not currently functional and will be re-added as soon as it is.

## February 3, 2022

### Support for third-party identity providers

You can now integrate both Azure AD and Okta as identity providers (IdPs) for federated authentication on Astro. By setting up a third-party identity provider, a user in your organization will be automatically logged in to Astro if they're already logged in via your IdP. By adding new Astro users through your IdP's own user management system, Workspace admins can automatically add new users to their Workspace without those users needing to individually sign up for Astro.

For more information about this feature read [Set up an identity provider](configure-idp.md).

### Support for the Astro CLI

The Astro CLI (`astro`) is now generally available as the official command-line tool for Astro. It is a direct replacement of the previously released `astro` executable and comes with various significant improvements. We encourage all customers to upgrade.

For more information on the Astro CLI, see [CLI Release Notes](cli/release-notes.md). For install instructions, read [Install the CLI](cli/get-started.md).

### Multiple authentication methods for a single user account

Astro now supports multiple authentication methods for a single user account. This means that as long as you're using a consistent email address, you now have the flexibility to authenticate with GitHub, Google, username/password, and/or [an external identity provider (idP)](configure-idp.md) at any time. Previously, a single user account could only be associated with one authentication method, which could not be changed after the account was created.

This also means that all Organizations now have GitHub, Google, and username/password authentication methods enabled by default for all users.

### Additional improvements

- Changed the default RDS instance type for new clusters from `db.r5.xlarge` to `db.r5.large`, which represents a monthly cost reduction of ~50% for newly provisioned clusters. Customers with existing clusters will need to request a downscale via [Astronomer support](https://support.astronomer.io)

## January 13, 2022

### Identity-based login flow

Astro now utilizes an identity-based login flow for all users. When you first log in via the Cloud UI, you now only need to enter the email address for your account. Astro assumes your Organization and brings you directly to your Astro Organization's login screen.

This change serves as a foundation for future SSO and authentication features. In upcoming releases, users will be able to authenticate via custom identity providers like Okta and Azure Active Directory.

### Additional improvements

- Significant improvements to the load times of various Cloud UI pages and elements.
- In the Cloud UI, the tooltips in the **Resource Settings** section of a Deployment's page now show the definition of 1 AU. This should make it easier to translate AU to CPU and Memory.
- Scheduler logs in the Cloud UI no longer show `DEBUG`-level logs.
- To ensure that all workers have enough resources to run basic workloads, you can no longer allocate less than 10 AU to **Worker Resources**.

## January 6, 2022

### Improvements to "Scheduler Logs" in the Cloud UI

The **Scheduler Logs** tab in the Cloud UI has been updated to make logs easier to read, separate, and parse. Specifically:

- You can now filter logs by type (`DEBUG`, `INFO`, `WARN`, and `ERROR`).
- The page now shows logs for the past 24 hours instead of the past 30 minutes.
- The page now shows a maximum of 500 logs instead of a lower maximum.
- When looking at a Deployment's logs, you can return to the Deployment's information using the **Deployment Details** button.

![Logs page in the UI](/img/release-notes/log-improvements.png)

### Removal of worker termination grace period

The **Worker Termination Grace Period** setting is no longer available in the Cloud UI or API. Previously, users could set this to anywhere between 1 minute and 24 hours per Deployment. This was to prevent running tasks from being interrupted by a code push. Today, however, existing Celery workers don't have to terminate in order for new workers to spin up and start executing tasks. Instead, existing workers will continue to execute running tasks while a new set of workers gets spun up concurrently to start executing most recent code.

To simplify Deployment configuration and reflect current functionality:

- The worker Termination Grace Period was removed from the Cloud UI
- This value was permanently set to 24 hours for all Deployments on Astro

This does not change or affect execution behavior for new or existing Deployments. For more information, read [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Additional improvements

- Removed _Kubernetes Version_ column from the **Clusters** table. This value was previously inaccurate and is not needed. The Kubernetes version of any particular Astro cluster is set and modified exclusively by Astro as part of our managed service.

## December 16, 2021

### View scheduler error logs from the Cloud UI

The new **Logs** tab in the Cloud UI shows scheduler error and warning logs for all Deployments in your Workspace. When you select a Deployment in this menu, all error logs generated over the last 30 minutes appear in the UI.

![Logs page in the UI](/img/release-notes/logs-page.png)

To access logs directly for a given Deployment, click the new **Logs** button on the Deployment's page or in the **Deployments** table.

![Logging direct access button](/img/release-notes/logs-button.png)

For more information on how to view logs, read [View logs](view-logs.md).

### Bug fixes

Fixed various bugs in the Cloud UI to better handle nulls and unknowns in Deployment metrics

## December 9, 2021

### Additional improvements

- In the Cloud UI, the **Open Airflow** button now shows more specific status messages when a Deployment's Airflow UI is inaccessible.

### Bug fixes

- Fixed Deployment table scrolling and alignment issues in the UI

## December 6, 2021

### New "Usage" tab in the Cloud UI

Total task volume for your Organization is now available in a new **Usage** tab in the Cloud UI. Astro is priced based on successful task runs, so this view can help you monitor both Astro cost as well as Airflow usage in aggregate and between Deployments.

![Usage tab in the Cloud UI](/img/docs/usage.png)

For more information about the **Usage** tab, read [Deployment metrics](deployment-metrics.md#usage).

### New AWS regions available

You can now create new clusters in:

- `us-west-1`
- `ap-northeast-1 `
- `ap-southeast-1`
- `ap-northeast-2`
- `ap-southeast-2`
- `ap-south-1`
- `us-west-1`
- `us-west-2`

For a full list of AWS regions supported on Astro, see [AWS Resource Reference](https://docs.astronomer.io/resource-reference-aws.md#aws-region).

### Additional improvements

- You can now see your Deployment's **Namespace** in the **Deployments** menu and on the Deployment information screen in the Cloud UI. Namespace is a required argument to run tasks with the KubernetesPodOperator. It is also required to submit an issue to [Astronomer support](https://support.astronomer.io).

    ![Deployment namespace available on a Deployment's information page](/img/docs/namespace.png)

- The Cloud UI now shows a warning if you attempt to exit Environment Variable configuration without saving your changes.
- A Deployment's health status is now based on the health of both the Airflow webserver and scheduler. Previously, a Deployment's health status was only based on the health of the webserver. Now, the Cloud UI will show that your Deployment is "Healthy" only if both components are running as expected.

### Bug fixes

- The Cloud UI now has error handling for attempts to access a Deployment that does not exist.
- If you attempt to modify an existing secret environment variable, the **Value** field is now blank instead of showing hidden characters.

### Data plane improvements

- Amazon EBS volumes have been upgraded from gp2 to [gp3](https://aws.amazon.com/about-aws/whats-new/2020/12/introducing-new-amazon-ebs-general-purpose-volumes-gp3/) for improved scale and performance.
- EBS volumes and S3 buckets are now encrypted by default.
- The ability to enable public access to any Amazon S3 bucket on an Astro data plane is now blocked per a new AWS account policy. Previously, public access was disabled by default but could be overridden by a user creating a new S3 bucket with public access enabled. This AWS account policy could be overridden by AWS account owners, but Astronomer strongly recommends against doing so.

## November 19, 2021

### Secret environment variables

You can now set secret environment variables via the Cloud UI. The values of secret environment variables are hidden from all users in your Workspace, making them ideal for storing sensitive information related to your Astro projects.

![Secrets checkbox available in the Cloud UI](/img/release-notes/secrets-feature.png)

For more information, read [Set environment variables via the Cloud UI](environment-variables.md#set-environment-variables-via-the-astro-ui).

### Additional improvements

- You can now create new clusters in AWS `sa-east-1`.
- Extra whitespace at the end of any environment variable that is set via the Cloud UI is now automatically removed to ensure the variable is passed correctly.

## November 11, 2021

### Deployment metrics dashboard

In the Cloud UI, your Deployment pages now show high-level metrics for Deployment health and performance over the past 24 hours.

<div class="text--center">
  <img src="/img/docs/deployment-metrics.png" alt="New metrics in the Cloud UI" />
</div>

For more information on this feature, read [Deployment metrics](deployment-metrics.md).

### Bug fixes

- Resolved a security vulnerability by setting `AIRFLOW__WEBSERVER__COOKIE_SECURE=True` as a global environment variable

## November 5, 2021

### Bug fixes

- Fixed an issue where a new user could not exit the Cloud UI "Welcome" screen if they hadn't yet been invited to a Workspace

## October 29, 2021

### Cloud UI redesign

The Cloud UI has been redesigned so that you can more intuitively manage Organizations, Workspaces, and your user profile.

To start, the homepage is now a global view. From here, you can now see all Workspaces that you have access to, as well as information and settings related to your **Organization**: a collection of specific users, teams, and Workspaces. Many features related to Organizations are coming soon, but the UI now better represents how Organizations are structured and what you can do with them in the future:

<div class="text--center">
  <img src="/img/docs/ui-release-note1.png" alt="New global menu in the UI" />
</div>

You can now also select specific Workspaces to work in. When you click in to a Workspace, you'll notice the lefthand menu bar is now entirely dedicated to Workspace actions:

- The Rocket icon brings you to the **Deployments** menu.
- The People icon brings you to the **Workspace Access** menu.
- The Gear icon brings you to the **Workspace Settings** menu.

To return to the global menu, you can either click the Astro "A" or click the Workspace name to produce a dropdown menu with your Organization.

<div class="text--center">
  <img src="/img/docs/ui-release-note2.png" alt="New Workspace menu in the UI" />
</div>

All user configurations can be found by clicking your user profile picture in the upper righthand corner of the UI. From the dropdown menu that appears, you can both configure user settings and access other Astronomer resources such as documentation and the Astronomer Registry.

<div class="text--center">
  <img src="/img/docs/ui-release-note3.png" alt="New profile menu in the UI" />
</div>

### Additional improvements

- You can now create new clusters in `us-east-2` and `ca-central-1`.
- In the Deployment detail page, **Astro Runtime** now shows the version of Apache Airflow that the Deployment's Astro Runtime version is based on.
- You can now create or modify an existing Astro cluster to run any size of the `t2`,`t3`, `m5`, or `m5d` [AWS EC2 instances](resource-reference-aws.md).

### Bug fixes

- Fixed an issue where a new Deployment's health status did not update unless you refreshed the Cloud UI

## October 28, 2021

### Bug fixes

- Fixed an issue where you couldn't push code to Astro with a Deployment API key via a CI/CD process
- Fixed an issue where you couldn't update or delete an API key after creating it

## October 25, 2021

### Additional improvements

- When deleting a Deployment via the UI, you now have to type the name of the Deployment in order to confirm its deletion.

### Bug fixes

- Fixed an issue where you could not access Airflow's REST API with a Deployment API key
- Fixed an issue where calling the `imageDeploy` API mutation with a Deployment API key would result in an error

## October 15, 2021

### Additional improvements

- When creating a new Deployment, you can now select only the latest patch version for each major version of Astro Runtime.
- When creating a new Deployment in the Cloud UI, the cluster is pre-selected if there is only one cluster available.
- The name of your Astro Deployment now appears on the main DAGs view of the Airflow UI.
- You can now see the health status for each Deployment in your Workspace on the table view of the **Deployments** page in the Cloud UI:

   <div class="text--center">
     <img src="/img/docs/health-status-table.png" alt="Deployment Health statuses visible in the Deployments table view" />
   </div>

- In the Cloud UI, you can now access the Airflow UI for Deployments via the **Deployments** page's card view:

    <div class="text--center">
      <img src="/img/docs/open-airflow-card.png" alt="Open Airflow button in the Deployments page card view" />
    </div>

- The Cloud UI now saves your color mode preference.

## October 1, 2021

### Additional improvements

- In the Cloud UI, the **Open Airflow** button is now disabled until the Airflow UI of the Deployment is available.
- Workspace Admins can now edit user permissions and remove users within a given Workspace.

## September 28, 2021

:::danger

This release introduces a breaking change to code deploys via the Astro CLI. Starting on September 28, you must upgrade to v1.0.0+ of the CLI to deploy code to Astro. [CI/CD processes](ci-cd.md) enabled by Deployment API keys will continue to work and will not be affected. For more information, read the [CLI release notes](cli/release-notes.md).

:::

### Additional improvements

- In the Cloud UI, a new element on the Deployment information screen shows the health status of a Deployment. Currently, a Deployment is considered unhealthy if the Airflow webserver is not running and the Airflow UI is not available:

    <div class="text--center">
      <img src="/img/docs/deployment-health.png" alt="Deployment Health text in the UI" />
    </div>

- The documentation home for Astro has been moved to `docs.astronomer.io`, and you no longer need a password to access the page.

### Bug fixes

- The Cloud UI now correctly renders a Deployment's running version of Astro Runtime.

## September 17, 2021

### Support for Deployment API keys

Astro now officially supports Deployment API keys, which you can use to automate code pushes to Astro and integrate your environment with a CI/CD tool such as GitHub Actions. For more information on creating and managing Deployment API keys, see [Deployment API keys](api-keys.md). For more information on using Deployment API keys to programmatically deploy code, see [CI/CD](ci-cd.md). Support making requests to Airflow's REST API using API keys is coming soon.

## September 3, 2021

### Bug fixes

- Added new protections to prevent S3 remote logging connections from breaking
- Fixed an issue where environment variables with extra spaces could break a Deployment
- Fixed an issue where Deployments would occasionally persist after being deleted via the UI
- In the UI, the **Organization** tab in **Settings** is now hidden from non-admin users
- In the UI, the table view of Deployments no longer shows patch information in a Deployment's **Version** value

## August 27, 2021

### Additional improvements

- You can now remain authenticated to Astro across multiple active browser tabs. For example, if your session expires and you re-authenticate to Astro on one tab, all other tabs running Astro will be automatically updated without refreshing.
- If you try to access a given page on Astro while unauthenticated and reach the login screen, logging in now brings you to the original page you requested.

### Bug fixes

- Fixed an issue where an incorrect total number of team members would appear in the **People** tab

## August 20, 2021

### Support for the Airflow REST API

You can now programmatically trigger DAGs and update your Deployments on Astro by making requests to Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html). Currently this feature works only with temporary tokens, which are available at `cloud.astronomer.io/token`. Support for Deployment API keys is coming soon. For more information on using this feature, read [Airflow API](airflow-api.md).

### Additional improvements

- Set `AIRFLOW_HOME = 'usr/local/airflow'` as a permanent global environment variable
- In the Cloud UI, long environment variable keys and values now wrap to fit the screen
- Added links for the Astronomer Registry and certification courses to the left-hand navbar
- Moved the **Teams** and **People** tabs into the **Settings** page of the UI
- Added **Cluster** information to the metadata section of a Deployment's information page in the UI
- Renamed various UI elements to better represent their functionality
- Increased the maximum **Worker Termination Grace Period** from 600 minutes (10 hours) to 1440 minutes (24 hours)

### Bug fixes

- The left-hand navbar in the UI is no longer cut off when minimized on smaller screens
- Fixed an issue where you could not delete a Workspace via the UI
- Fixed an issue where expired tokens would occasionally appear on `cloud.astronomer.io/token`
- Fixed an issue where the UI would initially load an inaccurate number of team members on the **Access** page
- Fixed alphabetical sorting by name in the **People** tab in the UI
- Removed placeholder columns from various tables in the UI

## August 6, 2021

### Additional improvements

- Informational tooltips are now available on the **New Deployment** page.

### Bug fixes

- Fixed an issue where adding a user to a Workspace and then deleting the user from Astro made it impossible to create new Deployments in that Workspace
- Improved error handling in the Airflow UI in cases where a user does not exist or does not have permission to view a Deployment

## July 30, 2021

### Improvements

- Increased the limit of **Worker Resources** from 30 AU to 175 AU (17.5 CPU, 65.625 GB RAM). If your tasks require this many resources, reach out to us to make sure that your cluster is sized appropriately
- Collapsed the **People** and **Teams** tabs on the left-hand navigation bar into a single **Access** tab
- Added a **Cluster** field to the Deployments tab in the Cloud UI. Now, you can reference which cluster each of your Deployments is in
- Replaced our white "A" favicon to one that supports color mode
- Informational tooltips are now available in **Deployment Configuration**

### Bug fixes

- Fixed an issue where a deleted user could not sign up to Astro again
- Removed Deployment-level user roles from the Cloud UI. Support for them coming soon
- Fixed an issue where a newly created Deployment wouldn't show up on the list of Deployments in the Workspace
