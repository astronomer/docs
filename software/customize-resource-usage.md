---
sidebar_label: 'Customize resource usage'
title: 'Customize Deployment CPU and management resources per component'
id: customize-resource-usage
description: Scale Deployments directly using non-proportional CPU and memory specifications.
---

By default, all Astronomer Deployments use Astronomer Units (AU) to define a relative amount of CPU and memory that you can allocate to a Deployment, and components must use the same AU value for both CPU and memory.

You can change the amount of CPU and memory an AU represents, but there are some scenarios where you need to size Deployments differently and without restraints on how your CPU and memory scale together. For example, you might need to allocate significantly more memory than CPU to your worker Pods if you need to run memory-intensive tasks, but at the same time you need more memory than CPU in your scheduler. In this scenario, using AUs isn't sufficient because each component needs a different CPU to memory ratio.

For the greatest degree of flexibility, you can enable custom resource specifications for Deployments. When this feature is enabled, Deployment Admins can specify the exact amount of CPU and memory they want each component to have without any scaling limitations. The resources you specify are used both as the limit and request values for the Pods running your components.