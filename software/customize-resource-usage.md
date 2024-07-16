---
sidebar_label: 'Customize resource usage'
title: 'Customize Deployment CPU and management resources per component'
id: customize-resource-usage
description: Scale Deployments directly using non-proportional CPU and memory specifications.
---

When you create a new Astronomer Deployment, you can specify the exact amount of CPU and memory that power its core components using the **Custom Resources** resource strategy.

Compared to using Astronomer Units (AU), which represent a fixed amount of CPU and memory, specifying custom resources gives you greater flexibility to define how your Deployments run. For example, you might need to allocate significantly more memory than CPU to your worker Pods if you need to run memory-intensive tasks, but at the same time you need more memory than CPU in your scheduler. In this scenario, using AUs isn't sufficient because each component needs a different CPU to memory ratio.

When a Deployment uses the **Custom Resources** resource strategy, Deployment Admins can specify the exact amount of CPU and memory they want each component to have without any scaling limitations. The resources you specify are used both as the limit and request values for the Pods running your components.

## Set custom resource usage in the Software UI

To switch from using AU to using custom resource specifications:

1. In the Software UI, open your Deployment.
2. In the **Settings** tab, change your **Resource Strategy** to **Custom Resources**.
3. For each Software component, adjust the CPU and memory sliders to match your resource requirements. You can change the unit of the resource by clicking the dropdown menu that shows your current unit.

:::info

To create a Deployment through the Houston API that uses the custom resource strategy be default, set `astroUnitsEnabled: false` in your [Deployment creation mutation](houston-api.md#create-or-update-a-deployment-with-configurations).

:::

## Disable Astronomer Units (AUs) from Deployment resource configurations

To limit users to only configure Deployments using custom resources, set the following configuration in your `values.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        resourceProvisioningStrategy:
          astroUnitsEnabled: false
```

Then, save this configuration and push it to your platform. See [Apply a Platform Config Change](apply-platform-config.md).
