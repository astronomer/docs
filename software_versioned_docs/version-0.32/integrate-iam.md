---
sidebar_label: 'Integrate IAM roles'
title: 'Integrate IAM roles on Astronomer Software'
id: integrate-iam
description: Append IAM roles to an Airflow Deployment on Astronomer Software.
---

On Astronomer, IAM roles can be appended to the webserver, scheduler and worker pods within any individual Airflow Deployment on the platform.

IAM roles on [AWS](https://aws.amazon.com/iam/faqs/) and other platforms are often used to manage the level of access a specific user (or object, or group of users) has to some resource (or set of resources). The resource in question could be an S3 bucket or Secret Backend, both of which are commonly used in tandem with Airflow and Astronomer and can now be configured to be accessible only to a subset of Kubernetes pods within your wider Astronomer cluster.

## Implementation Considerations

Consider the following when you integrate IAM roles:

* All pods within your Airflow Deployment assume the IAM role. There is currently no way to use more than one IAM role per Deployment.
* If you’d like your IAM role to apply to more than one Deployment, you must annotate each Deployment.
* You must use the Astro CLI to pass IAM role annotations.
* Only Workspace Admins can pass IAM role annotations.
* Once a Deployment is created or updated with an IAM role, the annotation can't be deleted.

## Prerequisites

* [The Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
* Admin access on an Astronomer Workspace
* Direct access to your Kubernetes cluster (for example, permission to run `$ kubectl describe po`)
* A compatible version of Kubernetes as described in Astronomer's [Version compatibility reference](version-compatibility-reference.md)

## AWS

Before you can integrate IAM with an Airflow Deployment on Astronomer, you'll need to do the following within AWS:

- Create an IAM OIDC Identity Provider
- Create an IAM Policy
- Create an IAM role
- Create a Trust Relationship

### Step 1: Create an IAM OIDC identity provider

1. Retrieve your EKS cluster with the following AWS CLI command:

    ```bash
    aws eks list-clusters
    ```

    The output of this command should look something like this:

    ```json
    {
        "clusters": [
            "<your-cluster>"
        ]
    }
    ```

2. Retrieve and make note of your cluster's OIDC issuer URL with the following AWS CLI command:

    ```bash
    aws eks describe-cluster --name <your-cluster> --query "cluster.identity.oidc.issuer" --output text
    ```

    The output of this command should be a URL with the format `https://oidc.eks.[region].amazonaws.com/id/[id]`.

3. Open the [IAM console](https://console.aws.amazon.com/iam/).
4. In the navigation pane, click **Identity Providers** > **Create Provider**.
5. For **Provider Type**, click **Choose a provider type** > **OpenID Connect**.
6. For **Provider URL**, use the OIDC issuer URL for your cluster.
7. For **Audience**, use `sts.amazonaws.com`.
8. Verify that the provider information is correct, and then click **Add provider** to create your identity provider.

For additional information, refer to [Enable IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html).

### Step 2: Create an IAM policy

1. Open the IAM console at https://console.aws.amazon.com/iam/.
2. In the navigation panel, click **Policies** > **Create Policy**.
3. Open the **JSON** tab.
4. In the Policy Document field, specify the permissions you'd like to apply (or restrict) to the resource in question (e.g. read / write access to an AWS S3 bucket). You can also use the visual editor to construct your own policy.

    The following example will grant your IAM role read/write permissions to an S3 bucket named `astronomer-bucket`:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                    "s3:ListBucketMultipartUploads"
                ],
                "Resource": "arn:aws:s3:::astronomer-bucket"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject",
                    "s3:ListMultipartUploadParts",
                    "s3:AbortMultipartUpload"
                ],
                "Resource": "arn:aws:s3:::astronomer-bucket/*"
            }
        ]
    }
    ```

5. Review and create your policy.

### Step 3: Create an IAM role

1. Open the IAM console at https://console.aws.amazon.com/iam/.
2. In the navigation panel, go to **Roles** > **Create Role**.
3. In the **Select trusted entity** section, choose **AWS service** and **EC2**. Choose **Next**.
4. In the **Add permissions** section, select your policy created in the previous section. Choose **Next.**
5. In the **Name, review, and create** section, enter a name for your role and click **Create role**.

For additional information, refer to [Create service account IAM Policy and Role](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html).

### Step 4: Create a trust relationship

To create a trust relationship between your IAM role and OIDC identity provider:

1. Open the IAM console at https://console.aws.amazon.com/iam/.
2. In the navigation panel, choose **Roles** and open your role created in the previous section.
3. Select the **Trust relationships** tab and choose **Edit trust policy**.
4. Create a trust relationship between your IAM role and OIDC identity provider with the following format:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "arn:aws:iam::AWS_ACCOUNT_ID:oidc-provider/OIDC_PROVIDER"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringLike": {
              "OIDC_PROVIDER:sub": "system:serviceaccount:SERVICE_ACCOUNT_NAMESPACE:SERVICE_ACCOUNT_NAME"
            }
          }
        }
      ]
    }
    ```

    Example:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "arn:aws:iam::<your-iam-id>:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEA829F4B2854D8DAE63782CE90"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringLike": {
              "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEA829F4B2854D8DAE63782CE90:sub": "system:serviceaccount:astronomer-*:*"
            }
          }
        }
      ]
    }
    ```

For additional information, refer to [IAM role Configuration](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-technical-overview.html#iam-role-configuration).

### Step 5: Integrate your IAM role with Astronomer

In order to apply your IAM role to any Airflow Deployment on Astronomer, you'll need to explicitly pass an annotation key to the platform. To do so:

1. Set the following in your `config.yaml` file under `astronomer.houston.config.deployments`:

    ```yaml
    serviceAccountAnnotationKey: eks.amazonaws.com/role-arn
    ```

    Example:

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
            serviceAccountAnnotationKey: eks.amazonaws.com/role-arn
    ```

2. Push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).

### Step 6: Create or update an Airflow Deployment with an attached IAM role

1. To create a new Airflow Deployment with your IAM role attached, run the following Astro CLI command:

    ```sh
    astro deployment create <deployment-id> --executor=celery --cloud-role=arn:aws:iam::<your-iam-id>:role/<your-role>
    ```

    Alternatively, to update an existing Airflow Deployment with your IAM role attached, run the following:

    ```sh
    astro deployment update <deployment-id> --cloud-role=arn:aws:iam::<your-iam-id>:role/<your-role>
    ```

2. Confirm the role was passed successfully to all webserver, scheduler and worker pods within your Airflow Deployment by running the following command:

    ```bash
    kubectl describe po <pod-name> -n <airflow-namespace>
    ```

    You should see the following in your output:

    ```yaml
    AWS_ROLE_ARN: arn:aws:iam::<your-iam-id>:role/<your-role>
    AWS_WEB_IDENTITY_TOKEN_FILE: /var/run/secrets/eks.amazonaws.com/serviceaccount/token
    ```

> **Note:** If using Airflow `1.10.5`, you'll need to add `boto3 >=1.9` and `botocore >= 1.12` to your `requirements.txt` file.

## GCP

[Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) is a secure and manageable way to access Google Cloud services from applications running on GKE. This guide walks through the necessary steps for integrating IAM roles with Airflow Deployments running on GKE using Workload Identity.

### Step 1: Enable workload identity on your GKE cluster

1. Create a new cluster with Workload Identity enabled by running the following command:

    ```bash
    gcloud container clusters create <cluster-name> \
      --workload-pool=<project-id>.svc.id.goog
    ```

    Alternatively, run the following to enable Workload Identity on an existing cluster:

    ```bash
    gcloud container clusters update <cluster-name> \
      --workload-pool=<project-id>.svc.id.goog
    ```

2. Configure your node pool to use Workload Identity by running the following command:

    ```bash
    gcloud container node-pools update <nodepool-name> \
      --cluster=<cluster-name> \
      --workload-metadata=GKE_METADATA
    ```

### Step 2: Create a GCP service account

To create a GCP service account, run the following command:

```bash
gcloud iam service-accounts create <gsa-name>
```

### Step 3: Configure Astronomer

Add the following to your `config.yaml` file and push it to your platform as described in [Apply a config change](apply-platform-config.md):

```yaml
astronomer:
  houston:
    config:
      deployments:
        serviceAccountAnnotationKey: iam.gke.io/gcp-service-account
```

### Step 4: Create an Airflow Deployment

1. Create an Airflow Deployment with your GCP service account attached by running the following command:

    ```bash
    astro deployment create <deployment-name> --executor=celery --cloud-role=<gsa-name>@<project-id>.iam.gserviceaccount.com
    ```

2. Note the name of the worker and scheduler service accounts that appear when you run the following command:

    ```bash
    kubectl get sa -n <your-airflow-namespace>
    ```

3. Create an IAM policy binding your Google and GKE service accounts by running the following command for both the worker and scheduler GKE service accounts you noted:

    ```bash
    gcloud iam service-accounts add-iam-policy-binding \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:<project-id>.svc.id.goog[<your-airflow-namespace>/<airflow-worker-service-account-name>]" \
    <gsa-name>@<project-id>.iam.gserviceaccount.com
    ```

### Step 5: Confirm Workload Identity is working

1. Create an interactive session by running the following command:

    ```bash
      kubectl run -it \
      --image google/cloud-sdk:slim \
      --overrides='{ "spec": { "serviceAccount": "<airflow-worker-service-account-name>" } }' \
      --namespace <your-airflow-namespace> \
      workload-identity-test
    ```

2. In the interactive session, confirm you're able to authenticate successfully via Workload Identity by running the following command:

    ```bash
    gcloud auth list
    ```

    If Workload Identity is working, you should see a list of credentialed accounts related to your GCP service account.
