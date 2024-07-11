---
title: 'Terraform examples'
sidebar_label: 'Example uses'
id: terraform-provider-examples
description: Explore examples of common Terraform actions or configurations.
---

After you finish your first Terraform initialization, you can begin using Terraform scripts to automate, templatize, or programmatically manage your Astro environments.

## Prerequisites

- [Go](https://go.dev/doc/install) version 1.21 or higher
- [Terraform](https://developer.hashicorp.com/terraform/install) version 1.0 or higher
- Astro Organization Owner [user permissions](user-permissions.md)
- Organization ID


## Example: Create a Workspace per Team

You can use Terraform to script creating a Workspace for multiple Teams. The following example shows how to create a Workspace, Team within that Workspace, and three Deployments for that Team. You can use the full code example in the [Astro Terraform Provider's GitHub](https://github.com/astronomer/terraform-provider-astro/blob/main/examples/scenarios/workspace_per_team.tf) to create multiple teams, following the same pattern.

<details>
<summary><strong>Terraform code example</strong></summary>

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