---
sidebar_label: "Create and apply Deployment files"
title: "Manage Deployments programmatically using Deployment files"
id: manage-deployments-as-code
description: "Manage an Astro Deployment using a Deployment file in YAML or JSON format"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

You can configure Deployments programmatically using Deployment files and Deployment template files. _Deployment files_ are used to update the same Deployment programmatically, and _Deployment template files_ are used to create new Deployments based on a single template.

Managing Deployments with files is essential to automating Deployment management at scale.  For example, you can:

- Create a template file in a central GitHub repository and use it as a source of truth for new Deployments that fit a particular use case. For example, you can standardize your team's development Deployments by creating a template file with configurations for that type of Deployment.
- Create a Deployment file that represents the configurations of an existing Deployment and store it in your GitHub repository. You can make changes to this file to update a Deployment  using CI/CD, which maintains the history of your changes.

Use this document to learn how to create and manage Deployment files and Deployment template files. See the [Deployment file reference](deployment-file-reference.md) for a list of all configurable Deployment file values. When you're ready to programmatically run Deployment file workflows, see [Authenticate your workflow](automation-authentication.md).

## Create a template file or Deployment file

To create a template file based on an existing Deployment, run the following command:

```bash
astro deployment inspect <deployment-id> --template > <your-deployment-template-file-name>.yaml
```

To create a Deployment file based on an existing Deployment, run the following command:

```bash
astro deployment inspect <deployment-id> > <your-deployment-file-name>.yaml
```

Alternatively, you can manually create a template file without using an existing Deployment as explained in [Create a Deployment using a template file](#create-a-deployment-using-a-template-file).

## Create a Deployment using a template file

1. Copy one of the following templates to a local `yaml` file:

  <Tabs
      defaultValue="standard"
      groupId= "create-a-deployment-using-a-template-file"
      values={[
          {label: 'Standard cluster', value: 'standard'},
          {label: 'Dedicated cluster', value: 'dedicated'},
      ]}>

  <TabItem value="standard">

  ```bash
  deployment:
      configuration:
          name: <your-deployment-name>
          deployment_type: HOSTED_SHARED
          cloud_provider: aws
          description: <deployment-description>
          runtime_version: 9.1.0
          dag_deploy_enabled: true
          executor: CeleryExecutor
          cluster_name: us-east-1
          region: us-east-1
          workspace_name: <your-workspace-name>
          scheduler_size: small
  ```
  
  Note that for Deployments on a standard cluster, the `region` and `cluster-name` parameters must both contain the region name for the standard cluster. See [Available regions for your cloud provider](resource-reference-hosted.md#standard-cluster-configurations). 

  </TabItem>

  <TabItem value="dedicated">

  ```bash
  deployment:
      configuration:
          name: <your-deployment-name>
          deployment_type: HOSTED_DEDICATED
          cloud_provider: aws
          description: <deployment-description>
          runtime_version: 9.1.0
          dag_deploy_enabled: true
          executor: KubernetesExecutor
          cluster_name: <your-cluster-name>
          region: us-east-1
          workspace_name: <your-workspace-name>
          scheduler_size: small
  ```
  
  The `cluster_name` field must include the name of the dedicated cluster that exists in your Astro Organization.

  </TabItem>

  </Tabs>
  
    These are the minimum values required to create a Deployment using a template file. Any configurations not specified are set to default values. To add more configurations, see [Deployment file reference](deployment-file-reference.md).

2.  Adjust the template file values for the Deployment you want to create. When working with template files, keep the following in mind:

    - The `name` field must include a unique name within the Workspace. 

    - The `workspace_name` field must include a valid Workspace name that exists in your Astro Organization.
    
    - The possible values for `cloud_provider`, `executor`, and `scheduler_size` are the same possible values when you create a Deployment with [`astro deployment create`](cli/astro-deployment-create.md#options). 

    - See to [Airflow and Astro Runtime version parity](runtime-image-architecture.md#astro-runtime-and-apache-airflow-parity) to choose your Astro Runtime version.

  See [Deployment file reference](deployment-file-reference.md) for a list of all configurable Deployment template file values.
  

3. Run the following command to create the Deployment:

    ```bash
    astro deployment create --deployment-file <your-deployment-file-name>
    ```

4. (Optional) Either open the Cloud UI or run the following command to confirm that you successfully created your Deployment:

   ```bash
   astro deployment list
   ```
   
4. (Optional) Reconfigure any Airflow connections or variables from the Deployment that you copied into the template file. Airflow connections and variables cannot be configured using template files. See [Manage connections in Airflow](manage-connections-variables.md).

## Update a Deployment using a Deployment file

A Deployment file is a complete snapshot of an existing Deployment at the point you inspected it. It's similar to a template file, but also contains your Deployment's name, description, and metadata. In the same way you use a template file to create a new Deployment, you use a Deployment file to update an existing Deployment with a new set of configurations.

When you update a Deployment with a Deployment file, keep the following in mind:

- You can’t change the cluster or Workspace the Deployment runs on. To transfer a Deployment to a different Workspace, see [Transfer a Deployment](deployment-settings.md#transfer-a-deployment-to-another-workspace).
- You can't change the Astro Runtime version of the Deployment. To upgrade Astro Runtime, you must update the Dockerfile in your Astro project. See [Upgrade Astro Runtime](upgrade-runtime.md).
- Environment variables marked as secret in the Cloud UI will be exported with a blank `value` to your Deployment file. To redeploy using the Deployment file, you either need to provide the `value` again in the Deployment file or delete the object for the variable. Otherwise, `astro deployment create` will fail. See [`deployment.environment_variables`](#deploymentenvironment_variables) for more details.

:::warning 

When you update a Deployment with a Deployment file, you must push a complete Deployment file that lists all of your existing worker queues. If a worker queue exists on Astro but doesn't exist in your Deployment file, the worker queue is deleted when you push your Deployment file. 

:::

To update a Deployment using a Deployment file:

1. Inspect an existing Deployment and create a Deployment file for its current configurations:

  ```bash
  astro deployment inspect <deployment-id> > <your-deployment-file-name>.yaml
  ```

2. Modify the Deployment file and save your changes. See [Deployment file reference](deployment-file-reference.md) for fields that you can modify.

3. Update your Deployment according to the configurations in the Deployment file:

  ```bash
  astro deployment update <deployment-id> --deployment-file <your-deployment-file>
  ```

4. (Optional) Confirm that your Deployment was updated successfully by running the following command. You can also go to the Deployment page in the Cloud UI to confirm the new values.

  ```bash
  astro deployment inspect <deployment-id>
  ```

## See also

- [Manage Deployment API keys](api-keys.md)
- [Deploy Code](deploy-code.md)
- [Choose a CI/CD Strategy for deploying code to Astro](set-up-ci-cd.md)