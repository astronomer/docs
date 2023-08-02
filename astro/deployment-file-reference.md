---
sidebar_label: 'Deployment file reference'
title: 'Deployment file reference'
id: deployment-file-reference
description: View all possible values that you can include in a Deployment file when managing Deployments as code.
---

When you [inspect a Deployment](cli/astro-deployment-inspect.md) to generate a Deployment file, its current configuration is generated. The output of this command includes the name, description, and metadata that is unique to the Deployment. This configuration is also available in the Cloud UI. It incldues the the following sections:

- `environment_variables`
- `configuration`
- `worker_queues`
- `alert_emails`
- `metadata`

A _Deployment template file_ is different from the _Deployment file_ such that it does not have the `metadata` and `environment_variables` section, and the `name` and `description` fields are empty. If you wish to use a deployment file as a template, you can remove the `metadata` section and update the other sections as required.

## Deployment file 

```yaml
deployment:
    environment_variables:
        - is_secret: true
          key: API_KEY
          updated_at: "2023-06-22T14:02:27.892Z"
          value: ""
    configuration:
        name: test
        description: ""
        runtime_version: 8.7.0
        dag_deploy_enabled: false
        ci_cd_enforcement: false
        scheduler_size: small
        is_high_availability: false
        executor: CeleryExecutor
        scheduler_au: 10
        scheduler_count: 1
        cluster_name: us-central1
        workspace_name: least-permission
        deployment_type: HOSTED_SHARED
        cloud_provider: gcp
        region: us-central1
    worker_queues:
        - name: default
          max_worker_count: 10
          min_worker_count: 0
          worker_concurrency: 5
          worker_type: a5
    metadata:
        deployment_id: clkcbz5d01458926ewbjzubt3fx
        workspace_id: clk7zoqbf00f901hka4c66q2d
        cluster_id: us-central1
        release_name: N/A
        airflow_version: 2.6.3
        current_tag: 8.7.0
        status: CREATING
        created_at: 2023-07-21T08:40:02.531Z
        updated_at: 2023-07-21T08:40:02.532Z
        deployment_url: cloud.astronomer.io/clk7zoqbf00f901hka4c66q2d/deployments/clkcbz5d01458926ewbjzubt3fx/analytics
        webserver_url: org.astronomer.run/dzubt3fx
        workload_identity: astro-native-magnify-8566@proj.iam.gserviceaccount.com
```

:::caution  

Note that when you add environment variables using deployment file, you must provide a value for the key `value` for your environment variable. Empty string ("") or leaving it blank will cause the `astro deployment create` command to fail.

:::

### `deployment.environment_variables`

You can create, update, or delete environment variables in the `environment_variables` section of the template file. This is equivalent to configuring environment variables in the **Variables** page of a Deployment in the Cloud UI.

When you inspect a Deployment, the value of any environment variable that is set as secret in the Cloud UI will not appear in the template file. To set any new or existing environment variables as secret in the file, specify `is_secret: true` next to the key and value. If you commit a template file to a GitHub repository, Astronomer recommends that you update the secret values manually in the Cloud UI and leave them blank in the file. This ensures that you do not commit secret values to a version control tool in plain-text.

### `deployment.configuration`

The `configuration` section contains all basic settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Create a Deployment](create-deployment.md#create-a-deployment).
- [Update a Deployment name and description](configure-deployment-resources.md#update-a-deployment-name-and-description).
- [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

### `deployment.worker_queues`

The `worker_queues` section defines the [worker queues](configure-worker-queues.md) for a Deployment. If you don't enter specific values for the `default` worker queue for a Deployment with CeleryExecutor, default values based on the worker types available on your cluster are applied. This section is not applicable to Deployments running KubernetesExecutor. 

### Other fields

- `scheduler_size` and `is_high_availability` are not applicable to Astro Hybrid. 
- `deployment_type` can be HOSTED_SHARED or HOSTED_DEDICATED for Astro Hosted depending on your [cluster_type](cli/astro-deployment-create.md#options). HOSTED_SHARED is another name for `standard` cluster_type and HOSTED_DEDICATED is another name for `dedicated` cluster_type. For Astro Hybrid, this will be `HYBRID`.
- `cluster_name` will contain your region name for HOSTED_SHARED `deployment_type` because you are running on a shared or standard cluster.

