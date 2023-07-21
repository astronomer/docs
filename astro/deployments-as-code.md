---
sidebar_label: "Using Deployment file"
title: "Using Deployment file to manage Deployments"
id: deployments-as-code
description: "Manage an Astro Deployment using a Deployment file in YAML or JSON format"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


After you create an Astro Deployment, you can create a file using Astro CLI that contains its unique configurations represented as code. This includes worker queues, environment variables, Astro Runtime version, etc. See [Deployment file reference](./deployment-file-reference.md) for details on all sections of a deployment file.

You can use Deployment files to manage Deployments programmatically on Astro.

Specifically, you can:

- Create a template file in a central GitHub repository and use it as a source of truth for new Deployments that fit a particular use case. For example, you can standardize your team's development environments by creating a template file with configurations for that type of Deployment.
- Store a Deployment file that represents the configurations of an existing Deployment. You can make changes to this file to update a Deployment faster and more easily than doing so with the Cloud UI or individual Astro CLI commands.
- Use a template file from an existing Deployment to create another Deployment with the same configurations. This is an alternative to creating a new Deployment in the Cloud UI and manually copying configurations.

Astro supports updating a Deployment programmatically using [API keys or tokens](./automation-authentication.md). 

## Generate a Deployment template file

You can use Astro CLI's [`astro deployment inspect`](/cli/astro-deployment-inspect.md) command to create a Deployment file for an existing Deployment. A deployment file is created in `yaml` or `json` format and includes all information about a Deployment. 

A Deployment template file is a special type of Deployment file which does not have the `metadata` section, and the `name` and `description` fields are replaced with placeholder values (`""`). You can then use this template file to automate the creation of new Deployments in your CI/CD process. 

To create a template file in `yaml` format, run the following command:

```bash

astro deployment inspect <deployment-name> --template > <your-deployment-template-file-name>.yaml

```

To create a template file in `json` format, run the following command:

```bash

astro deployment inspect <deployment-name> --template --output json > <your-deployment-template-file-name>.json

```


## Create a Deployment from a template file

You can use Astro CLI's [`astro deployment create`](cli/astro-deployment-create.md) command to create a Deployment by using an existing Deployment template file as reference. Before you do, keep the following in mind:

- Deployment names must be unique within a single Workspace. Make sure that you replace the `name` field in the file with the desired name of your new Deployment.

- Only `name` field needs to be populated in the template file to create a Deployment. Rest all fields will have the values populated based on the existing Deployment. You can also update or omit the remaining fields as required based on the [deployment file reference](./deployment-file-reference.md). The CLI will create the Deployment using default values for each unspecified configuration. These default values are the same default values that are used when you create a Deployment from the Cloud UI.

:::tip Additional fields for Astro Hybrid

To create a Deployment on Astro Hybrid, both `name` and `cluster_name` fields are required.

:::

- When you create worker queues, the `name` and `worker_type` fields are required. Any unspecified fields are populated with smart defaults based on the worker types available in your cluster.

- When you create environment variables, each variable must include a `key` and a `value`.


To create a new Deployment from an existing template file:

1. In your template file, provide a name for the new Deployment.
2. Run:

    ```bash

    astro deployment create --deployment-file <deployment-template-file-name>

    ```

3. (Optional) Confirm that your Deployment was successfully created by running the following command in your current Workspace:

   ```bash

   astro deployment list

   ```
   
   You can also go to the Workspace page in the Cloud UI.

4. (Optional) Reconfigure any Airflow connections or variables from the Deployment that you copied into the template file. Airflow connections and variables cannot be configured using template files. See [Manage connections in Airflow](https://docs.astronomer.io/learn/connections).


## Update a Deployment using a Deployment file

:::warning 

You must push a complete Deployment file that lists all valid configurations whenever you update a Deployment with a Deployment file. If a configuration exists on Astro but doesn't exist in your Deployment file, such as a worker queue, that configuration is deleted when you push your Deployment file. 

:::

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but also contains your Deployment's name, description, and metadata. In the same way you use a template file to create a new Deployment, you use a Deployment file to update an existing Deployment with a new set of configurations.

You can create a Deployment file by running the following command:

```bash

astro deployment inspect <deployment-name> --template > <your-deployment-template-file-name>.yaml

```

When you update a Deployment with a Deployment file, keep in mind that:

- You can’t change the cluster or Workspace the Deployment runs on. To transfer a Deployment to a different Workspace, see [Transfer a Deployment](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).
- You can't change the Astro Runtime version of the Deployment. To upgrade Astro Runtime, you must update the Dockerfile in your Astro project. See [Upgrade Astro Runtime](upgrade-runtime.md).
- Environment variables marked as secret in the Cloud UI are not exported to your Deployment file. Hence, these will be deleted from your Deployment if you do not add them to your deployment file. See [`deployment.environment_variables`](#deploymentenvironment_variables) for more details.

To update a Deployment using a Deployment file:

1. Inspect an existing Deployment and create a Deployment file for its current configurations:

  ```bash
  
  astro deployment inspect -n <deployment-name> > <your-deployment-file-name>

  ```

2. Modify the Deployment file and save your changes. See [Deployment file reference](#deployment-file-reference) for fields that you can modify.

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