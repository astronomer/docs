---
sidebar_label: 'Authorize Deployments to cloud resources'
title: 'Authorize an Astro Deployment to cloud resources using workload identity'
id: authorize-deployments-to-your-cloud
description: Give Astro Deployments access to your cloud resources using a Kubernetes workload identity
toc_max_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import HostedBadge from '@site/src/components/HostedBadge';

When you create an Airflow connection from a Deployment to access cloud resources, Airflow uses your connection details to access those services. You can add credentials to your Airflow connections to authenticate, but it can be risky to add secrets like passwords to your Airflow environment.

To avoid adding secrets to your Airflow connection, you can directly authorize your Astro Deployment to access AWS or GCP cloud services using workload identity. Astronomer recommends using a workload identity in most cases to improve security and avoid managing credentials across your Deployments. If you have less strict security requirements, you can still use any of the methods described in [Airflow connection guides](https://docs.astronomer.io/learn/connections) to manage your connection authorization.

This guide explains how to authorize your Deployment to a cloud using workload identity. For each Deployment, you will:

- Authorize your Deployment to your cloud services.
- Create an Airflow connection to access your cloud services.

:::tip

You can learn more about what a managed identity is and how to set up passwordless authentication for the Google Cloud Provider with the Astro Academy [Customer Workload Managed Identity](https://academy.astronomer.io/learning-bytes-customer-workload-managed-identity) Learning Byte.

:::

## Prerequisites

The Astro cluster running your Deployment must be connected to your cloud's network. See [Networking overview](networking-overview.md).

## What is workload identity?

A workload identity is a Kubernetes service account that provides an identity to your Deployment. The Deployment can use this identity to authenticate to a cloud's API server, and the cloud can use this identity to authorize the Deployment to access different resources.

## Setup

<Tabs
    defaultValue="aws"
    groupId="setup"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

### Step 1: Authorize the Deployment in your cloud

To grant a Deployment access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles to authorize your Deployment's workload identity. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource, such as Amazon S3 buckets, Redshift instances, and secrets backends.

To authorize your Deployment, create an IAM role that is assumed by the Deployment's workload identity:

1. In the Astro UI, select your Deployment and then click **Details**. Copy the Deployment's **Workload Identity**.
2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.
4. Click **Roles** and in the **Role name** column, select the role you created in Step 2.
5. Click **Trust relationships**.
6. Click **Edit trust policy** and paste the workload identity you copied from Step 1 in the trust policy. Your policy should look like the following:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "<workload-identity-role>"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    ```

7. Click **Update policy**.

Repeat these steps for each Astro Deployment that needs to access your AWS resources.

### Step 2: Create an Airflow connection

Now that your Deployment is authorized, you can connect it to your cloud using an Airflow connection. Either create an **Amazon Web Services** connection in the [Astro UI](create-and-link-connections.md) or the Airflow UI for your Deployment and specify the following fields:

- **Connection Id**: Enter a name for the connection.
- **Extra**:

    ```json
    {
    "role_arn": "<your-role-arn>",
    "region_name": "<your-region>"
    }
    ```

If you don't see **Amazon Web Services** as a connection type in the Airflow UI, ensure you have installed its provider package in your Astro project's `requirements.txt` file. See **Use Provider** in the [Astronomer Registry](https://registry.astronomer.io/providers/Amazon/versions/latest) for the latest package.

</TabItem>

<TabItem value="gcp">

### Attach a service account to your Deployment

<HostedBadge/>

You can attach a custom GCP service account to your Deployment to grant the Deployment all of the service account's permissions.

Using service accounts provides the greatest amount of flexibility for authorizing Deployments to your cloud. For example, you can use existing service accounts on new Deployments, or your can attach a single service account to multiple Deployments that all have the same level of access to your cloud.

1. [Create a service account](https://cloud.google.com/iam/docs/service-accounts-create) in the GCP project that you want your Deployment to access. Grant the service account any permissions that the Deployment will need in your GCP project. Copy the service account ID to use later in this setup.
2. In the Cloud UI, select your Deployment, then click **Details**. In the **Advanced** section, click **Edit**.
3. In the **Workload Identity** menu, select **Customer Managed Identity**
4. Enter your GCP service account ID when prompted, then copy and run the provided gcloud CLI command.
5. Click **Update Deployment**. The service account is now selectable as a workload identity for the Deployment.
6. Complete one of the following options for your Deployment to access your cloud resources:

    - Create a **Google Cloud** connection type in Airflow and configure the following values:
      - **Connection Id**: Enter a name for the connection.
      - **Impersonation Chain**: Enter the ID of the service account that your Deployment should impersonate.

    - To access resources in a secrets backend, run the following command to create an environment variable that grants access to the secrets backend:

    ```zsh
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<your-secret-manager-project-id>", "impersonation_chain": "<your-gcp-service-account>"}
    ```

### Alternative setup: Authorize your Deployment through GCP service account impersonation

If your organization has requirements over how service accounts are managed outside of your cloud, you can manually configure [GCP service account impersonation](https://cloud.google.com/docs/authentication/use-service-account-impersonation) to allow your Deployment's default workload identity to impersonate a service account in your GCP project.

1. [Create a service account](https://cloud.google.com/iam/docs/service-accounts-create) in the GCP project that you want your Deployment to access. Grant the service account any permissions that the Deployment will need in your GCP project. Copy the service account ID to use later in this setup.
2. In the Astro UI, select your Deployment, then click **Details**. Copy the Deployment's **Workload Identity**.
3. In the Google Cloud Console, open the **IAM & Admin > Service Accounts** menu, then open the service account you just created.
4. In the **Actions** column, click **Manage Permissions**, then click **Grant Access**. In the modal that appears, enter your Deployment's workload identity service account in the **Add Principals** field and select the [`Service Account Token Creator`](https://cloud.google.com/iam/docs/understanding-roles#iam.serviceAccountTokenCreator) in the **Assign Roles** field.
5. Complete one of the following options for your Deployment to access your cloud resources:

    - Create a **Google Cloud** connection type in Airflow and configure the following values:
      - **Connection Id**: Enter a name for the connection.
      - **Impersonation Chain**: Enter the ID of the service account that your Deployment should impersonate.

    Note that this implementation requires `apache-airflow-providers-google >= 10.8.0`. See [Add Python, OS-level packages, and Airflow providers](https://docs.astronomer.io/astro/cli/develop-project#add-python-os-level-packages-and-airflow-providers).

   - Specify the impersonation chain in code when you instantiate a Google Cloud operator. See [Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html#direct-impersonation-of-a-service-account). Note that if you configure both a connection type and an operator, the operator-level configuration takes precedence.
    - To access resources in a secrets backend, run the following command to create an environment variable that grants access to the secrets backend:

    ```zsh
    astro deployment variable create --deployment-id <your-deployment-id> AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "<your-secret-manager-project-id>", "impersonation_chain": "<your-gcp-service-account>"}
    ```

### Alternative setup: Grant an IAM role to your Deployment workload identity

Complete this alternative setup if you don't have an existing Google service account that your Deployment workload identity can impersonate.

#### Step 1: Authorize the Deployment in your cloud

To grant a Deployment access to a service that is running in a GCP account not managed by Astronomer, use your Deployment's workload identity. Workload identity is a service account in GCP that's used to manage the level of access for a specific user, object, or group of users to a resource, such as Google BigQuery or a GCS bucket.

To authorize your Deployment, grant the required access to your Deployment's workload identity:

1. In the Astro UI, select your Deployment, then click **Details**. In the **Workload Identity** dropdown menu, select **Default Identity**. Then, copy the workload identity that appears next to the dropdown menu.

2. Grant your Deployment's workload identity an IAM role that has access to your external data service. To do this with the Google Cloud CLI, run:

    ```bash
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:<workload-identity> --role=roles/viewer
    ```

    To grant your workload identity an IAM role using the Google Cloud console, see [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console#grant_an_iam_role).

Repeat these steps for each Deployment that needs to access your GCP resources.

#### Step 2: Create an Airflow connection

Now that your Deployment is authorized, you can connect it to your cloud using an Airflow connection. Either create a **Google Cloud** connection in the [Astro UI](create-and-link-connections.md) or the Airflow UI for your Deployment and specify the following fields:

- **Connection Id**: Enter a name for the connection.
- **Project Id**: Enter the ID of your Google Cloud Project where your services are running.

If you don't see **Google Cloud** as a connection type in the Airflow UI, ensure you have installed its provider package in your Astro project's `requirements.txt` file. See **Use Provider** in the [Astronomer Registry](https://registry.astronomer.io/providers/Google/versions/latest) for the latest package.

</TabItem>

<TabItem value="azure">

<HostedBadge/>

In this setup, you'll authorize an existing user-assigned managed identity to a resource on Azure, then give permissions to your Deployment to assume that managed identity.

#### Prerequisites

- A [Microsoft Entra ID tenant](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-create-new-tenant) with Global Administrator or Application Administrator privileges.
- A user-assigned managed identity on Azure. See [Azure documentation](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?source=recommendations&pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity).
- The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

:::caution

You can only use the same user-assigned managed identity for up to five Deployments. If you need to authorize more than five Deployments to Azure, you need to create more than one user-managed identity. For more information, see [Microsoft Entra documentation](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-considerations#general-federated-identity-credential-considerations).

:::

#### Step 1: Authorize the managed identity in Azure

1. In your Azure portal, open the resource that your managed identity needs access to. Then, select **Access control (IAM)**.
2. Click **Add** > **Add role assignment**.
3. Select the role for your managed identity, then click **Next**.
4. In the **Assign access to** section, select **Managed identity**. Click **+ Select Members** and choose your managed identity. After you add your managed identity, click **Next**.
5. Review and finalize the assignment.

#### Step 2: Configure your Deployment

1. In your Azure portal, open the **Managed Identities** menu.
2. Search for your managed identity, click **Properties**, then copy its **Name**, **Client ID**, **Tenant ID**, and **Resource group** name.
4. In the Astro UI, select your Deployment, click **Details**, then click **How to Configure...** under **Workload Identity**.
5. In **Managed Identity**, enter the Name of the managed identity you assigned to the resource.
6. In **Resource Group**, enter the **Resource group** name that your managed identity belongs to.
7. Using the Azure CLI, copy and run the provided command in your local terminal.
8. After the command completes, click **Close** on the modal in the Astro UI.
9. (Optional) repeat Steps 4 - 8 for any other Deployments that need to be authorized to Azure.

#### Step 3: Create an Airflow connection

1. In the Astro UI, click **Environment** in the main menu to open the **Connections** page.
2. Click **+ Connection** to add a new connection for your Workspace.
3. Search for **Azure**, then select the **Managed identity** option.
4. Configure your Airflow connection with the information you copied in the previous steps.
5. Link the connection to the Deployment(s) where you configured your managed identity.

Any DAG that uses your connection will now be authorized to Azure through your managed identity.

</TabItem>
</Tabs>

## See also
- [Manage Airflow connections and variables](manage-connections-variables.md)
- [Deploy code to Astro](deploy-code.md)
