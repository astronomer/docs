---
sidebar_label: "Configure Deployments with Deployment files"
title: "Configure Deployments programmatically using Deployment files"
id: deployments-as-code
description: "Manage an Astro Deployment using a Deployment file in YAML or JSON format"
---

You can configure Deployments using Deployment files and Deployment template files. Deployment files are used to update the same Deployment programmatically, and Deployment template files are used to create or update multiple Deployments based on a single template.

Use this document to learn how to create and manage Deployment files and Deployment template files. See [Deployment file reference](deployment-file-referenece.md) for a list of all configurable Deployment file values. 

## Create a Deployment template file

After you create an Astro Deployment, you can create a _Deployment template file_ using the Astro CLI that contains its unique configurations represented as code. This includes details such as worker queues, environment variables, and Astro Runtime version, but does not include the Deployment's unique metadata.

You can use Deployment template files to manage Deployments programmatically on Astro. The following examples are some ways you can use Deployment files to manage Deployments as code:

- Create a template file in a central GitHub repository and use it as a source of truth for new Deployments that fit a particular use case. For example, you can standardize your team's development environments by creating a template file with configurations for that type of Deployment.
- Store a Deployment template file that represents the configurations of an existing Deployment. You can make changes to this file to update a Deployment faster and more easily than doing so with the Cloud UI or individual Astro CLI commands.
- Use a template file from an existing Deployment to create another Deployment with the same configurations. This is an alternative to creating a new Deployment in the Cloud UI and manually copying configurations.

To create a YAML template file based on an existing Deployment, run the following command:

```bash
astro deployment inspect <deployment-name> --template > <your-deployment-template-file-name>.yaml
```

To create a JSON template file based on an existing Deployment, run the following command:

```bash
astro deployment inspect <deployment-name> --template --output json > <your-deployment-template-file-name>.json
```

Alternatively, you can manually create a template file without using an existing Deployment. See [Deployment file reference](deployment-file-referenece.md) for a list of all configurable Deployment template file values. 

## Create a Deployment from a template file

Before you create a Deployment from a template file, keep the following in mind:

- The `name` field must include a unique name for the Deployment in the Workspace. 

- The `name` field is the only required field in a Deployment template file for Astro Hosted. You must also specify the `cluster_name` field on Astro Hybrid. The Astro CLI will use default values for any other unspecified fields. These default values are the same default values when you create a Deployment in the Cloud UI.

- When you create worker queues, each worker queue must include a `name` and `worker_type`. The Astro CLI will use default values for any other unspecified fields.

- When you create environment variables, each variable must include a `key` and a `value`.

To create a new Deployment from an existing template file:

1. In your template file, provide a name for the new Deployment.
2. Run the following command to create the Deployment:

    ```bash
    astro deployment create --deployment-file <deployment-template-file-name>
    ```

3. (Optional) Either open the Cloud UI or run the following command to confirm that your Deployment was successfully created:

   ```bash
   astro deployment list
   ```
   
4. (Optional) Reconfigure any Airflow connections or variables from the Deployment that you copied into the template file. Airflow connections and variables cannot be configured using template files. See [Manage connections in Airflow](manage-connections-variables.md).

## Update a Deployment using a Deployment file

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but also contains your Deployment's name, description, and metadata. In the same way you use a template file to create a new Deployment, you use a Deployment file to update an existing Deployment with a new set of configurations.

You can create a Deployment file by running the following command:

```bash
astro deployment inspect <deployment-name> --template > <your-deployment-template-file-name>.yaml
```

When you update a Deployment with a Deployment file, keep the following in mind:

- You can’t change the cluster or Workspace the Deployment runs on. To transfer a Deployment to a different Workspace, see [Transfer a Deployment](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).
- You can't change the Astro Runtime version of the Deployment. To upgrade Astro Runtime, you must update the Dockerfile in your Astro project. See [Upgrade Astro Runtime](upgrade-runtime.md).
- Environment variables marked as secret in the Cloud UI are not exported to your Deployment file. Hence, these will be deleted from your Deployment if you do not add them to your deployment file. See [`deployment.environment_variables`](#deploymentenvironment_variables) for more details.

:::warning 

You must push a complete Deployment file that lists all valid configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

To update a Deployment using a Deployment file:

1. Inspect an existing Deployment and create a Deployment file for its current configurations:

  ```bash
  astro deployment inspect -n <deployment-name> > <your-deployment-file-name>
  ```

2. Modify the Deployment file and save your changes. See [Deployment file reference](deployment-file-reference.md) for fields that you can modify.

  <!-- You can modify any value in the `environment_variables` and `worker_queues` sections, and most values in the `configuration` section. -->

3. Update your Deployment according to the configurations in the Deployment file:

  ```bash
  astro deployment update <deployment-name> --deployment-file <your-deployment-file>
  ```

4. (Optional) Confirm that your Deployment was updated successfully by running the following command. You can also go to the Deployment page in the Cloud UI to confirm the new values.

  ```bash
  astro deployment inspect -n <deployment-name>
  ```

## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [Choose a CI/CD Strategy for deploying code to Astro](set-up-ci-cd.md)