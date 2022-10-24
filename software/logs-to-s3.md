---
title: 'Forward Astronomer Software logs to Amazon S3'
sidebar_label: 'Forward task logs to S3'
id: logs-to-s3
description: Configure Astronomer Software to forward logs to Amazon S3.
---

If you're running Astronomer Software and are interested in making Airflow task logs available in an Amazon S3 bucket, you're more than free to do so on the platform.

For context, Astronomer Software leverages [Fluentd](https://www.fluentd.org/) as a data collector that is responsible for scraping and cleaning Airflow task logs to then send to [Elasticsearch](https://www.elastic.co/elasticsearch/), a search engine used to centralize and index logs from Airflow. The Airflow webserver pulls from Elasticsearch to render those logs directly to the user in the Airflow UI.

The guidelines below will outline how to forward Airflow logs from Fluentd via an existing Fluentd to S3 plugin. For more information on the plugin itself, reference the following:

- [Fluentd docs on the `out_s3` Output Plugin](https://docs.fluentd.org/output/s3)
- [Fluentd GitHub repo for the Amazon S3 Plugin](https://github.com/fluent/fluent-plugin-s3)

Fluentd will continue to forward logs to Elasticsearch in addition to the destination you additionally configure, so we strongly recommend keeping the Elasticsearch output.

> **Note:** The logs in question in this doc are Airflow logs, NOT Astronomer platform logs from Houston, the Registry, etc. They're the equivalent of deployment-level logs exposed in the 'Logs' tab of the Software UI and task logs rendered in the Airflow UI.

### Prerequisites

To configure log forwarding from Fluentd to Amazon S3, you'll need:

- An existing S3 Bucket
- An EKS worker node autoscaling policy

Follow the guidelines below for step-by-step instructions.

### Configure IAM policy and role

**1. Create an AWS IAM policy with the following permissions**

The first step in configuring Airflow task logs to be forwarded to Amazon S3 is to create an IAM policy on AWS and grant it the following 3 roles:

- `s3:ListBucket`
- `s3:PutObject`
- `s3:GetObject`

The IAM policy should look like the following:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::my-s3-bucket"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::my-s3-bucket/*"
    }
  ]
}
```

For more information on S3 permissions, read the ["Amazon S3 Actions" doc from AWS](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.html).

**2. Create an AWS IAM role and attach the policy created in Step 1**

Now, create an IAM role and attach the policy created above. You can do so via the AWS Management Console or the AWS CLI, among other tools.

For more information, refer to the ["Creating IAM roles" doc from AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html).

### Configure EKS worker node policy

**1. Allow your EKS nodes to assume your new IAM role**

Find your EKS worker node autoscaling policy for your EKS cluster. The policy `arn` should look like: `arn:aws:iam::123456789:policy/eks-worker-autoscaling-astronomer-5dyw2O4d20200730104135818400000008`.

Add the following section to the policy:

```
{
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": "arn:aws:iam::123456789:role/my-role"
}
```

**2. Add a Trust Relationship between your EKS nodes and your new IAM role**

Add the following section to the role created in the section above:

```
{
    "Effect": "Allow",
    "Principal": {
    "AWS": "arn:aws:iam::123456789:role/astronomer-5dyw2O4d20200730104135764200000006"
    },
    "Action": "sts:AssumeRole"
}
```

This will allow your EKS nodes to assume the role created above, giving them the necessary permissions to write to S3.

### Enable Fluentd to S3 in your config.yaml file

In your `config.yaml` file, add the following values:

```
fluentd:
  s3:
    enabled: true
    role_arn: arn:aws:iam::123456789:role/my-role
    role_session_name: my-session-name
    s3_bucket: my-s3-bucket
    s3_region: us-east-1
```

Then, push the configuration change to your platform as described in [Apply a config change](apply-platform-config.md).
