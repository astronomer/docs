---
title: 'Get started with Astro Terraform Provider'
sidebar_label: 'Get Started'
id: terraform-provider-get-started
description: Get started using the Astro Terraform Provider to work with your Astro implementations.
---

:::publicpreview
:::

Terraform enables you to define and manage infrastructure as code. Using the [Astro Terraform Provider](https://registry.terraform.io/providers/astronomer/astro/latest), this guide demonstrates how to manage Astro infrastructure using Terraform, by creating and deleting a Workspace and Deployment.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) version 1.0 or higher
- Astro Workspace Owner [user permissions](user-permissions.md)

## Step 1: Create an API Token

To use [Terraform](https://www.terraform.io/) with Astro, you must authorize the [Astro Terraform Provider](https://registry.terraform.io/providers/astronomer/astro/latest) to access and modify your Astro resources using an API token. Then, you can programmatically update your Astro Organization using Terraform. You can use any of the following API tokens to authenticate. Astronomer recommends applying the principle of least privilege, which means only permitting the necessary actions and no more. Since the following code example creates a new workspace, you'll require an Organization API token with the Organization Owner role.

- An Organization API token. See [Create an Organization API token](organization-api-tokens.md).
- A Workspace API token. See [Create a Workspace API token](workspace-api-tokens.md).
- A Deployment API token. See [Deployment API tokens](deployment-api-tokens.md).

When you create an API token for your environment, keep the following best practices in mind:

- Always give your API token the minimum permissions required to perform an action. This improves control and security over your Astro components. For example, instead of creating an Organization API token to automate actions across two  Workspaces, create a separate Workspace API token for each Workspace.
- Always set an expiration date for your API tokens.
- Always [rotate your API tokens](workspace-api-tokens.md#rotate-a-workspace-api-token) for enhanced security.

## Step 2: Apply the provider

1. Retrieve your **Organization ID** from the Astro UI by clicking on your **Organization Settings** in your **Organization Details** section.

2. Create a `main.tf` file with the following code. This code example declares the Astro provider as a requirement and includes the Organization ID for your Astro resources. You can add your own custom Terraform code or use one of the example scenarios shared in the [Astro Terraform Provider GitHub Repo](https://github.com/astronomer/terraform-provider-astro/tree/main/examples/scenarios).

The following example sets up a new Workspace with a hosted Deployment.

```tcl
terraform {
  required_providers {
    astro = {
      source = "astronomer/astro"
    }
  }
}

provider "astro" {
  organization_id = "<your-astro-organization-id>"
}

# Create a Workspace
resource "astro_workspace" "my_workspace" {
  name                  = "My Terraform Workspace"
  description           = "Managed by Terraform"
  cicd_enforced_default = true
}

# Create a standard Hosted Deployment in that Workspace
resource "astro_deployment" "my_standard_deployment" {
  name                    = "My Terraform Deployment"
  description             = "Managed by Terraform"
  type                    = "STANDARD"
  cloud_provider          = "AWS"
  region                  = "us-east-1"
  contact_emails          = []
  default_task_pod_cpu    = "0.25"
  default_task_pod_memory = "0.5Gi"
  executor                = "CELERY"
  is_cicd_enforced        = true
  is_dag_deploy_enabled   = true
  is_development_mode     = true
  is_high_availability    = false
  resource_quota_cpu      = "10"
  resource_quota_memory   = "20Gi"
  scheduler_size          = "SMALL"
  workspace_id            = astro_workspace.my_workspace.id
  environment_variables   = []
  worker_queues = [{
    name               = "default"
    is_default         = true
    astro_machine      = "A5"
    max_worker_count   = 10
    min_worker_count   = 0
    worker_concurrency = 1
  }]
}
```

If you want to use a different example Terraform file, the [`workspace_per_team.tf`](https://github.com/astronomer/terraform-provider-astro/blob/main/examples/scenarios/workspace_per_team.tf) example shows how to create three [Astro Teams](manage-teams.md) and development, staging, and production Deployments for each.

3. Using the API Token you made in Step 1, run the following commands to apply the provider to your Astro implementation.

```bash
export ASTRO_API_TOKEN=<your-api-token>
terraform init # only needed the first time - initializes a working directory and downloads the necessary provider plugins and modules and sets up the backend for storing your infrastructure's state
terraform plan # creates a plan that make your resources match your configuration
terraform apply # performs a plan, just like Terraform plan does, and also carries out the planned changes to each resource by using the relevant infrastructure provider's API
```

After `terraform apply` completes, Terraform either prints that your configuration was successful or it prints error logging that includes information on how to resolve your problem.

4. (Optional) You can continue to import additional resources or experiment with Terraform using the [Terraform Provider docs](https://registry.terraform.io/providers/astronomer/astro/latest/docs). After you're done, to prevent any unexpected charges or activity in your account from working with your Terraform example, you can delete any resources you created on Astro by using the following code example:

```bash
terraform destroy
```

## Next Steps

You can continue to explore how to work with Terraform and Astro with the examples in the [Astro Terraform Provider GitHub](https://github.com/astronomer/terraform-provider-astro/tree/main/examples/scenarios) or [Terraform Provider Examples](terraform-provider-examples.md).
