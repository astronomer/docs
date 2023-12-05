---
sidebar_label: 'Apply a config change'
title: 'Apply a Software platform configuration change'
id: apply-platform-config
description: Apply platform-wide configuration changes to Astronomer via Helm.
---

Astronomer Software uses [Helm](https://helm.sh/) to manage platform-level settings that apply to all users and Deployments. The [Astronomer Helm chart](https://github.com/astronomer/astronomer/blob/master/values.yaml) includes configurations for areas such as:

- [Identity provider integrations](integrate-auth-system.md)
- [Registry backends](registry-backend.md)
- [Resource allocation limits](configure-platform-resources.md)

All Astronomer Software platform customizations require setting key-value pairs in a file named `config.yaml` and applying the file to your cluster. `config.yaml` contains settings for both the Astronomer Helm chart, as well Helm charts for system components like [ElasticSearch](https://github.com/astronomer/astronomer/blob/master/charts/elasticsearch/values.yaml) and [nginx](https://github.com/astronomer/astronomer/blob/master/charts/nginx/values.yaml). Using Helm allows you to keep all of your configurations in a single file that you can version and store securely. Use this document to learn how to retrieve your existing Helm configuration, modify configurations, and apply your changes to your Astronomer Software cluster.

## Step 1: Retrieve your current cluster configuration

The best way to add or modify configurations is to start with your existing `config.yaml` file. To retrieve the current `config.yaml` file of an existing Software cluster, run the following command:

```sh
helm get values <your-installation-release-name> -n <your-installation-namespace> > config.yaml
```

:::caution

When you retrieve your file this way, delete `USER-SUPPLIED VALUES:` from the first line before changing any other configurations.

:::

Alternatively, your team might use version management to store your existing Helm configuration. In this case, retrieve, update, and store your configuration file according to your team's workflows.

## Step 2: Update key-value pairs for your configurations

<!--- Version-specific -->

1. Create a copy of your `config.yaml` file so that you can compare your existing configuration to your new configuration. 
2. In your copied file, update the key-value pairs for the settings you want to change. To update a setting you haven't already specified, copy the corresponding key-value pair from the relevant [default Helm chart](https://github.com/astronomer/astronomer/tree/master/charts) into your `config.yaml` file and modify the value from there.

When you have finished updating the key-value pairs, ensure that they have the same relative order and indentation as they do in the [default configuration file](https://github.com/astronomer/astronomer/blob/master/values.yaml). If they don't, your changes might not be properly applied. The name of the Helm charts you're modifying should be the first keys in the file, such as in the following example:
 
```yaml
global:
  <your-global-configuration>

astronomer:
  <your-astronomer-configuration>

alertmanager:
  <your-alertmanager-configuration>

nginx:
  <your-nginx-configuration>
```

:::info 

A number of key-value pairs, including configurations for user permissions and identity providers, must be set in the `astronomer.houston.config` section of the Astronomer Helm chart. The default values for `houston.config` key-value pairs are not available for reference in the Astronomer Helm repo. To view the default configurations for this section, see the [Astronomer documentation repository](https://github.com/astronomer/docs/blob/main/software_configs/0.33/default.yaml).

:::

## Step 3: Push changes to your Astronomer Software cluster

1. Copy your platform namespace and release name. These are both likely to be `astronomer`. Your platform release name can be found in your list of active namespaces, which you can view by running the following command:

    ```zsh
    kubectl get ns
    ```

    To locate your platform release name, run:

    ```zsh
    helm ls -n <your-platform-namespace>
    ```

2. Save your updated `config.yaml` file and run the following command to apply it as a Helm upgrade:

    ```zsh
    helm upgrade <your-platform-release-name> astronomer/astronomer -f <your-updated-config-yaml-file> -n <your-platform-namespace> --set astronomer.houston.upgradeDeployments.enabled=false
    ```

    Setting `astronomer.houston.upgradeDeployments.enabled=false` ensures that no Airflow components in Deployments are restarted during your upgrade.

3. Run the following command to confirm that your configuration was applied:

    ```zsh
    helm get values <your-platform-release-name> -n <your-platform-namespace>
    ```
