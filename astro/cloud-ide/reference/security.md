---
sidebar_label: "Security & data governance"
title: Astro Cloud IDE security & data governance
id: security
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in Public Preview. This means that it is available to all Astro customers, but is still undergoing heavy development and features are subject to change. Using the Cloud IDE has no impact to your Deployments or pipelines running in production. If you have any feedback, please submit it to the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

## Security

The Cloud IDE is a fully managed service that runs in an Astronomer-managed private cluster. This means that all of the infrastructure is managed by Astronomer, and you don't have to worry about managing the underlying infrastructure. Infrastructure is tightly scoped to organizations, so your code and data will never be exposed to other organizations.

## Data governance

The Cloud IDE stores Python cell outputs in an encrypted S3 bucket. SQL cell outputs are stored in the corresponding connection database under the schema you configure.

If you would like to provide your own S3 bucket for storing Python cell outputs, please reach out to the Astronomer team.

## Execution

When a user executes a cell, the request is sent through the Astronomer control plane to a dedicated, isolated Kubernetes pod running the Cloud IDE. The request is then either executed on the worker pod (in the case of Python) or sent to the appropriate database (in the case of SQL). The response is then sent back through the control plane to the user.

The worker pods are isolated from each other and from the control plane. Only requests from your organization may be sent to the same pods. No code or data is ever persisted on the worker pods.
