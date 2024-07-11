---
title: 'Get started with Astro Terraform Provider'
sidebar_label: 'Get Started'
id: terraform-provider-get-started
description: Get started using the Astro Terraform Provider to work with your Astro implementations.
---

To use Terraform with Astro, you must set up authorize the Astro Terraform Provider to access and modify your Astro Organization resources. Then, you can programattically update your Astro Organization using Terraform files.

## Prerequisites

- [Go](https://go.dev/doc/install) version 1.21 or higher
- [Terraform](https://developer.hashicorp.com/terraform/install) version 1.0 or higher
- Astro Organization Owner [user permissions](user-permissions.md)

## Step 1: Create an API Token

You can use any of the following credentials to authenticate in an automated process, but an Organization API token is recommended:

- A Deployment API token. See [Deployment API tokens](deployment-api-tokens.md).
- A Workspace API token. See [Create a Workspace API token](workspace-api-tokens.md).
- An Organization API token. See [Create an Organization API token](organization-api-tokens.md).

When you create an API token for your environment, keep the following best practices in mind:

- Always give your API token the minimum permissions required to perform an action. This improves control and security over your Astro components. For example, instead of creating an Organization API token to automate actions across two  Workspaces, create a separate Workspace API token for each Workspace.

- Always set an expiration date for your API tokens.
- Always [rotate your API tokens](workspace-api-tokens.md#rotate-a-workspace-api-token) for enhanced security.

## Step 2 Apply the provider

1. Retrieve your **Organization ID** from the Astro UI by clicking on your **Organization Settings** in your **Organization Details** section.

2. Create a `main.tf` file with the following code. This code example declares the Astro provider as a requirement, and includes the Organization ID for your Astro resources. You can add your own custom terraform commands, or use one of the examples shared in the [Astro Terraform Provider Github Repo]

```
terraform {
  required_providers {
    astro = {
      source = "astronomer/astro"
    }
  }
}

provider "astro" {
  organization_id = "<you-astro-organization-id>"
}

# your terraform commands here

```

If you want to use an example Terraform file, the [`workspace_per_team.tf`](https://github.com/astronomer/terraform-provider-astro/blob/main/examples/scenarios/workspace_per_team.tf) example shows how to create three [Astro Teams](manage-teams.md) and development, staging, and production Deployments for each.

2. Using the API Token you made in Step 1, run the following commands to apply the provider to your Astro implementation.

```bash
export ASTRO_API_TOKEN=<your-api-token>
terraform init # only needed the first time - initializes a working directory and downloads the necessary provider plugins and modules and setting up the backend for storing your infrastructure's state
terraform plan # creates a plan that make your resources match your configuration
terraform apply # performs a plan, just like terraform plan does, and also carries out the planned changes to each resource by using the relevant infrastructure provider's API
```

Now that you've initialited a working directory and downloaded required provider plugins and modules, you can start updating your Astro Workspace or Organizations with Terraform.