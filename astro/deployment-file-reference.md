---
sidebar_label: 'Deployment file reference'
title: 'Deployment file reference'
id: deployment-file-reference
description: View all possible values that you can include in a Deployment file when managing Deployments as code.
---

After you create an Astro Deployment, you can use the Astro CLI to create a Deployment file that contains its unique configurations represented as code. That includes worker queues, environment variables, Astro Runtime version, and more. You can use Deployment files to manage Deployments programmatically on Astro.

When you [inspect a Deployment](cli/astro-deployment-inspect.md) to generate a Deployment file, its current configuration is generated as a YAML _Deployment file_. The file includes the name, description, and metadata that is unique to the Deployment.

A _Deployment template file_ is different from the _Deployment file_. A template file does not have the `metadata` and `environment_variables` section, and the `name` and `description` fields are empty. Deployment template files are used to create new Deployments, while a Deployment file of an existing Deployment can be used to update its configuration. To create a Deployment template file in YAML format, run `astro deployment inspect <your-deployment-id> --template > your-deployment.yaml`.

Use this document as a reference for all fields in both Deployment files and Deployment template files. 

## Deployment file example

The following is an example Deployment file that includes all possible key-value pairs:

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

The following sections describe each section in the file.

### `deployment.environment_variables`

You can create, update, or delete environment variables in the `environment_variables` section of the template file. This is equivalent to configuring environment variables in the **Variables** page of a Deployment in the Cloud UI. When you create or update a variable, each variable in this section must include a `key` and a `value`. By default, each variable is created as a non-secret variable.

To set any new or existing environment variables as secret in the file, specify `is_secret: true` next to the key and value.

To delete an environment variable, remove the lines that contain its key, its value, and other associated fields.

When you inspect a Deployment, the value of any secret environment variables will not appear in the template file.  

If you commit a template file to a GitHub repository, do not add secret environment variables in the file. Instead, add them manually in the Cloud UI. This ensures that you do not commit secret values to a version control tool in plain-text.

:::caution  

When you add environment variables using a Deployment file, you must provide a `value` for your environment variable. Leaving this value blank or as an empty string (`""`) will cause the `astro deployment create` command to fail.

:::

### `deployment.configuration`

The `configuration` section contains all of the basic settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Create a Deployment](create-deployment.md#create-a-deployment).
- [Update a Deployment name and description](deployment-settings.md#update-a-deployment-name-and-description).
- [Scheduler resources](deployment-settings.md#scheduler-resources).

### `deployment.worker_queues`

The `worker_queues` section defines the [worker queues](configure-worker-queues.md) for a Deployment with CeleryExecutor. This section is not applicable to Deployments running with the Kubernetes executor. 

If you don't enter specific values for the `default` worker queue for a Deployment, default values based on the worker types available on your cluster are applied. Each additional worker queue must include a `name` and `worker_type`. The Astro CLI will use default values for any other unspecified fields.


### Other fields

- `scheduler_size` and `is_high_availability` are not applicable to Astro Hybrid. 
- `deployment_type` can be `HOSTED_SHARED` or `HOSTED_DEDICATED` for Astro Hosted depending on your [cluster type](cli/astro-deployment-create.md#options). Use `HOSTED_SHARED` for standard clusters and `HOSTED_DEDICATED` for dedicated clusters. For Astro Hybrid, the only option is `HYBRID`.
- `cluster_name` is be the region name for Hosted standard clusters. For Astro Hybrid and Astro Hosted dedicated clusters, it's the name for the cluster that appears in the Cloud UI. 
