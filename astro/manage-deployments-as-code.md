---
sidebar_label: 'Manage Deployments as Code'
title: 'Manage Deployments as Code'
id: manage-deployments-as-code
---

<head>
  <meta name="description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
  <meta name="og:description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
</head>

After you create and configure your Astro Deployment, you can create a Deployment file in JSON or YAML format that contains its unique configurations. That includes worker queues, environment variables, and Astro Runtime version. You can use Deployment files to create and manage Deployments as code on Astro.

Specifically, you can:

- Create a template file from an existing Deployment and use it to programmatically create another Deployment with the same configurations. This is an alternative to creating a new Deployment in the Cloud UI and manually copying configurations.
- Store a Deployment file that represents the configurations of an existing Deployment in a central GitHub repository. You can make changes to this file to update a Deployment faster and more easily than doing so with the Cloud UI or individual Astro CLI flags.
- Save a template file in a central GitHub repository and use it as a source of truth for new Deployments that fit a particular use case. For example, standardize your team's configuration of development environments.

## Inspect a Deployment

You can inspect an existing Deployment with the Astro CLI to create a template file of its configurations. A template file is created in JSON or YAML format and includes all information about a Deployment except for its name, description, and metadata. You can use template files to programmatically create new Deployments based on configurations from an existing Deployment.

To create a template file, run the following command. Replace `<deployment-template-file-name>` with your preferred name for the new template file. For example, `deployment.yaml` or `deployment.json`.

```sh
astro deployment inspect <deployment-id> <deployment-name> --template
```

For more information about inspecting a Deployment, see [Astro CLI command reference](/cli/astro-deployment-inspect.md).

:::tip

To see the complete configuration of a Deployment directly in your terminal and without creating a file, run:

```
astro deployment inspect <deployment-name>
```

The output of this command includes the name, description, and metadata that is unique to the Deployment.

:::

### Template file reference

When you inspect a Deployment and create a template file, the file will contain the following sections:

- `environment_variables`
- `configuration`
- `worker_queues`
- `alert_emails`

If you use a template file to create or update a new Deployment, you might choose to change these values. All information in the template file is also available in the Cloud UI.

```yaml
deployment:
    environment_variables:
        - is_secret: false
          key: ENVIRONMENT
          value: Dev
        - is_secret: true
          key: AWS_ACCESS_KEY_ID
          value: "
    configuration:
        # Name and description are left blank in template files because they are unique to a single Deployment. Manually specify these values when you create a new Deployment from a template file.
        name: ""
        description: ""
        runtime_version: 7.0.0
        dag_deploy_enabled: true
        scheduler_au: 5
        scheduler_count: 1
        cluster_name: AWS Cluster
        workspace_name: Data Science Workspace
    worker_queues:
        - name: default
          max_worker_count: 10
          min_worker_count: 1
          worker_concurrency: 16
          worker_type: m5.xlarge
         worker_queues:
        - name: machine-learning-tasks
          max_worker_count: 4
          min_worker_count: 0
          worker_concurrency: 10
          worker_type: m5.8xlarge
    alert_emails:
        - paola@cosmicenergy.io
        - viraj@cosmicenergy.io
```

The following sections in this guide include information about each key and value within these sections in the template file. 

#### `deployment.configuration`

The `configuration` section contains all settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Create a Deployment](https://docs.astronomer.io/astro/create-deployment)
- [Update a Deployment name and description](configure-deployment-resources.md#update-a-deployment-name-and-description)
- [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

#### `deployment.environment_variables`

You can create, update, or delete environment variables in the `environment_variables` section of the template file. This is equivalent to configuring environment variables in the **Variables** page of a Deployment in the Cloud UI.

You can set `environment_variables.is_secret: true` on any new or existing environment variables to set them as secret, but you won't be able to retrieve the secret value from the Deployment once you push your configuration. Astronomer recommends that you avoid committing any files containing secret values to GitHub repositories. If you are committing these files to continually update a Deployment, update the secret values manually in the Cloud UI and leave them blank in the file.

See [Environment variables](environment-variables.md).

#### `deployment.worker_queues`

The `worker_queues` section defines the worker queues for a Deployment. All Deployment files must include configuration for a `default` worker queue. If you don't enter specific values for the `default` worker queue, default values based on the worker types available on your cluster are applied.

See [Worker queues](configure-worker-queues.md).

## Create a Deployment from a template file

When you create a new Deployment from a template file, the template file becomes a Deployment file. A Deployment file is intended to be applied to a specific Deployment and requires a unique Deployment name. Before you create a Deployment from a template file, keep the following in mind:

- You can create a new Deployment from a template file generated by `astro deployment inspect`, but you must replace the existing Deployment name before using it as a template. You can optionally leave the description blank.
- The `name` and `cluster_name` fields are the only fields required to create a Deployment. The CLI will create the Deployment using default values for each unspecified configuration. These default values are the same default values for when you create a Deployment from the Cloud UI.
- When creating worker queues, the `name` and `worker_type` fields are required. Any unspecified fields are populated with smart defaults based on your cluster's available worker types. 
- When creating environment variables, each variable must include a `key` and a `value`.

1. In your Deployment template file, provide a name for the new Deployment.
2. Run the following command to create a new Deployment based on the Deployment file:

    ```bash
    astro deployment create --deployment-file <deployment-template>.yaml
    ```

## Update a Deployment using a Deployment file

:::danger 

You must push individual Deployment changes alongside all existing Deployment configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but additionally contains your Deployment's metadata, name, and description. See [Template file contents](#template-file-contents) for a list of all configurable values. You can use a Deployment file to programmatically update the associated Deployment.

After you create a Deployment file by inspecting a Deployment, you can modify the file and use it to update your Deployment's configurations. You can modify all Deployment configurations except for `cluster_name`, `workspace_name`, and `metadata`.

Keep the following in mind when when updating a Deployment with a Deployment file:

- You can’t change the cluster the Deployment runs on. However, you can use the Deployment file to create a new Deployment with a different cluster.
- You can't change the runtime version of the Deployment using this command. You can only change the runtime version by updating your Docker file with the Deploy command.
- The Deployment's environment variables are updated to match the exact variables configured in `environment_variables`. Any variables that exist in the Deployment but are not in the Deployment file are deleted. If an environment variable is a secret, remove the value from the Deployment file to ensure it doesn’t change during an update.
- Worker queues are updated to match the `worker_queues` section in the Deployment file. Any existing worker queues that are in the Deployment but not in the Deployment file are deleted.

To update a Deployment using a Deployment file:

1. Create a Deployment file from an existing Deployment:

```sh
astro deployment inspect -n <deployment-name> <your-deployment-file>
```

2. Update your Deployment based on `<your-deployment-file>`:

```sh
astro deployment update -d <deployment-name> --deployment-file <your-deployment-file>
```

3. Go to the Deployment page in the Cloud UI to confirm the new values of your Deployment.

## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)
