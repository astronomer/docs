---
title: 'Managing resources on Astro'
sidebar_label: 'Managing resources'
id: managing-resources
---

Astro supports a number of approaches to managing [Deployment resources](https://www.astronomer.io/docs/astro/deployment-settings#deployment-resources).

## Managing instances not requiring automation

The Astro UI is a no-code option supporting some configuration of resources. Astro recommends this option for less complex use cases that do not require automation.

On the Astro UI, you can:

- Optimize Deployment processing.
- Optimize compute resources and cost.
- Enable use cases with intensive workloads.

For more details about configuring resources with the UI, see []().

## Automating resource management at scale

Managing resources as code is possible using the Astro API, Astro CLI, and Terraform Provider. Astro recommends one of these options when you need to automate Deployment management at scale.

- [Astro API](https://www.astronomer.io/docs/api). The API enables you to get and update Organizations, Deployments, Clusters, Deploys, and Workspaces. Organization API token required.
- [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview). The CLI uses the API to enable tasks such as creating and deleting Deployments, hibernating and waking Deployments, creating and updating Deployment pools, and creating and updating worker queues. Running of commands can be automated in CI/CD pipelines using API tokens.
- [Terraform provider](https://www.astronomer.io/docs/astro/terraform-provider). You can use Terraform to automate, templatize, or programmatically manage Astro environments. For example, you can automate creating Workspaces and Teams based on existing Astro resources.
