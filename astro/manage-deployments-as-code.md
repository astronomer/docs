---
sidebar_label: 'Manage Deployments as Code'
title: 'Manage Deployments as Code'
id: manage-deployments-as-code
---

<head>
  <meta name="description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
  <meta name="og:description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
</head>

After you configure your Astro Deployment, its unique configurations can be stored as a JSON or YAML Deployment file.

You can use Deployment files to manage your Deployment as code. Specifically:

- Create a template file from an existing Deployment and use it to programmatically create another Deployment with the same configurations. This is an alternative to creating a new Deployment in the Cloud UI and manually copying configurations.
- Update existing Deployments faster and more easily than doing so with the Cloud UI or individual Astro CLI flags.
- Manage Deployment configurations from a GitHub repository and in a single place.
- Create a single source of truth for Deployments with a particular use case. For example, standardize your team's configuration of sandbox environments.

## Create a template file from a Deployment

Create a Deployment template file to programmatically create new Deployments based on configurations from an existing Deployment. A template file is a YAML configuration file that includes all information about a Deployment except for its name, description field, and metadata.

To create a template file, run the following command. Replace `<deployment-template>` with your preferred name for the new template file.

### Template file contents

```yaml
deployment:
    environment_variables:
        - key: EXAMPLE
          value: test
          is_secret: false
        - key: EXAMPLE2
          value:
          is_secret: true
    configuration:
        # Name and description are left blank in template files. Configure these values when you create a new Deployment from the template file. 
        name: 
        description:
        runtime_version: 7.0.0
        dag_deploy_enabled: false
        scheduler_au: 5
        scheduler_count: 1
        cluster_name: Test Cluster
        workspace_name: Test Workspace
    worker_queues:
        - name: default
          max_worker_count: 10
          min_worker_count: 1
          worker_concurrency: 16
          worker_type: m5.xlarge
    alert_emails:
        - me@myorganization.com
        - me2@myorganization.com
# This section is only populated when inspecting a Deployment without creating a template. 
# Do not configure metadata when you create a new Deployment from a template. 
        metadata:
        deployment_id: 
        workspace_id: 
        cluster_id: 
        release_name: 
        airflow_version: 
        status: 
        created_at: 
        updated_at: 
        deployment_url: 
        webserver_url: 
```

You can use the `environment_variables`, `configuration`, `worker_queues`, and `alert_emails` sections to create or update a Deployment. 

The `metadata` section is automatically populated when you run `astro deployment inspect` to check the status of an existing Deployment. Do not configure this section when creating or updating a Deployment with a Deployment file. 

#### `deployment.configuration`

The `configuration` section contains all settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Update a Deployment name and description](configure-deployment-resources.md#update-a-deployment-name-and-description)
- [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

#### `deployment.environment_variables`

The `environment_variables` section contains configurations for Deployment environment variables. See [Environment variables](environment-variables.md).

You can set `environment_variables.is_secret: true` on any new or existing environment variables to set them as secret, but you won't be able to retrieve the secret value from the Deployment once you push your configuration. Astronomer recommends that you avoid committing Deployment files containing secret values to GitHub repositories. If you are committing these files to continually update a Deployment, update the secret values manually in the Cloud UI and leave them blank in the file.

#### `deployment.worker_queues`

The `worker_queues` section defines the worker queues for a Deployment. All Deployment files must include configuration for a `default` worker queue. If you don't enter specific values for a worker queue, smart default values based on your available worker types are applied.

### Create a Deployment from a template file

Before you create a Deployment from a template file, keep the following in mind:

- You can create a Deployment from a standard Deployment file generated by `astro deployment inspect`, but you must replace the existing Deployment name and description and remove the metadata before using it as a template. If you plan on using a Deployment's configuration as a template for future Deployments, Astronomer recommends using `astro deployment inspect --template`.
- The `name` and `cluster_name` fields are the only fields required to create a Deployment. The CLI will create the Deployment using default values for each unspecified configuration. These default values are the same default values for when you create a Deployment from the Cloud UI.
- When creating worker queues, the `name` and `worker_type` fields are required. Any unspecified fields are populated with smart defaults based on your cluster's available worker types. 
- When creating environment variables, each variable must include a `key` and a `value`.

1. In your Deployment template file, provide a name for the new Deployment.
2. Run the following command to create a new Deployment based on the Deployment file:

    ```bash
    astro deployment create --deployment-file <deployment-template>.yaml
    ```

## Inspect a Deployment

Run the following command to create a Deployment file from an existing Deployment:

```sh
astro deployment inspect -n <deployment-name> > deployment.yaml
```

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but additionally contains your Deployment's metadata, name, and description. See [Template file contents](#template-file-contents) for a list of all configurable values. You can use a Deployment file to programmatically update the associated Deployment.

### Update a Deployment using a Deployment file

:::danger 

You must push individual Deployment changes alongside all existing Deployment configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

After you create a Deployment file by inspecting a Deployment, you can modify the file and use it to update your Deployment's configurations. You can modify all Deployment configurations except for `cluster_name`, `workspace_name`, and `metadata`.

Run the following command to update your Deployment based on `<your-deployment-file>`:

```sh
astro deployment update -d <deployment-id> --deployment-file <your-deployment-file>
```

Keep the following in mind when when updating a Deployment with a Deployment file:

- You can’t change the cluster the Deployment runs on. However, you can use the Deployment file to create a new Deployment with a different cluster.
- You can't change the runtime version of the Deployment using this command. You can only change the runtime version by updating your Docker file with the Deploy command.
- The Deployment's environment variables are updated to match the exact variables configured in `environment_variables`. Any variables that exist in the Deployment but are not in the Deployment file are deleted. If an environment variable is a secret, remove the value from the Deployment file to ensure it doesn’t change during an update.
- Worker queues are updated to match the `worker_queues` section in the Deployment file. Any existing worker queues that are in the Deployment but not in the Deployment file are deleted.

## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)