---
sidebar_label: 'Manage Deployments as Code'
title: 'Manage Deployments as Code'
id: manage-deployments-as-code
---

<head>
  <meta name="description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
  <meta name="og:description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
</head>

Once you determine the configuration of your Astro Deployment this configuration can be stored, created or updated using a JSON or YAML Deployment file. Managing your Deployments with Deployment files has a few different use cases:

- Simplifies the management of Deployments with a large number of worker queues or environment variables.
- Allows Deployments to be managed as files in a Github repository.
- Allows the quick transfer of existing configuration settings to new Deployments. 
- Allows environment variables and worker queues to be shared between Deployments.
- You’d like to create Deployment Templates that can be used to create Deployments for different use cases. For example a Machine Learning Deployment Template can come with configurations, worker queues, and Variables needed for an ML Deployment at your company

# Deployment File Spec

A Deployment file includes the following specifications:

```yaml
deployment:
    environment_variables:
        - key: EXAMPLE
          value: test
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
          is_default: true
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

The following is an example of a Deployment file that is created when you run `astro deployment inspect`. You can use the `environment_variables`, `configuration`, `worker_queues`, and `alert_emails` sections to create and update a Deployment. The `metadata` section provides information about a Deployment and is not required when you create or delete a Deployment.

### Configuration settings

Edit the `configuration` section when you need to add or update Deployment settings. 

### Environment variable settings

You can modify the `environment_variables` section to add or update the environment variables displayed in the Cloud UI. The Deployment file lists all of the environment variables in a Deployment. If an environment variable is marked as secret, the value is not shown, but the `is_secret` value is `true`. You can use the `environment_variables.value` field to add or update secret environment variables. Astronomer recommends that you avoid committing Deployment files containing secret values to GitHub repositories.

### Worker queue settings

The `worker_queues` section defines the worker queues for a Deployment. All Deployment files must include a worker queue named `default` to allow worker queue settings to be added or updated, If you don't enter specific values for a worker queue, default values are applied.

## Create a Deployment file

Run the following command to create a Deployment file from an existing Deployment:

```bash
astro deployment inspect -d [deployment_id] > deployment.yaml
```

After the Deployment file is created, you can use it to update the settings of original Deployment, or you can use it to create a new Deployment

## Create a Deployment with a Deployment file

Run the following command to create a new Deployment with a Deployment file:

```bash
astro deployment create --name <new-deployment-name> --deployment-file deployment.yaml
```

The name provided with the `—name` flag will override name field in the Deployment file. If you’d like you could also delete the `metadata` section and change the `name`, `cluster_name`, or any section you’d like before running `astro deployment create`. A few notes on creating a Deployment with a Deployment file:

- The `name` and `cluster_name` fields are the only fields required to create a Deployment. The rest of the fields are autopopulated.
- When creating worker queues, only the `name` field is required. The rest of the fields are autopopulated.
- When creating environment variables, each variable must include a `key` and a `value`.

## Update a Deployment with a Deployment file

Confirm the `configuration.name` field is correct for the Deployment, and then run the following command:

```bash
astro deployment update -d <deployment-id> --deployment-file deployment.yaml
```

You now can see your updated Deployment in the Astro UI. You can update any of the fields in the `environment_variables`, `configuration`, `worker_queues`, or `alert_emails` sections of the Deployment File. A few notes on updating a Deployment with a Deployment file:

- You can’t change the Cluster the Deployment runs on. However, you can use the Deployment file to create a new Deployment with a different Cluster.
- Environment variables are updated to match the `environment_variables` section in the Deployment file. Environment variables that are in the Deployment but not in the Deployment file are deleted. If an environment variable is a secret, remove the value from the Deployment file to ensure it doesn’t change during an update.
- Worker queues are updated to match the `worker_queues` section in the Deployment file. Worker queues that are in the Deployment but not in the Deployment file are deleted. Omitted values in the `worker_queues` section keep their existing values and are not updated.

## Next steps:

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)