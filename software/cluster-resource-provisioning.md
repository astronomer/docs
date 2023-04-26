---
title: "Change how Astronomer Software provisions resources"
sidebar_label: "Cluster resource provisioning"
id: cluster-resource-provisioning
description: Configure your Astronomer cluster to over- or underprovision Deployment resources.
---

:::danger Development workloads only

Changing cluster resource provisioning is only recommended for development clusters and can result in task failures. Astronomer can't provide support or troubleshoot issues related to  over- or underprovisioning Deployments through this configuration.

:::

By default, Deployments can request CPU and memory for Airflow components in terms Astronomer Units (AU). One AU is equivalent to 0.1 CPU and 385 MB of memory. You can only request whole numbers of AUs, which can sometimes result in you over- or underprovisioning your Deployments.

To change this behavior, you can change the amount of CPU and memory that an AU represents, allowing you to more accurately provision resources based on the requirements for your Deployments. 

1. Add the following configuration to your `config.yaml` file. Replace the values for `overProvisioningFactorMem` and `overProvisioningFactorCPU` with the factor by which you want to increase or decrease the amount of CPU and memory in an AU.

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
            # This is a multiplying factor as a percentage of the limits. Defaults to 1
            overProvisioningFactorMem: 1
            overProvisioningFactorCPU: 1
    ```

    For example, if you set `overProvisioningFactorMem: 0.75` and `overProvisioningFactorCPU: 0.5`, an AU will be equivalent to 0.075 CPU and 192.5 MB of memory.

2. Save the `config.yaml` file and push the configuration change to your platform. See [Apply a config change](apply-platform-config.md). After the change is applied, new Deployments automatically use the updated AU definition.
3. Redeploy code to your existing Deployments to have them start using your updated AU definition. See [Deploy code](deploy-cli.md).
