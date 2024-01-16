---
title: "Overprovision Deployments on Astronomer Software"
sidebar_label: "Overprovision Deployments"
id: cluster-resource-provisioning
description: Configure your Astronomer cluster to overprovision Deployments.
---

:::danger Development workloads only

Changing cluster resource provisioning is only recommended for development clusters and can result in task failures. Astronomer can't provide support or troubleshoot issues related to overprovisioning Deployments through this configuration.

:::

By default, Deployments specify CPU and memory [requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for Kubernetes in terms of Astronomer Units (AU). For example, if an Airflow scheduler uses 1AU, it has both a request and a limit of 0.1 CPU and 385 MB of memory on its given Kubernetes node. Because you can't normally have a request lower than a limit, some Airflow components might reserve more resources on a node than they actually require.

To change this behavior, you can change the amount of CPU and memory that an AU requests, allowing you to more efficiently provision resources based on the requirements for your Deployments. This is known as overprovisioning, because it allows more Airflow component instances to exist on a single Kubernetes node.

1. Add the following configuration to your `config.yaml` file. Replace the values for `overProvisioningFactorMem` and `overProvisioningFactorCPU` with the factor by which you want to set your resource requests as a percentage of your resource limits.

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
            # This is a multiplying factor as a percentage of the limits. Defaults to 1
            overProvisioningFactorMem: 1
            overProvisioningFactorCPU: 1

            ## (Optional) Remove components that the overprovisioning factor should not apply to
            overProvisioningComponents:

              - scheduler
              - webserver
              - workers
              - triggerer
              - flower
              - pgbouncer
              - statsd
              - triggerer-log-groomer
    ```

    For example, if you set `overProvisioningFactorMem: 0.75` and `overProvisioningFactorCPU: 0.5`, a scheduler using 1 AU will only request 0.075 CPU and 192.5 MB of memory on a node, allowing you to run more components on that node than before.

    By default, this configuration applies to all Airflow components. Any components that you remove from `overProvisioningComponents` will not have overprovisioning applied.

2. Save the `config.yaml` file and push the configuration change to your platform. See [Apply a config change](apply-platform-config.md). After the change is applied, new Deployments automatically use the updated AU definition.
3. Redeploy code to your existing Deployments to have them start using your updated AU definition. See [Deploy code](deploy-cli.md).
