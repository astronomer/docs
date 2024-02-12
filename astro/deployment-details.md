---
sidebar_label: 'Deployment details'
title: 'Deployment details'
id: deployment-details
description: "Edit information about your Deployment, like metadata settings, observability settings, and user access settings."
---

Deployment details define how users can view and interact with your Deployment. They include metadata settings, observability settings, and user access settings.

## Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Basic** section, update the Deployment **Name** or **Description**.

4. Click **Update Deployment**.

## Configure Deployment contact emails

Configure a contact email to get proactive alerts directly from Astronomer support. Astronomer support uses contact emails to notify recipients in case there's an issue with the infrastructure for your Deployment, such as a problem with your scheduler or worker components.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Details** tab. In the **Advanced** menu, click **Edit**.

3. To add an alert email:
    - In the **Contact Emails** section, click **Add Email**.
    - Enter an email address and then click **Add**.

4. To delete an alert email address:
    - In the **Contact Emails** section, click **Delete** next to the email you want to delete.
    - Click **Yes, Continue**.

In addition to alert emails for your Deployments, Astronomer recommends configuring [Astro alerts](alerts.md) and subscribing to the [Astro status page](https://status.astronomer.io). When you subscribe to the status page, you'll receive email notifications about system-wide incidents as they happen.

## Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. This means that by default, any individual user can deploy code either directly from the Astro CLI or from a CI/CD process that is authenticated with an API token. To help your team protect production environments from manual code deploys that circumvent your organization's CI/CD processes and checks, Astronomer supports a Deployment-level setting called **CI/CD Enforcement**. When you enforce CI/CD deploys for a Deployment, the Deployment accepts code deploys only if the deploys are triggered with a Deployment API token, Workspace API token, or Organization API token. Astronomer recommends enabling this setting for all production environments.

:::info

When CI/CD enforcement is enabled for a Deployment, you can't enable [DAG-only deploys](deploy-dags.md) for the Deployment. To use both of these features, Astronomer recommends that you:

1. Turn **CI/CD Enforcement** to **Off**.
2. Enable the DAG-only deploy feature. See [Enable DAG-only deploys](deploy-dags.md#enable-dag-only-deploys).
3. Turn **CI/CD Enforcememt** to **On**.

You have to only complete these steps once. Once the DAG-only deploy feature is enabled, you can turn CI/CD enforcement on or off at any time.

:::

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, find **CI/CD Enforcement** and click the toggle to **On**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

## Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.
