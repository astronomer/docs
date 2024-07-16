---
title: 'Terraform examples'
sidebar_label: 'Example uses'
id: terraform-provider-examples
description: Explore examples of common Terraform actions or configurations.
---

:::publicpreview
:::

After you finish your first [Terraform](https://www.terraform.io/) initialization, you can begin using Terraform scripts to automate, templatize, or programmatically manage your Astro environments.

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) version 1.0 or higher
- Astro Workspace Owner [user permissions](user-permissions.md)
- Organization ID

## Example: Import existing resources

By adding both an `import` command and defining the configuration to your Terraform file, you can import existing Astro resources, such as Deployments or Workspaces, for Terraform to manage. After you successfully import import them, Terraform fully manages your resources and you can update or delete them by updating the Terraform configuration file.

:::tip

Your Terraform file takes the highest priority in defining your Astro resource configuration. This means that when you import resources using Terraform, you need to specify all required fields if your Terraform file is different from any resource configurations that you configured through the Terraform CLI, Astro CLI, Astro API, or Astro UI. If the resources defined in your Terraform file and your actual resources are different, Terraform overrides your resource settings to match the configurations of the resources in your Terraform file.

:::

<details>
<summary><strong> Import existing Deployment as a resource example</strong></summary>

In a Terraform file, add the following configuration.

```
// Import the new configuration to an existing Deployment. After you use `terraform apply` to apply this new configuration once, you can remove this section of code from your Terraform file.
import {
  id = "<your-deployment-ID>" // ID of the existing deployment
  to = astro_deployment.imported_deployment
}
// The new resource configuration.
resource "astro_deployment" "imported_deployment" {
  name                    = "import me"
  description             = "an existing deployment"
  type                    = "DEDICATED"
  cluster_id              = "<your-cluster-ID>"
  contact_emails          = ["preview@astronomer.test"]
  default_task_pod_cpu    = "0.25"
  default_task_pod_memory = "0.5Gi"
  executor                = "KUBERNETES"
  is_cicd_enforced        = true
  is_dag_deploy_enabled   = true
  is_development_mode     = false
  is_high_availability    = true
  resource_quota_cpu      = "10"
  resource_quota_memory   = "20Gi"
  scheduler_size          = "SMALL"
  workspace_id            = "<your-workspace-ID>"
  environment_variables   = []
}
```

</details>

## Example: Define variables with Terraform

You can define variables in a separate file and then call it from within other Terraform commands.

<details>
<summary><strong>Define variables in Terraform code example</strong></summary>

In a Terraform `variables.tf` file, you can define your variables:
```

variable "teams" {
  type = map(object({
    name = string
    default_worker_queue_size = string
    contact_emails = list(string)
  }))
  default = {
    finance = {
      name = "finance"
      default_worker_queue_size = "A5"
      contact_emails = ["foo@bar.com", "john@doe.com"]
    }
    ads = {
      name = "ads"
      default_worker_queue_size = "A10"
      contact_emails = ["foo@bar.com", "john@doe.com"]
    }
    ml = {
      name = "ml"
      default_worker_queue_size = "A40"
      contact_emails = ["foo@bar.com", "john@doe.com"]
    }
  }
}

```

Then, in your Terraform configuration file, `main.tf`, you can refer to those variables to create resources:

```
resource "astro_workspace" "team_workspaces" {
  for_each = var.teams

  name                  = "${each.value.name} Workspace"
  description           = "${each.value.name} Workspace"
  cicd_enforced_default = true
}
```

</details>

## Example: Create a Workspace per Team

You can use Terraform to script creating a Workspace for multiple Teams. The following example shows how to create a Workspace, a Cluster, and three Deployments for that Team. You can use the full code example in the [Astro Terraform Provider's GitHub](https://github.com/astronomer/terraform-provider-astro/blob/main/examples/scenarios/workspace_per_team.tf) to create multiple teams following the same pattern.

<details>
<summary><strong>Terraform Workspaces and Teams code example</strong></summary>

Before using the code example, be sure to add your Astro Organization ID for the `organization_id` parameter.

```
/* Workspace Per Team

Team 1 Workspace
- Dev Deployment
- Stage Deployment
- Prod Deployment

*/

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

resource "astro_workspace" "team_1_workspace" {
  name                  = "Team 1 Workspace"
  description           = "Team 1 Workspace"
  cicd_enforced_default = true
}

resource "astro_cluster" "team_1_cluster" {
  type             = "DEDICATED"
  name             = "Team 1 AWS Cluster"
  region           = "us-east-1"
  cloud_provider   = "AWS"
  vpc_subnet_range = "172.20.0.0/20"
  workspace_ids    = []
  timeouts = {
    create = "3h"
    update = "2h"
    delete = "1h"
  }
}

resource "astro_deployment" "team_1_dev_deployment" {
  name                    = "Team 1 Dev Deployment"
  description             = "Team 1 Dev Deployment"
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
  workspace_id            = astro_workspace.team_1_workspace.id
  environment_variables   = []
  worker_queues = [{
    name               = "default"
    is_default         = true
    astro_machine      = "A5"
    max_worker_count   = 10
    min_worker_count   = 0
    worker_concurrency = 1
  }]
  scaling_spec = {
    hibernation_spec = {
      schedules = [{
        is_enabled        = true
        hibernate_at_cron = "20 * * * *"
        wake_at_cron      = "10 * * * *"
      }]
    }
  }
}

resource "astro_deployment" "team_1_stage_deployment" {
  name                    = "Team 1 Stage Deployment"
  description             = "Team 1 Stage Deployment"
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
  workspace_id            = astro_workspace.team_1_workspace.id
  environment_variables   = []
  worker_queues = [{
    name               = "default"
    is_default         = true
    astro_machine      = "A5"
    max_worker_count   = 10
    min_worker_count   = 0
    worker_concurrency = 1
  }]
  scaling_spec = {
    hibernation_spec = {
      schedules = [{
        is_enabled        = true
        hibernate_at_cron = "20 * * * *"
        wake_at_cron      = "10 * * * *"
      }]
    }
  }
}

resource "astro_deployment" "team_1_prod_deployment" {
  name                    = "Team 1 Prod Deployment"
  description             = "Team 1 Prod Deployment"
  type                    = "DEDICATED"
  cluster_id              = astro_cluster.team_1_cluster.id
  contact_emails          = ["preview@astronomer.test"]
  default_task_pod_cpu    = "0.25"
  default_task_pod_memory = "0.5Gi"
  executor                = "KUBERNETES"
  is_cicd_enforced        = true
  is_dag_deploy_enabled   = true
  is_development_mode     = false
  is_high_availability    = true
  resource_quota_cpu      = "10"
  resource_quota_memory   = "20Gi"
  scheduler_size          = "SMALL"
  workspace_id            = astro_workspace.team_1_workspace.id
  environment_variables = [{
    key       = "key1"
    value     = "value1"
    is_secret = false
  }]
}
```

</details>