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

- Manage Deployment’s with a large number of worker queues or Environment Variables.
- Manage your Deployments as files in a Github Repository
- You’d like to create a new Deployment that has the same or similar configuration of an already existing deployment
- Share Environment Variables and worker queues between Deployments
- You’d like to create Deployment Templates that can be used to create Deployments for different use cases. For example a Machine Learning Deployment Template can come with configurations, worker queues, and Variables needed for an ML Deployment at your company

# Deployment File Spec

The following section will explain the Deployment File Spec with the example below. The below example is a YAML file but Deployment files can be YAML or JSON files.

```yaml
deployment:
    environment_variables:
        - key: FOO
          value: bar
        - key: FOO2
          value:
          is_secret: true
    configuration:
        name: My Deployment
        description: test deployment create from file
        runtime_version: 7.0.0
        dag_deploy_enabled: false
        scheduler_au: 5
        scheduler_count: 1
        cluster_name: My Cluster
        workspace_name: My Workspace
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
# not needed or used when creating/updating a deployment
	metadata:
        deployment_id: clbh5ybjz110732503e94m13z7
        workspace_id: cl0v1p6lc728255byzyfs7lw21
        cluster_id: cl8woz99j003j0t37fpux1nbd
        release_name: geodetic-spectroscope-9368
        airflow_version: 2.5.0
        status: HEALTHY
        created_at: 2022-12-09T23:52:56.063Z
        updated_at: 2022-12-09T23:53:04.596Z
        deployment_url: cloud.astronomer-dev.io/cl0v1p6lc728255byzyfs7lw21/deployments/clbh5ybjz110732503e94m13z7/analytics
        webserver_url: astronomer.astronomer-dev.run/d94m13z7?orgId=org_dlgevirUCwI9vX10
```

The following is an example of deployment file that is created when you run `astro deployment inspect`. The `environment_variables`, `configuration`, `worker_queues`, and `alert_emails` sections can be used to create and update a Deployment. The `metadata` section only provides information about a deployment and is not needed when creating or deleting a deployment.

## Configuration

The `configuration` section can be used to create and update Astronomer Deployment with specific resources and configurable aspects. 

## Environment Variables

The `environment_variables` section can be used to create and update the Astronomer environment variables you see in the UI. The Deployment File will list the fields of all the variables a Deployment has. If a variable is marked as secret the value will not be shown but `is_secret` will be shown as `true`. You can however use the `environment_variables.value` field to update/create secret variables. Just make sure not to commit a Deployment file that contains a secret value to a github repo.

## Worker Queues

The `worker_queues` section can be used define a list of worker queues for a Deployment. All Deployments must have a worker queue named `default`. At least the name `default` needs to be listed to update or create a worker queues, default values will be used for the rest of the fields.

# Create a Deployment File

To create a deployment file from an existing Deployment run:

```bash
astro deployment inspect -d [deployment_id] > deployment.yaml
```

This file will look just like the file that is shown above. You can use this file to store and update the original Deployment with this file or create a new Deployment

# Create a Deployment with a Deployment File

To create a new Deployment based on the Deployment File you created below use the following command:

```bash
astro deployment create --name <new-deployment-name> --deployment-file deployment.yaml
```

The name provided with the `—name` flag will override name field in the Deployment file. If you’d like you could also delete the `metadata` section and change the `name`, `cluster_name`, or any section you’d like before running `astro deployment create`. A few notes on creating a Deployment with a Deployment file:

- The command flags always override the values given in the file.
- The `name` and `cluster_name` fields are the only fields required to create a deployment. The rest of the fields will be auto-populated by “smart defaults”.
- When creating worker queues only the `name` field is required. The rest of the fields will be auto populated with “smart defaults”.
- When creating Environment Variables your variable must have `key` and `value`

# Update a Deployment with a Deployment File

To update the Deployment you just created first make sure the `configuration.name` field is correct. Then update `deployment.yaml` to the configuration you want and run:

```bash
astro deployment update -d <deployment-id> --deployment-file deployment.yaml
```

You now can see your updated Deployment in the Astro UI. You can update any of the fields in the `environment_variables`, `configuration`, `worker_queues`, or `alert_emails` sections of the Deployment File. A few notes on updating a Deployment with a Deployment file:

- The command flags always override the values given in the file.
- You can’t change the Cluster the Deployment is running on. However you can create a new Deployment based on your file with a different Cluster for a similar result
- Your environment variables will be updated to match the `environment_variables` section in the file. This means that environment variables that currently exist in the Deployment but not in the file will be deleted. If a variable is secret omit the value from the file to ensure it doesn’t change during an update.
- Your worker queues will be updated to match the `worker_queues` section in the file. This means that worker queues that currently exist in the Deployment but not in the file will be deleted. Omitted values in the `worker_queues` section will fallback to there current value and not update to “smart defaults”.

# Next Steps:

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)