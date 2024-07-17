---
title: 'Managing resources on Astro'
sidebar_label: 'Managing resources'
id: managing-resources
---

Astro supports a number of approaches to managing [Deployment resources](https://www.astronomer.io/docs/astro/deployment-settings#deployment-resources).

## Managing resources manually

Astro recommends the Astro UI for managing resources if you do not yet need to deploy or modify projects programmatically. Chances are, if you are on a small team getting started or you are an individual dev creating projects on an ad-hoc basis, the Astro UI will meet all your needs when it comes to managing resources. Along with all the options an individual or small team needs in order to get started, the UI displays guidance that will help ensure that your instance is right-sized for your use case.

On the Astro UI, you can:

- Optimize Deployment processing.
- Optimize compute resources and cost.
- Enable use cases with intensive workloads.

For more details about configuring resources with the UI, see [Deployment resources](https://www.astronomer.io/docs/astro/deployment-resources).

:::info

If you prefer to use a command-line tool, you can use the Astro CLI to manage all the resources configurable with the UI.

For information about all the commands and settings available in the Astro CLI, see [Command reference](https://www.astronomer.io/docs/astro/cli/reference).

:::

## Managing resources programmatically at scale

When managing resources at scale, you can choose between the Astro API, Astro CLI, and Terraform Provider. Astro recommends one of these options when you need to automate Deployment management .

Benefits of managing Deployments as code include the ability to track and rollback changes as well as recreate resources if something goes wrong.

- [Astro API](https://www.astronomer.io/docs/api). The API enables you to get and update Organizations, Deployments, Clusters, Deploys, and Workspaces. An Organization API token is required.
- [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview). The CLI uses the API to enable tasks such as creating and deleting Deployments, hibernating and waking Deployments, creating and updating Deployment pools, and creating and updating worker queues. Running of commands can be automated in CI/CD pipelines using API tokens. Requires Docker.
- [Terraform provider](https://www.astronomer.io/docs/astro/terraform-provider). You can use Terraform to automate, templatize, or programmatically manage Astro environments. For example, you can automate creating Workspaces and Teams based on existing Astro resources.
- - track changes with git
- - recreate resources if something goes wrong
