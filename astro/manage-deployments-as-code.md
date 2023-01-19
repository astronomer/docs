---
sidebar_label: 'Manage Deployments as Code'
title: 'Manage Deployments as Code'
id: manage-deployments-as-code
---

<head>
  <meta name="description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
  <meta name="og:description" content="Manage an Astro Deployment with JSON or YAML Deployment file. This Deployment file can be used to store, create, or update a Deployment's configuration." />
</head>

After you create an Astro Deployment, you can create a file with the Astro CLI that contains its unique configurations represented as code. That includes worker queues, environment variables, and Astro Runtime version. You can use Deployment files to create and manage Deployments programmatically on Astro.

Specifically, you can:

- Create a template file from an existing Deployment and use it to create another Deployment with the same configurations. This is an alternative to creating a new Deployment in the Cloud UI and manually copying configurations.
- Store a Deployment file that represents the configurations of an existing Deployment. You can make changes to this file to update a Deployment faster and more easily than doing so with the Cloud UI or individual Astro CLI commands.
- Save a template file in a central GitHub repository and use it as a source of truth for new Deployments that fit a particular use case. For example, you can standardize your team's development environments by creating a template file with configurations for that type of Deployment.

## Inspect a Deployment

You can inspect an existing Deployment with the Astro CLI to create a template file of its configurations. A template file is created in YAML or JSON format and includes all information about a Deployment except for its name, description, and metadata. You can use template files to programmatically create new Deployments based on configurations from an existing Deployment.

To create a template file, run the following command. Replace `<deployment-template-file-name>` with your preferred name for the new template file. For example, `dev-deployment.yaml` or `dev-deployment.json`.

```sh
# save the template to a YAML file
astro deployment inspect <deployment-name>  --template  > <deployment-template-file-name>
# save the template to a JSON file
astro deployment inspect <deployment-name>  --template --output json > <deployment-template-file-name>
# print the template to your terminal
astro deployment inspect <deployment-name>  --template
```

For more information about inspecting a Deployment, see [Astro CLI command reference](/cli/astro-deployment-inspect.md).

:::tip

To see the complete configuration of a Deployment directly in your terminal and without creating a template file, run:

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

When you use a template file to create a new Deployment, you might choose to change these values. All information in the template file is also available in the Cloud UI. See the following template file as an example.

```yaml
deployment:
    environment_variables:
        - is_secret: false
          key: ENVIRONMENT
          value: Dev
        - is_secret: true
          key: AWS_ACCESS_KEY_ID
          value: ""
    configuration:
        # Name and description are replaced with placeholder values (`""`) in a template file. Manually specify these values when you create a new Deployment.
        name: ""
        description: ""
        runtime_version: 7.1.0
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

#### `deployment.environment_variables`

You can create, update, or delete environment variables in the `environment_variables` section of the template file. This is equivalent to configuring environment variables in the **Variables** page of a Deployment in the Cloud UI.

When you inspect a Deployment, the value of any environment variable that is set as secret in the Cloud UI will not appear in the template file. To set any new or existing environment variables as secret in the file, specify `is_secret: true` next to the key and value. If you commit a template file to a GitHub repository, Astronomer recommends that you update the secret values manually in the Cloud UI and leave them blank in the file. This ensures that you do not commit secret values to a version control tool in plain-text.

See [Environment variables](environment-variables.md).

#### `deployment.configuration`

The `configuration` section contains all basic settings that you can configure from the Deployment **Details** page in the Cloud UI. See:

- [Create a Deployment](create-deployment.md#create-a-deployment).
- [Update a Deployment name and description](configure-deployment-resources.md#update-a-deployment-name-and-description).
- [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

#### `deployment.worker_queues`

The `worker_queues` section defines the worker queues for a Deployment. All Deployment files must include configuration for a `default` worker queue. If you don't enter specific values for the `default` worker queue, default values based on the worker types available on your cluster are applied.

See [Worker queues](configure-worker-queues.md).

## Create a Deployment from a template file

You can create a Deployment in the Astro CLI according to the configurations specified in a given template file. Before you do so, keep the following in mind:

- Deployment names must be unique within a single Workspace. Make sure that you replace the `name` field in the file with the desired name of your new Deployment.
- The `name` and `cluster_name` fields are the only fields required to create a Deployment. The CLI will create the Deployment using default values for each unspecified configuration. These default values are the same default values that are used when you create a Deployment from the Cloud UI.
- When creating worker queues, the `name` and `worker_type` fields are required. Any unspecified fields are populated with smart defaults based on the worker types available in your cluster.
- When creating environment variables, each variable must include a `key` and a `value`.

To create a new Deployment from an existing template file:

1. In your template file, provide a name for the new Deployment.
2. Run:

    ```bash
    astro deployment create --deployment-file <deployment-template-file-name>
    ```
3. Optional. Confirm that your Deployment was successfuly created by running the following command in your current Workspace:

   ```bash
   astro deployment list
   ```
   
   You can also go to the Workspace page in the Cloud UI.

## Update a Deployment using a Deployment file

:::danger 

You must push a complete Deployment file that lists all valid configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but additionally contains your Deployment's name, description, and metadata. In the same way you use a template file to create a new Deployment, you use a Deployment file to update an existing Deployment with a new set of configurations.

You can create a Deployment file by inspecting a Deployment file and not specifying the `--template-file` flag on the command. After you create a Deployment file, you can modify most Deployment configurations.

When you update a Deployment with a Deployment file, keep in mind that:

- You can’t change the cluster or Workspace the Deployment runs on. To transfer a Deployment to a different Workspace, see [Transfer a Deployment](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).
- You can't change the Astro Runtime version of the Deployment. To upgrade Astro Runtime, you must update the Dockerfile in your Astro project. See [Upgrade Astro Runtime](upgrade-runtime.md).
- Worker queues and environment variables are updated to match the corresponding sections in the Deployment file. Any existing worker queues or environemnt variables that are specified in the Cloud UI but not in the Deployment file are deleted.

To update a Deployment using a Deployment file:

1. Inspect an existing Deployment and create a Deployment file for its current configurations:

  ```sh
  astro deployment inspect -n <deployment-name> <your-deployment-file-name>
  ```

2. Modify the Deployment file and save your changes. You can modify any value in the `environment_variables` and `worker_queues` sections, and most values in the `configuration` section.

3. Update your Deployment according to the configurations in the Deployment file:

  ```sh
  astro deployment update -d <deployment-name> --deployment-file <your-deployment-file>
  ```

4. Optional. Confirm that your Deployment was updated successfully by running the following command. You can also go to the Deployment page in the Cloud UI to confirm the new values.

  ```sh
  astro deployment inspect -n <deployment-name>
  ```
  
## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [CI/CD](ci-cd.md)
