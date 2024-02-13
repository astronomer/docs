---
sidebar_label: 'Deployment file reference'
title: 'Deployment file reference'
id: deployment-file-reference
description: View all possible values that you can include in a Deployment file when managing Deployments as code.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import HostedBadge from '@site/src/components/HostedBadge';
import HybridBadge from '@site/src/components/HybridBadge';

After you create an Astro Deployment, you can use the Astro CLI to create a Deployment file that contains its unique configurations represented as code. That includes worker queues, environment variables, Astro Runtime version, and more. You can use Deployment files to manage Deployments programmatically on Astro.

When you [inspect a Deployment](cli/astro-deployment-inspect.md) to generate a Deployment file, its current configuration is generated as a YAML _Deployment file_. The file includes the name, description, and metadata that is unique to the Deployment.

A _Deployment template file_ is different from the _Deployment file_. A template file does not have the `metadata` and `environment_variables` section, and the `name` and `description` fields are empty. Deployment template files are used to create new Deployments, while a Deployment file of an existing Deployment can be used to update its configuration. To create a Deployment template file in YAML format, run `astro deployment inspect <your-deployment-id> --template > your-deployment.yaml`.

Use this document as a reference for all fields in both Deployment files and Deployment template files.

## Deployment file example

<Tabs
defaultValue="hosted"
values={[
{label: 'Hosted', value: 'hosted'},
{label: 'Hybrid', value: 'hybrid'},
]}>
<TabItem value="hosted">

The following is an example Deployment file that includes all possible key-value pairs for Astro Hosted:

```yaml
deployment:
    environment_variables:
        - is_secret: false
          key: PROJECT_NAME
          updated_at: "2023-06-22T14:02:26.281Z"
          value: test_project
        - is_secret: true
          key: API_KEY
          updated_at: "2023-06-22T14:02:27.892Z"
          value: ""
    configuration:
        name: test-standard
        description: ""
        runtime_version: 10.3.0
        dag_deploy_enabled: true
        ci_cd_enforcement: false
        scheduler_size: SMALL
        is_high_availability: false
        executor: CELERY
        cluster_name: "" ## Only used when deployment_type is DEDICATED
        workspace_name: least-permission
        deployment_type: STANDARD
        cloud_provider: gcp
        region: us-east4
        default_task_pod_cpu: "0.25" ## new field
        default_task_pod_memory: 0.5Gi ## new field
        resource_quota_cpu: "10" ## new field
        resource_quota_memory: 20Gi ## new field
    worker_queues: ## worker_queues only used when executor is CELERY
        - name: default
          max_worker_count: 10
          min_worker_count: 0
          worker_concurrency: 5
          worker_type: A5
		alert_emails:
        - test-email@testdomain.io
    metadata:
        deployment_id:
        workspace_id:
        cluster_id: us-central1
        release_name: N/A
        airflow_version: 2.6.3
        current_tag: 8.7.0
        status: CREATING
        created_at: 2023-07-21T08:40:02.531Z
        updated_at: 2023-07-21T08:40:02.532Z
        deployment_url:
        webserver_url:
        workload_identity:
```
</TabItem>
<TabItem value="hybrid">

The following is an example Deployment file that includes all possible key-value pairs for Astro Hybrid:

```yaml
deployment:
		environment_variables:
        - is_secret: false
          key: TEST
          updated_at: "2024-02-12T15:56:38.46620671Z"
          value: TESTVALUE
        - is_secret: true
          key: TEST2
          updated_at: "2024-02-12T15:56:38.46621831Z"
          value: ""
    configuration:
        name: test
        description: "hybrid deployment"
        runtime_version: 10.3.0
        dag_deploy_enabled: false
        ci_cd_enforcement: false
        is_high_availability: false
        executor: CELERY
        scheduler_au: 5
        scheduler_count: 1
        cluster_name:
        workspace_name:
        deployment_type: HYBRID
        cloud_provider: "aws"
        region: "us-west-2"
				default_worker_type: m5.xlarge ## default_worker_type only exist when executor is KUBERNETES
    worker_queues: ## worker_queues is only used when executor is CELERY
        - name: default
          max_worker_count: 10
          min_worker_count: 0
          worker_concurrency: 16
          worker_type: m5.xlarge
    metadata:
        deployment_id:
        workspace_id:
        cluster_id:
        release_name:
        airflow_version: 2.8.1
        current_tag: 10.3.0
        status: HEALTHY
        created_at: 2024-02-09T20:38:11.749Z
        updated_at: 2024-02-09T20:38:11.749Z
        deployment_url:
        webserver_url:
        workload_identity:
		alert_emails:
```


</TabItem>
</Tabs>

The following sections describe each section in the file.

### `deployment.environment_variables`

You can create, update, or delete environment variables in the `environment_variables` section of the template file. This is equivalent to configuring environment variables in the **Variables** page of a Deployment in the Cloud UI. Each variable in this section must include a `key` and a `value`.

By default, each variable is created as a non-secret variable. To set any new or existing environment variables as secret, specify `is_secret: true` in the same section as the key and value. For example:

```yaml
 - is_secret: true
    key: PROJECT_NAME
    value: test_project
```

When you inspect a Deployment, the value of secret environment variables do not appear in the Deployment file.

To delete an environment variable, remove the lines that contain its key, its value, and other associated fields. Then, reapply the file to the Deployment. Any variables that exist on the Deployment, but are not included in the most recently applied Deployment file, are deleted.

If you commit a template file to a GitHub repository, do not add secret environment variables in the file. Instead, add them manually in the Cloud UI. This ensures that you do not commit secret values to a version control tool in plain-text.

:::warning

When you add environment variables using a Deployment file, you must provide a `value` for your environment variable. Leaving this value blank or as an empty string (`""`) will cause the `astro deployment create` command to fail.

:::

### `deployment.configuration`

The `configuration` section contains all of the basic settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Create a Deployment](create-deployment.md#create-a-deployment).
- [Update a Deployment name and description](deployment-details.md#update-a-deployment-name-and-description).
- [Scheduler size](deployment-resources.md#scheduler-size).

### `deployment.worker_queues`

The `worker_queues` section defines the [worker queues](configure-worker-queues.md) for Deployments that use the Celery executor. This section is not applicable to Deployments that use Kubernetes executor.

If you don't enter specific values for the `default` worker queue for a Deployment, Astro uses default values based on the worker types available on your cluster. Each additional worker queue must include a `name` and `worker_type`. The Astro CLI uses default values for any other unspecified fields.

### Other fields

- `scheduler_size` and `is_high_availability` are not applicable to Astro Hybrid.
- `deployment_type` can be `HOSTED_SHARED` or `HOSTED_DEDICATED` for Astro Hosted depending on your [cluster type](cli/astro-deployment-create.md#options). Use `HOSTED_SHARED` for standard clusters and `HOSTED_DEDICATED` for dedicated clusters. For Astro Hybrid, the only option is `HYBRID`.
- `cluster_name` is the name for the cluster that appears in the Cloud UI for Astro Hosted and Hybrid.
