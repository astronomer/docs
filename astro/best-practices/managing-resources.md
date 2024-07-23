---
title: 'Managing resources on Astro'
sidebar_label: 'Managing resources'
id: managing-resources
---

Astro supports several approaches to managing [Deployment resources](https://www.astronomer.io/docs/astro/deployment-settings#deployment-resources), so you can provision the resources you need whether you are just starting or you are deploying projects programmatically at scale.

## Managing resources manually

Astronomer recommends the Astro UI for managing resources if you do not need to deploy or modify project config programmatically. If you are on a small team getting started or you are an individual dev creating projects on an ad hoc basis, the Astro UI will likely meet your needs when managing resources. In addition to all the options you need in order to create and customize resources, you will get guidance that will help ensure that your instance is right-sized for your use case.

On the Astro UI, you can:

- Optimize Deployment processing.
- Optimize compute resources and cost.
- Enable use cases with intensive workloads.

For more details about configuring resources with the UI, see [Deployment resources](https://www.astronomer.io/docs/astro/deployment-resources).

:::info

If you prefer to use a command-line tool, you can use the Astro CLI to manage all the resources configurable with the UI.

For the commands and settings available in the Astro CLI, see [Command reference](https://www.astronomer.io/docs/astro/cli/reference).

:::

## Managing resources programmatically

Astronomer recommends the Terraform Provider, Astro API, or Deployment files when you need to manage resources programmatically. Typically, teams manage resources as code as they start managing instances at scale. Benefits of managing resources as code include the ability to have your infrastructure configuration in your version control solution, which allows for tracking and rolling back changes as well as recreating resources easily if something goes wrong. Also, you can create and modify large numbers of Deployments quickly, making it easy to onboard new teams, reallocate resources, reassign Deployments, and more. 

- [Terraform provider](https://www.astronomer.io/docs/astro/terraform-provider). Terraform is an industry-standard tool for managing infrastructure as code (IaC). With the provider, you can use Terraform to automate, templatize, or programmatically manage Astro environments. For example, you can automate creating Workspaces and Teams based on existing resources. Astro recommends this approach in general but especially for teams in organizations where Terraform is already in use.
- [Astro API](https://www.astronomer.io/docs/api). The API enables you to create or update resources such as Organizations, Deployments, Clusters, Deploys, and Workspaces. An Organization API token is required. You can [download the OpenAPI spec](https://www.astronomer.io/docs/api#download-openapi-specifications) for easy configuration of tools such as Postman and Swagger. Astronomer recommends the API for Python-centric use cases.
- [Deployment files](https://www.astronomer.io/docs/astro/manage-deployments-as-code). You can configure Deployments programmatically using Deployment files, which you can generate automatically from existing Deployments. You can standardize Deployment configuration for specific use cases using Deployment template files, which you can also generate automatically from existing Deployments.

:::info

If you prefer to use Bash scripts to manage your infrastructure, you can use the Astro CLI as a wrapper on the API. You can use CLI commands to automate tasks such as creating and deleting Deployments, hibernating and waking Deployments, creating and updating Deployment pools, and creating and updating worker queues. You can also automate command execution in CI/CD pipelines using API tokens. Note: the Astro CLI requires Docker.

For an overview of the CLI, see [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).

:::
