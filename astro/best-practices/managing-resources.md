---
title: 'Managing resources on Astro'
sidebar_label: 'Managing resources'
id: managing-resources
---

Astro supports a number of approaches to managing [Deployment resources](https://www.astronomer.io/docs/astro/deployment-settings#deployment-resources).

## Managing resources manually

Astro recommends the Astro UI for managing resources if you do not yet need to deploy or modify projects programmatically. Chances are, if you are on a small team getting started or you are an individual dev creating projects on an ad-hoc basis, the Astro UI will meet all your needs when it comes to managing resources. You will find all the options an individual or small team needs in order to get started, plus guidance that will help ensure that your instance is right-sized for your use case.

On the Astro UI, you can:

- Optimize Deployment processing.
- Optimize compute resources and cost.
- Enable use cases with intensive workloads.

For more details about configuring resources with the UI, see [Deployment resources](https://www.astronomer.io/docs/astro/deployment-resources).

:::info

If you prefer to use a command-line tool, you can use the Astro CLI to manage all the resources configurable with the UI.

For information about the commands and settings available in the Astro CLI, see [Command reference](https://www.astronomer.io/docs/astro/cli/reference).

:::

## Managing resources programmatically

Astro recommends the Terraform Provider or Astro API when you need to manage resources programmatically. Typically, teams manage Deployments as code as they start managing instances at scale. Benefits of managing Deployments as code include the ability to have your infrastructure configuration in your version control solution, which allows for tracking and rolling back changes as well as recreating resources easily if something goes wrong.

- [Terraform provider](https://www.astronomer.io/docs/astro/terraform-provider). Terraform is an industry-standard tool for managing infrastructure as code (IaC). With the provider, you can use Terraform to automate, templatize, or programmatically manage Astro environments. For example, you can automate creating Workspaces and Teams based on existing resources. Astro recommends this approach in general but especially for teams in organizations where Terraform is already in use.
- [Astro API](https://www.astronomer.io/docs/api). The API enables you to create and/or update resources such as Organizations, Deployments, Clusters, Deploys, and Workspaces. An Organization API token is required. You can download the OpenAPI spec for easy configuration of tools such as Postman and Swagger. Astro recommends the API for Python-centric use cases.

:::info

If you prefer to use Bash scripts to manage your infrastructure, you can use the Astro CLI as a wrapper on the API. You can use CLI commands to automate tasks such as creating and deleting Deployments, hibernating and waking Deployments, creating and updating Deployment pools, and creating and updating worker queues. Running of commands can be automated in CI/CD pipelines using API tokens. Requires Docker.

For an overview of the CLI, see [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).

:::
