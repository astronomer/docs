---
sidebar_label: 'Manage Deployments as Code'
title: 'Manage Deployments as Code'
id: manage-deployments-as-code
---

<head>
  <meta name="description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
  <meta name="og:description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
</head>

After you configure your Astro Deployment, it can be stored, created or updated using a JSON or YAML Deployment file. Using Deployment files to manage your Deployments provides the following benefits:

- Quickly update Deployments with a large number of worker queues or environment variables.
- Manage Deployments as files from a Github repository.
- Transfer existing configuration settings to new Deployments. 
- Share environment variables and worker queues between Deployments.
- Create Deployment templates for specific use cases. For example, the worker queues and environment variables in an existing machine learning Deployment template can be repurposed in a machine learning Deployment.

## Deployment file contents

A Deployment file includes the following specifications:

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
        name: My Test Deployment
        description: A test Deployment created from a Deployment file
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
# not needed or used when creating or updating a deployment
        metadata:
        deployment_id: clbh5ybjz110732503e94m13z7
        workspace_id: cl0v1p6lc728255byzyfs7lw21
        cluster_id: cl8woz99j003j0t37fpux1nbd
        release_name: geodetic-spectroscope-9368
        airflow_version: 2.5.0
        status: HEALTHY
        created_at: 2022-12-09T23:52:56.063Z
        updated_at: 2022-12-09T23:53:04.596Z
        deployment_url: cloud.astronomer.io/cl0v1p6lc728255byzyfs7lw21/deployments/clbh5ybjz110732503e94m13z7/analytics
        webserver_url: astronomer.astronomer.run/d94m13z7?orgId=org_dlgevirUCwI9vX10
```

You can use the `environment_variables`, `configuration`, `worker_queues`, and `alert_emails` sections to create or update a Deployment. 

The `metadata` section is automatically populated when you run `astro deployment inspect` to check the status of an existing Deployment. Do not configure this section when creating or updating a Deployment with a Deployment file. 

### Configuration settings

The `configuration` section contains all settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Update a Deployment name and description](configure-deployment-resources.md#update-a-deployment-name-and-description)
- [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

### Environment variable settings

The `environment_variables` section contains configurations Deployment environment variables. See [Environment variables](environment-variables.md).

You can set `environment_variables.is_secret: true` on any new or existing environment variables to set them as secret, but you won't be able to retrieve the secret value from the Deployment once you push your configuration. Astronomer recommends that you avoid committing Deployment files containing secret values to GitHub repositories. If you are commiting these files to continually update deployments, update secret values manually and leave them blank in the file.

### Worker queue settings

The `worker_queues` section defines the worker queues for a Deployment. All Deployment files must include configuration for a `default` worker queue. If you don't enter specific values for a worker queue, smart default values based on your available worker types are applied.

## Create a Deployment file for an existing Deployment

Run the following command to create a Deployment file from an existing Deployment:

```bash
astro deployment inspect -n <deployment-name> > deployment.yaml
```

After the Deployment file is created, you can use it to update the settings of the original Deployment.

### Create a template file from an existing Deployment

Create a Deployment template file to programmatically create new Deployments based on configurations from an existing Deployment. A template file is YAML configuration file that includes all information about a Deployment except for its name, description field, and metadata.

To create a template file, run the following command. Replace `<deployment-template>` with your preferred name for the new template file.

```bash
astro deployment inspect -n <original-deployment-name> --template > <deployment-template>.yaml
```

## Create a Deployment from a template file

1. In your Deployment template file, provide a name for the new Deployment.
2. Run the following command to create a new Deployment based on the Deployment file:

    ```bash
    astro deployment create --deployment-file <deployment-template>.yaml
    ```

Keep the following in mind when creating a Deployment with a Deployment file:

- You can create a Deployment from a standard Deployment file generated by `astro deployment inspect`, but you must replace the existing Deployment name and description and remove the metadata before using it as a template. If you plan on using a Deployment's configuration as a template for future Deployments, Astronomer recommends using `astro deployment inspect --template`.
- The `name` and `cluster_name` fields are the only fields required to create a Deployment. The CLI will create the Deployment using default values for each unspecified configuration. These default values are the same default values for when you create a Deployment from the Cloud UI.
- When creating worker queues, the `name` and `worker_type` fields are required. Any unspecified fields are populated with smart defaults based on your cluster's available worker types. 
- When creating environment variables, each variable must include a `key` and a `value`.

## Update a Deployment with a Deployment file

:::danger 

You must push individual Deployment changes alongside all existing Deployment configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

Confirm the `configuration.name` field is correct for the Deployment, and then run the following command:

```bash
astro deployment update -d <deployment-id> --deployment-file deployment.yaml
```

The updated Deployment appears in the Cloud UI.

Keep the following in mind when when updating a Deployment with a Deployment file:

- You can’t change the cluster the Deployment runs on. However, you can use the Deployment file to create a new Deployment with a different cluster.
- You can't change the runtime version of the Deployment using this command. You can only change the runtime version by updatign your Docker file with the Deploy command.
- The Deployment's environment variables are updated to match the exact variables configured in `environment_variables`. Any variables that exist in the Deployment but are not in the Deployment file are deleted. If an environment variable is a secret, remove the value from the Deployment file to ensure it doesn’t change during an update.
- Worker queues are updated to match the `worker_queues` section in the Deployment file. Any existing worker queues that are in the Deployment but not in the Deployment file are deleted.

## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)