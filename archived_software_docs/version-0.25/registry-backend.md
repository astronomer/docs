---
title: 'Using Registry Back Ends in Astronomer Software'
sidebar_label: 'Use a Registry Backend'
id: registry-backend
---

## Overview

Astronomer Software requires a Docker Registry to store the Docker Images generated every time a user either pushes code or a configuration change to an Apache Airflow® Deployment on Astronomer.

The default storage backend for this Docker Registry is a [Kubernetes Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). While this may be sufficient for teams just getting started on Astronomer, we strongly recommend backing the registry with an external storage solution for any team running in production.

This doc will walk through configuring the 3 tools that Astronomer supports:

- [Google Cloud Storage](https://cloud.google.com/storage/)
- [AWS S3](https://aws.amazon.com/s3/)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)

## Google Cloud Storage

If you're running Astronomer Software on GCP GKE, we'd recommend Google Cloud Storage (GCS) as a registry backend solution. Read below for guidelines.

To read more about the Google Cloud Storage driver, reference [this doc](https://github.com/docker/docker.github.io/blob/master/registry/storage-drivers/gcs.md).

### Prerequisites

To use Google Cloud Storage (GCS) as a registry backend solution, you'll need:

- An existing GCS Bucket
- Your Google Cloud Platform Service Account JSON Key
- Ability to create a Kubernetes Secret in your cluster

### Update your config.yaml file

1. Download your Google Cloud Platform service account JSON key from [Google Console](https://console.cloud.google.com/apis/credentials/serviceaccountkey). Make sure the service account you use has both the `Storage Legacy Bucket Owner` and `Storage Object Admin` roles.

2. Create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) using the downloaded key:

```
kubectl create secret generic astronomer-gcs-keyfile --from-file astronomer-gcs-keyfile=/path/to/key.json -n <your-namespace>
```

3. Add the following to your config.yaml file:

```yaml
astronomer:
  registry:
    gcs:
      enabled: true
      bucket: my-gcs-bucket
```

Example:

```yaml
#################################
## Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

#################################
## Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: 0.0.0.0
  preserveSourceIP: true

#################################
## SMTP configuration
#################################  
astronomer:
  houston:
    config:
      email:
        enabled: true
        smtpUrl: YOUR_URI_HERE
  registry:
    gcs:
      enabled: true
      bucket: my-gcs-bucket
```

4. Push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).

## AWS S3

If you're running Astronomer Software on AWS EKS, we'd recommend AWS S3 as a registry backend solution. Read below for guidelines.

To read more about the AWS S3 storage driver, [go here](https://github.com/docker/docker.github.io/blob/master/registry/storage-drivers/s3.md).

### Prerequisites

To use AWS S3 as a registry backend solution, you'll need:

- An S3 bucket
- Your AWS Access Key
- Your AWS Secret Key
- Ability to create a Kubernetes Secret in your cluster

### Create S3 IAM Policy and User

To grant the registry appropriate push and pull permissions, follow the steps below.

1. Use the following definition to create a new AWS IAM policy, making sure to replace `S3_BUCKET_NAME` with your own S3 bucket's name:

```
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
      "Resource": "arn:aws:s3:::S3_BUCKET_NAME"
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
      "Resource": "arn:aws:s3:::S3_BUCKET_NAME/*"
    }
  ]
}
```

2. Create a new IAM User and attach the Policy. Your access key and secret key will be generated and displayed after the user is created.

3. Add the following to your `config.yaml` file:

```yaml
astronomer:
  registry:
    s3:
      enabled: true
      accesskey: my-access-key
      secretkey: my-secret-key
      region: us-east-1
      bucket: my-s3-bucket
```

4. Push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).

### Enable Encryption (_Optional_)

To enable encryption, follow the steps below.

1. Create a key in AWS Key Management Service (KMS). During the key creation process you'll be asked to add "key users". Add the user created above as a "key user".

2. Enable encryption by adding the following values to your `config.yaml` file:

```yaml
astronomer:
  registry:
    s3:
      enabled: true
      accesskey: my-access-key
      secretkey: my-secret-key
      region: us-east-1
      bucket: my-s3-bucket
      encrypt: true
      keyid: my-kms-key-id
```

3. Push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).

## Azure Blob Storage

If you're running Astronomer Software on Azure AKS, we'd recommend Azure Blob Storage as a registry backend solution. Read below for guidelines.

To read more about the Azure Blog Storage driver, [go here](https://github.com/docker/docker.github.io/blob/master/registry/storage-drivers/azure.md).


### Prerequisites

To use Azure Blog Storage as a registry backend solution, you'll need:

- Azure Storage Account Name
- Azure Account Access Key
- Azure Container Name

### Configure the registry backend

1. Add the following to your `config.yaml` file:

```yaml
astronomer:
  registry:
    azure:
      enabled: true
      accountname: my-account-name
      accountkey: my-account-key
      container: my-container-name
      realm: core.windows.net
```

2. Push the configuration change to your platform as described in [Apply a Platform Configuration Change on Astronomer](apply-platform-config.md).
