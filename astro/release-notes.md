---
sidebar_label: 'Astro'
title: 'Astro release notes'
id: release-notes
---

import HostedBadge from '@site/src/components/HostedBadge';
import HybridBadge from '@site/src/components/HybridBadge';


<head>
  <meta name="description" content="This is where you’ll find information about the latest Astro features and bug fixes. Check in regularly to know when issues are resolved and new features are added." />
  <meta name="og:description" content="This is where you’ll find information about the latest Astro features and bug fixes. Check in regularly to know when issues are resolved and new features are added." />
</head>

<p class="rssButton">
  <a href="/astro-release-notes.xml" target="_blank">
    <img src="/img/pic_rss.gif" width="36" height="14" alt="Subscribe to RSS Feed" />
  </a>
</p>

Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro.

**Latest Astro Runtime Version**: 9.0 ([Release notes](runtime-release-notes.md))

**Latest CLI Version**: 1.19.1 ([Release notes](cli/release-notes.md))

<!-- ALL LINKS TO INTERNAL DOCS MUST BE COMPLETE URLS INCLUDING HTTPS. Otherwise the links will break in RSS. -->

## August 29, 2023

### Changes to Workspace user roles

:::info Upgrade the Astro CLI

To take advantage of these new user roles programmatically, you must [upgrade the Astro CLI](https://docs.astronomer.io/astro/cli/install-cli#upgrade-the-cli) to version 1.19 or later.

:::

To increase granularity and better serve each user persona on Astro, Workspace roles have been updated with new names and permissions:

- The **Workspace Author** role is a new role for users who primarily write and deploy DAGs. Users with this role can push code changes, but they can't update Deployment or Airflow settings such as Airflow variables, Astro environment variables, or connections.
- The Workspace Admin role has been renamed to **Workspace Owner**. Users with this role are responsible for administrating membership to the Workspace. 
- The Workspace Editor role has been renamed to **Workspace Operator**. In addition to pushing code changes, Workspace Editors can now also edit Airflow objects such as variables, connections, and XComs. Users with this role are responsible for managing the environments that DAGs run in.
- The Workspace Viewer role has been renamed to **Workspace Member**. Users with this role only need viewing permissions for a Deployment and don't have permissions to make any code or configuration changes.

For more information about these role changes, see [User permissions reference](https://docs.astronomer.io/astro/user-permissions#workspace-roles) and [Enhanced Astro Workspace Roles for more granular permissions](https://www.astronomer.io/blog/introducing-updated-astro-workspace-roles-for-more-granular-permissions/)

### Additional improvements

- The lifespan of the personal user access token you can retrieve from `cloud.astronomer.io/token` has been reduced from 24 hours to 1 hour.

## August 21, 2023

### Additional improvements

- You can now configure [task log forwarding to Datadog](https://docs.astronomer.io/astro/view-logs#export-task-logs-to-datadog-aws-only) at the Deployment level.
- In the **DAGs** view of the Cloud UI, you can now double click a task run node in the graph view to view the task run's logs and mapped tasks.
- The A50 worker type has been renamed to A60 to make it consistent in scale with other worker types.
- The max possible **CPU quota** and **Memory quota** for a Deployment running in a Hosted dedicated cluster has increased to 1600 vCPU/ 3200 GiB respectively.

## August 15, 2023

### Additional improvements

- You can now see how many Astro alerts you've configured for a DAG in the **DAGs** page of the Cloud UI.

### Bug fixes

- Fixed an issue where you couldn't run Astro Cloud IDE pipelines that included a Markdown cell.
- Fixed an issue where an Organization's SSO bypass link was formatted incorrectly in the Cloud UI.

## August 8, 2023

### New Hosted worker type

<HostedBadge/>

You can now configure Deployments with the `A50` machine type, which has 12 vCPU and 24 GiB. See [Astro hosted resource reference](https://docs.astronomer.io/astro/resource-reference-hosted).

### Additional improvements

- When you create a new Astro Cloud IDE project, you can now specify whether you want the project to include an example pipeline.
- You can now access Organization-level settings in the Cloud UI only through the **Organization Settings** link. Additionally, some Organization settings have been moved to the top level of navigation so that there is no longer a **Settings** menu.
- You can now use commas, apostrophes, and ampersands in Workspace and Organization names.
- The Workspace list view in the Cloud UI has been redesigned so that Organization Owners can now edit and delete Workspaces directly from the list.

### Bug fixes

- Fixed an issue where the Cloud UI showed incorrect CPU and memory limits in bar charts on the Deployments list and **Details** page.

## August 1, 2023

### Hosted Deployments have DAG-only deploys enabled by default 

<HostedBadge/>

New Astro Hosted Deployments now have [DAG-only deploys](https://docs.astronomer.io/astro/deploy-dags) enabled by default. When DAG-only deploys are enabled, some workflows for your Deployment, including image-based deploys, are different. For more information about what happens to code deploys when DAG-only deploys are enabled, see [What happens during a project deploy](https://docs.astronomer.io/astro/deploy-project-image#what-happens-during-a-project-deploy). To disable DAG-only deploys, see [Enable/ disable DAG-only deploys on a Deployment](https://docs.astronomer.io/astro/deploy-dags#enable-disable-dag-only-deploys-on-a-deployment).

### Teams now have Organization-level roles

All Teams on Astro now have an Organization role. Existing Teams have been given the [Organization Member](https://docs.astronomer.io/astro/user-permissions#organization-roles) role, which doesn't result in any additional automatic permissions.

Coupled with [SCIM user groups](https://docs.astronomer.io/astro/set-up-scim-provisioning), you can now manage your Organization Owners and Billing Admins from your identity provider. See [Manage teams](https://docs.astronomer.io/astro/manage-teams) for more information. 

### Additional improvements

- The Cloud UI now shows how many Workspaces, DAGs, clusters, and Astro Cloud IDE projects you have in the left sidebar.
- You can now create Deployments in standard clusters hosted in `europe-west2` on GCP and `eu-central-1` on AWS.
- The default metadata database instance type for new Deployments on GCP clusters in Astro Hybrid has been reduced to `Small General Purpose` with 2 vCPUs and 8GiB. See [GCP Hybrid cluster settings](https://docs.astronomer.io/astro/resource-reference-gcp-hybrid).

### Bug fixes

- Because some regions don't support specific machine types that Astro Hosted uses, you can no longer create Hosted dedicated clusters in the following AWS regions:

    - `af-south-1`
    - `ap-east-1`
    - `ap-northeast-2`
    - `ap-northeast-3`
    - `ca-central-1`
    - `eu-south-1`
    - `eu-west-3`
    - `me-south-1`

## July 25, 2023

### Additional improvements

- The templates for [Astro alert](https://docs.astronomer.io/astro/alerts) messages have been updated to include more information about the Deployment that the alert was triggered in, including a link to the DAG that triggered the alert. 

### Bug fixes

- Fixed an issue where Azure AD single sign-on (SSO) connections were incorrectly labeled as SAML connections in the Cloud UI.

## July 18, 2023

### Configure default Pod sizes

<HostedBadge/>

You can now configure the default minimum CPU and memory for tasks that you run with the Kubernetes executor or KubernetesPodOperator. If you don't specify CPU or memory in a task definition, Astro runs the task in a Pod that uses your default resource configurations. Configure default minimum resources to ensure that tasks always have enough CPU and memory to run successfully. See [Deployment settings](https://docs.astronomer.io/astro/deployment-settings#configure-kubernetes-pod-resources).

### New regions available on Astro Hosted

<HostedBadge/>

You can now create Hosted dedicated clusters in the following regions:

- AWS
    - `af-south-1` - Africa (Cape Town)        
    - `ap-east-1` - Asia Pacific (Hong Kong)  
    - `ap-northeast-1` - Asia Pacific (Tokyo)      
    - `ap-northeast-2` - Asia Pacific (Seoul)      
    - `ap-northeast-3` - Asia Pacific (Osaka)      
    - `ap-southeast-1` - Asia Pacific (Singapore)  
    - `ap-southeast-2` - Asia Pacific (Sydney)     
    - `ap-south-1` - Asia Pacific (Mumbai)     
    - `ca-central-1` - Canada (Central)          
    - `eu-central-1` - Europe (Frankfurt)        
    - `eu-south-1` - Europe (Milan)            
    - `eu-west-1` - Europe (Ireland)          
    - `eu-west-2` - Europe (London)           
    - `eu-west-3` - Europe (Paris)            
    - `me-south-1` - Middle East (Bahrain)     
    - `sa-east-1` - South America (São Paulo) 
    - `us-east-1` - US East (N. Virginia)     
    - `us-east-2` - US East (Ohio)            
    - `us-west-1` - US West (N. California)   
    - `us-west-2` - US West (Oregon)          

- GCP
    - `asia-east1` - Taiwan, Asia                  
    - `asia-northeast1` - Tokyo, Asia                   
    - `asia-northeast2` - Osaka, Asia                   
    - `asia-northeast3` - Seoul, Asia                   
    - `asia-south1` - Mumbai, Asia                  
    - `asia-south2` - Delhi, Asia                   
    - `asia-southeast1` - Singapore, Asia               
    - `asia-southeast2` - Jakarta, Asia                 
    - `australia-southeast1` - Sydney, Australia             
    - `australia-southeast2` - Melbourne, Australia          
    - `europe-central2` - Warsaw, Europe                
    - `europe-north1` - Finland, Europe               
    - `europe-southwest1` - Madrid, Europe                
    - `europe-west1` - Belgium, Europe               
    - `europe-west2` - England, Europe               
    - `europe-west3` - Frankfurt, Europe             
    - `europe-west4` - Netherlands, Europe           
    - `europe-west6` - Zurich, Europe                
    - `europe-west8` - Milan, Europe                 
    - `europe-west9` - Paris, Europe                 
    - `northamerica-northeast1` - Montreal, North America       
    - `northamerica-northeast2` - Toronto, North America        
    - `southamerica-east1` - Sau Paolo, South America      
    - `southamerica-west1` - Santiago, South America       
    - `us-central1` - Iowa, North America           
    - `us-east1` - South Carolina, North America 
    - `us-east4` - Virginia, North America       
    - `us-east5` - Columbus, North America       
    - `us-south1` - Dallas, North America         
    - `us-west1` - Oregon, North America         
    - `us-west2` - Los Angeles, North America    
    - `us-west3` - Salt Lake City, North America 
    - `us-west4` - Nevada, North America         

See [Astro Hosted resource reference](https://docs.astronomer.io/astro/resource-reference-hosted#dedicated-cluster-configurations) for all available configurations. 

### Bug fixes

- You can no longer create Hybrid GCP clusters in `eu-north-1`.

## July 11, 2023

### Send Astro alerts to email

You can now send Astro alerts to multiple email addresses. Sending Astro alerts to email requires no configuration outside of Astro, which makes it a quick option to improve your alerting infrastructure. See [Configure Astro alerts](https://docs.astronomer.io/astro/alerts?tab=Email#step-1-configure-your-communication-channel) for setup steps.

### Configure SCIM provisioning for Azure AD

If your Organization uses Azure for single sign-on (SSO), you can now set up SCIM provisioning for Astro. SCIM provisioning simplifies user management by allowing you to add and remove Astro users from Okta based on your existing user groups. See [Set up SCIM provisioning](https://docs.astronomer.io/astro/set-up-scim-provisioning?tab=Azure#setup) for more information.

### Additional improvements

- On Astro Hosted deployments, the [`astronomer_monitoring_dag`](https://docs.astronomer.io/astro/runtime-image-architecture#astro-monitoring-dag-hybrid-only) has been paused for all image-based Deployments and removed entirely from all Deployments with DAG deploys enabled. It has been replaced with an implementation that allows workers on Deployments to fully scale to 0.

## July 5, 2023

### Configure SCIM provisioning for Okta

If your Organization uses Okta for single sign-on (SSO), you can now set up SCIM provisioning for Astro. SCIM provisioning simplifies user management by allowing you to add and remove Astro users from Okta based on your existing user groups. See [Set up SCIM provisioning](https://docs.astronomer.io/astro/set-up-scim-provisioning?tab=Okta#setup) for more information.

### See pricing estimate when creating a Deployment 

<HostedBadge/>

The Deployment creation page in the Cloud UI has been reorganized to make it easier to focus on specific configurations for your Deployment. Each configuration is now collapsible and includes guidance for different environment sizes. Additionally, the page now shows cost estimates for a Deployment before you create it.

![Deployment creation screen with new pricing information](/img/release-notes/deployment-pricing.png)

### Additional improvements

- You can now configure Deployments with the `A40` machine type, which has 8 vCPU and 16 GiB. See [Astro hosted resource reference](https://docs.astronomer.io/astro/resource-reference-hosted).
- You can now access your Organization settings from a Workspace by clicking the name of your Organization/ Workspace.
- On Astro Hybrid, the default Azure DB instance is now `Standard D2ds_v4`.
- The Deployment creation screen for Astro Hybrid has received several updates that were previously only available on Astro Hosted.

### Bug fixes

- Fixed an issue where DAGs that used the KubernetesPodOperator and had tasks with `in_cluster=False` could not be parsed.

## June 27, 2023

### Support for dedicated clusters on Azure

<HostedBadge/>

You can now create a dedicated cluster in the following Azure regions:

- `australiaeast`
- `eastus2`
- `northeurope`
- `westeurope`
- `uswest2`

See [Astro Hosted resource reference](resource-reference-hosted.md) for more information.

### Additional improvements

- The Cloud UI now shows how many Workspaces each Team belongs to in **Settings** > **Access Management** > **Teams**.
- You can now create dedicated clusters in `us-west1` on GCP.

## June 20, 2023

### Additional improvements

- You can now add a new Astro user to Workspaces before the user has accepted their invite.
- If you have Organization Owner permissions, you can now add a user to a Workspace even if the user hasn't been added to your Organization. Users added to Workspaces this way are automatically added to your Organization as an Organization Member.
- The Cloud UI now shows your Team IDs in **Settings** > **Access Management** > **Teams**. Use Team IDs to add Teams to Workspaces using the Astro CLI.
- A Team's **Updated At** and **Updated By** values are now updated when you change the Team's permissions in a Workspace or Organization.

### Bug fixes

- Fixed an issue where a Workspace descriptions were incorrectly required when creating a new Workspace through the Astro CLI.

## June 13, 2023

### Manage billing and track usage for Astro Hosted

Use the new **Billing** page in the Cloud UI to see both high-level and detailed metrics about your spend in Astro Hosted. You can also use this page to configure your billing details and view invoices. See [Manage billing](https://docs.astronomer.io/astro/manage-billing) for more details.

### New cell type for using Airflow operators in the Astro Cloud IDE

You can now use any Airflow operator available on the Astronomer Registry in your Astro Cloud IDE pipeline. Operator cells apply formatting and checks for parameter inputs, making it easy to configure operators as part of your pipeline. See [Use Airflow operators in the Astro Cloud IDE](https://docs.astronomer.io/astro/cloud-ide/use-airflow-operators).

Additionally, you can configure custom cells to use your team's custom operators in a pipeline. See [Create custom operator cells](https://docs.astronomer.io/astro/cloud-ide/use-airflow-operators#create-custom-operator-cells).

### IMDSv2 is now enforced on AWS clusters

:::warning Breaking change

If your DAGs assume IAM roles to directly access metadata on your cluster using IMDSv1, this change can result in DAG run failures. Upgrade your DAGs to use IMDSv2 for all cluster metadata requests.

See [Use IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) for more information.

:::

Astronomer now enforces IMDSv2 on all AWS clusters. Any requests for resources on your clusters are now session-based and muse include a token in the request body.

### Additional improvements

- Trial Deployments now have [DAG-only deploys](https://docs.astronomer.io/astro/deploy-code#deploy-dags-only) enabled by default.
- The Cloud UI now shows your **Organization Short Name** and **Astro SAML Connection Name** in the Cloud UI.
- You can now view mapped tasks from the **DAGs** page in the Cloud UI.

### Bug fixes

- Fixed an issue where worker node pools in Hosted dedicated clusters on Azure were not being updated correctly.
- Fixed an issue the Cloud UI would reset a Deployment's **Min Worker Count** from 0 to 1 after you edited the Deployment in any way.

## June 6, 2023

### Track user actions and ensure compliance with audit logs

You can now export audit logs from the Cloud UI to view all actions taken in your Organization over a given time period. See [Export audit logs](audit-logs.md) for setup steps.

### Additional improvements 

- You can now configure Hybrid GCP clusters with additional Memory Optimized and Compute Optimized Cloud SQL instance types. See [Supported Cloud SQL instance types](resource-reference-gcp-hybrid.md#supported-cloud-sql-instance-types).

## May 30, 2023

### Manage permissions for groups of users with Teams

Configure Teams from the Cloud UI to manage the permissions for many users across Workspaces from a single page. _Teams_ are a group of users in an Organization that you grant the same Workspace permissions, without needing to define them individually. 

See [Make a Team](https://docs.astronomer.io/astro/manage-teams) for setup steps.

### Bug fixes

- In Astro Hosted, an irrelevant **AWS external ID** info page has been removed from the Cloud UI.
- Fixed an issue where DAG-only deploys could be unreliable due to the deploy process not requesting enough resources in the cluster. 

## May 23, 2023

### Introducing Astro Hosted and Hybrid

_Astro Hosted_ is a new way to run Airflow on Astronomer's cloud. On Astro Hosted, Airflow environments are managed and hosted entirely by Astronomer, enabling you to shift your focus from infrastructure to data. 

For more information about how Astro Hosted works, see the [Architecture overview](https://docs.astronomer.io/astro/astro-architecture).

If you're already an Astro user and your Deployments run in your company's own cloud, you're using _Astro Hybrid_. This version of Astro was formerly known as Astro - Bring Your Own Cloud. 

To see whether you're an Astro Hybrid user, open your Organization in the Cloud UI and go to **Settings** > **General**. Your version of Astro is listed under **Product Type**. 

See [Documentation refactor for Astro Hybrid](#documentation-refactor-for-astro-hybrid) to learn how the documentation has changed for current Astro Hybrid users.

### Configure default Kubernetes Pods on Astro Hosted

One of the biggest risks of running the Kubernetes executor or KubernetesPodOperator is that your tasks can accidentally request more resources than expected, which can drive up costs. To limit this risk, you can now configure default and maximum Pod resources from the Cloud UI. If a task tries to request Pod resources that are more than your configured limits, the task fails. 

See [Configure Kubernetes Pod resources](deployment-settings.md#configure-kubernetes-pod-resources) for setup steps. 

### Documentation refactor for Astro Hybrid

The following updates have been made to documentation to accommodate new Astro Hosted information:

- Astro Hybrid documentation now has a dedicated menu under "Administration" that contains all docs related to Hybrid installation and cluster management. See [Astro Hybrid overview](https://docs.astronomer.io/astro/hybrid-overview).
- All other docs now assume Astro Hosted by default. If a feature is functionally different between Hosted and Hybrid, the documentation for that feature will include a note about how that setup differs for Hybrid. Look for the blue **Alternative Astro Hybrid setup** notes throughout documentation.

## May 16, 2023

### Automate Organization management with Organization API tokens

You can now create Organization API tokens to automate key actions across your Organization and all of the Workspaces in it. You can customize the role and expiration date of the token to give it the minimum required permissions for the task it completes. Some common actions that you can automate with Organization API token are:

- Creating Workspaces.
- Inviting users to an Organization or Workspace.
- Creating and updating Deployments using a [Deployment file](manage-deployments-as-code.md).
- Exporting audit logs.
- Gathering metadata about Deployments using the Airflow REST API.
- Completing any of the actions you can complete with a Workspace API token or Deployment API key across all Deployments in your Organization.

See [Manage Organization API tokens](organization-api-tokens.md) for more information.

## May 2, 2023

### Receive Astro alerts on Slack or PagerDuty

Astro alerts are a new way to be notified when your DAGs aren't running as expected. Unlike Airflow callbacks and SLAs, Astro alerts require no changes to DAG code and integrate with Slack and PagerDuty.

You can set an alert on any DAG to be notified when the DAG fails or when a task takes longer to run than expected. See [Astro alerts](alerts.md) for configuration steps.

### Bug fixes

- Fixed an issue where SSO configurations made through Astronomer support could be overridden by updating the SSO configuration through the Cloud UI.

## April 26, 2023

### Improved log viewing in the Cloud UI

The Deployment **Logs** page in the Cloud UI now shows logs for your Deployment's workers, schedulers, triggerers, and webserver. Additionally, you can now view up to the last 10,000 logs emitted by your Deployment from the Cloud UI.

To make it easier to parse this larger log volume, the **Logs** page now lets you filter by log type, date, and keyword. See [View logs](view-logs.md) for more information.

## April 18, 2023

### Self-service configuration for single sign-on (SSO) connections

You can now configure SSO connections directly from the Cloud UI without assistance from Astronomer support. Use the **Authentication** page to configure different authentication environments for your Organization by creating and managing multiple SSO connections and domains.

To review the new process for creating SSO connections, see [Set up authentication and SSO](configure-idp.md). To create new managed domains to map to your SSO connections, see [Manage domains](manage-domains.md).

## April 11, 2023

### Additional improvements

- The node type for running Airflow system components on GCP clusters has been reduced from `n2-standard-4`  to `e2-standard-4`.
- To optimize infrastructure costs for running the Kubernetes executor, Kubernetes executor worker Pods from different Deployments can now run on the same worker node. This occurs only when the Deployments are hosted in the same cluster and use the same worker node instance type.

## April 4, 2023

### Preview Deployments

You can now create preview Deployments from feature branches in your Git repository. Use a [preview Deployment template](/ci-cd-templates/template-overview.md#preview-deployment-templates) or [GitHub Actions template](/ci-cd-templates/github-actions.md#deployment-preview-templates) to configure your Astro pipelines to:
- Create the preview Deployment when you create a new branch.
- Deploy code changes to Astro when you make updates in the branch.
- Delete the preview Deployment when you delete the branch.
- Deploy your changes to your base Deployment after you merge your changes into your main branch.

### Additional improvements

- Added the ability to enforce CI/CD deploys. You can now configure your Deployment to only accept code deploys if they are triggered by a Deployment API key or Workspace token.
- When you create a new cell in the Astro Cloud IDE, the editor auto-scrolls to your new cell and selects it.

### Bug fixes

- Fixed a bug where the UI passed the wrong cluster type. 
- Fixed an issue where the Deployment status shows as 'deploying' when KPOs are running.

## March 28, 2023

### New GCP node instance types available

<HybridBadge/>

You can now use the following node instance types for worker nodes in GCP clusters:

- `e2-standard-32`
- `e2-highcpu-32`
- `n2-standard-32`
- `n2-standard-48`
- `n2-standard-64`
- `n2-highmem-32`  
- `n2-highmem-48`  
- `n2-highmem-64`  
- `n2-highcpu-32`  
- `n2-highcpu-48`  
- `n2-highcpu-64`  

For a list of all instance types available for GCP, see [Supported worker node pool instance types](resource-reference-gcp-hybrid.md#supported-worker-node-pool-instance-types).

### Additional improvements

- You can now use `db.m6g` and `db.r6g` RDS instance types on AWS clusters.
- The default RDS instance type for new AWS clusters has been reduced from `db.r5.large` to `db.m6g.large`
- The default CIDR range for new AWS clusters has been reduced from /19 to /20.
- You can now submit a **Request type** in the [Cloud UI support form](https://cloud.astronomer.io/support). When you choose a request type, the form updates to help you submit the most relevant information for your support request.
- You can no longer delete a Workspace if there are any Astro Cloud IDE projects still in the Workspace.
- Organization role permissions have changed so that only Organization Owners can create Workspaces.

### Bug fixes

- Fixed an issue where you could set a Deployment's scheduler resources to less than 5 AU.

## March 21, 2023

### Automate Workspace and Deployment actions using Workspace API tokens

Use Workspace API tokens to automate Workspace actions, such as adding users to a Workspace and creating new Deployments, or for processes that a [Deployment API key](api-keys.md) can automate. You can customize the role and expiration date of the token to give it the minimum required permissions for the task it completes.

To create and use Workspace API tokens, see [Workspace API tokens](workspace-api-tokens.md).

### Additional improvements

- In the Astro Cloud IDE, you can now specify the output table for a Warehouse SQL cell using both literal and Python expressions. See [Create a SQL cell](cloud-ide/run-sql.md#create-a-sql-cell).
- Port 80 is no longer used for certificate management on the data plane.
- To switch Organizations in the Cloud UI, you now use the **Switch Organization** button next to your Organization's name.

    ![Switch Organizations button](/img/release-notes/switch-organizations.png)

## March 15, 2023

### Run the Kubernetes executor in Astro

You can now configure your Deployments to use the Kubernetes executor for executing tasks. Using the Kubernetes executor, you can:

- Ensure that tasks running longer than 24 hours are not interrupted when your team deploys code.
- Run tasks with different version dependencies in the same Astro project.
- Request specific amounts of CPU and memory for individual tasks.
- Automatically down your resources when no tasks are running.

The Kubernetes executor runs each task in its own Kubernetes Pod instead of in shared Celery workers. Astronomer fully manages the infrastructure required to run the executor and automatically spins Pods up and down for each of your task runs. This executor is a good fit for teams that want fine-grained control over the execution environment for each of their tasks.

To learn whether the Kubernetes executor works for your use case, see [Choose an executor](executors-overview.md#choose-an-executor). To configure the Kubernetes executor for a task or Deployment, see [Configure the Kubernetes executor](kubernetes-executor.md).

### Simplified Organization management in the Cloud UI

The Cloud UI has been redesigned so that Organization settings tabs are now available in the left menu. Use this new menu to switch between pages as you can for Workspace settings.

While most tabs were migrated directly to the left menu with the same name, some pages have been renamed and moved:

- Formerly located in **Overview**, your Workspace list is now available in **Workspaces**.
- Formerly located in the **People** tab, Organization user management settings are now in **Settings** > **Access Management**.
- Formerly located in the **Settings** tab, general Organization settings are now in **Settings** > **General**.

### New Astro Cloud IDE integration with GitLab

You can now configure a GitLab repository in your Astro Cloud IDE project. Configuring a GitLab repository allows you to commit your pipelines and deploy them to Astro directly from the Astro Cloud IDE. See [Deploy a project from a Git repository to Astro](cloud-ide/deploy-project.md#deploy-a-project-from-a-git-repository-to-astro).

### Additional improvements

- Clusters on an Astro - Hosted installation no longer retain Airflow logs which are older than 90 days.
- The Data Plane System node pool instance type on GCP clusters has been reduced from `n2-standard-4` to `n2-standard-2`.

## March 7, 2023

### Get expert advice on Astro and Airflow in office hours

Office hours are a new way for Astro customers to meet with the Astronomer Data Engineering team. In an office hour meeting, you can ask questions, make feature requests, or get expert advice for your data pipelines.

You can now schedule a 30-minute office hour meeting in the **Help** menu next to your user profile in the Cloud UI.

![Button to book office hours in the Cloud UI](/img/release-notes/office-hours.png)

For more information, see [Book office hours in the Cloud UI](astro-support.md#book-office-hours-in-the-cloud-ui).

### Additional improvements

- The node pool instance type used for Astro system components on GCP clusters has been reduced from `n2-standard-4` to `n2-standard-2`.
- DAGs generated by the Astro Cloud IDE now use UTC instead of your current timezone as the default timezone for scheduling DAG runs.

### Bug fixes

- Fixed an issue in the Astro Cloud IDE where you could not update a pipeline that was configured with an invalid cyclic dependency chain.
- Fixed an issue where deploying an Astro project with a custom Docker image tag resulted in the Deployment always having the **Deploying** status in the Cloud UI.
- Fixed an issue where worker Pods on Azure clusters were sometimes unable to scale because there was no prioritization for starting up essential scheduling Pods.

## March 1, 2023

### Astro no longer requires administrator access on AWS

Astro no longer requires administrator permissions for its dedicated AWS account. Instead, Astro now assumes a cross-account IAM role with the minimum necessary permissions for running and managing clusters. See [Install Astro on AWS](install-aws-hybrid.md) for more information.

### IdP-initiated logins through the Okta dashboard

If your Organization uses Okta as your Astro identity provider, you can now log in to Astro directly from your [Okta Apps dashboard](https://help.okta.com/eu/en-us/Content/Topics/end-user/dashboard-overview.htm). If you've been authenticated by Okta, you no longer need to be authenticated by Astro when you access it through your dashboard.

### Additional improvements

- Ingress to the Kubernetes API on Google Cloud Platform (GCP) and Azure clusters is now limited to Astro control plane IPs. This change will be implemented on all clusters in the coming weeks.

### Bug fixes

- To protect the functionality of Astro monitoring services, you can no longer override the values of the following environment variables:
  
  - `AIRFLOW__METRICS__STATSD_ON`
  - `AIRFLOW__METRICS__STATSD_HOST`
  - `AIRFLOW__METRICS__STATSD_PORT`
  - `AIRFLOW__METRICS__STATSD_ALLOW_LIST`
  - `AIRFLOW__METRICS__STATSD_STATSD_CUSTOM_CLIENT_PATH`
  - `AIRFLOW__METRICS__STATSD_PREFIX`

    You can still set new values for these variables, but the values will be automatically overwritten in the Astro data plane. See [Platform variables](platform-variables.md).
  
- Fixed an issue where a user could provision multiple accounts when their login email address included differently cased characters.

## February 21, 2023

### New identity-first authentication model

Astro has migrated to an identity-first authentication model. Users now authenticate to the Astro platform instead of individual Organizations, and Organizations can set permissions for how users can modify and access resources. This model prioritizes identity verification and enforces authentication policies for user email domains.

For all users logging in to Astro, this migration has the following effects:

- Instead of being redirected to separate login pages for each Organization, all Astro users log in through a universal login page.
- Users belonging to multiple Organizations no longer have to log in again when switching Organizations.
- Users no longer need to enter their email on a separate page before they log in to the Cloud UI.
- If your Organization enforces single sign-on (SSO), users can now authenticate to Astro with a username and password when your email domain doesn't enforce SSO.

For Organization Owners, this migration has the following additional effects:

- You can now use an SSO bypass link to log in to Astro if your SSO connection is disrupted.
- Your Organization now has a list of owned email domains, and any users logging into Astro with one of those domains will be redirected to your configured identity provider.

For more information about how these changes can affect the Astro log in experience, see the [Login FAQ](log-in-to-astro.md#frequently-asked-questions). To configure authentication behavior, see [Configure SSO](configure-idp.md#advanced-setup).

### New Hosted regions available

You can now create clusters in the following regions on an Astro - Hosted installation.

- AWS
  
  - `ap-northeast-1`
  - `ap-southeast-2`
  - `eu-central-1`
  - `eu-west-1`
  - `us-east-1`
  - `us-west-2`

- Google Cloud

  - `asia-northeast1`
  - `australia-southeast1`
  - `europe-west1`
  - `europe-west2`
  - `us-central1`
  - `us-east4`

- Microsoft Azure

  - `australiaeast`
  - `japaneast`
  - `northeurope`
  - `westeurope`
  - `eastus2`
  - `westus2`

### Additional improvements

The default CIDR ranges for new GCP clusters have been reduced. The following are the new CIDR ranges:

- **Subnet CIDR**: `172.20.0.0/22`
- **Pod CIDR**: `172.21.0.0/19`
- **Service Address CIDR**: `172.22.0.0/22`
- **Service VPC Peering**: `172.23.0.0/20`

### Bug fixes

In the Cloud UI, when using **Compare** on the **Lineage Graph** page, you can now compare shorter run lengths.

## February 14, 2023

### Authorize Workspaces to clusters

You can now keep teams and projects isolated by authorizing Workspaces to specific clusters. Use this feature to better manage cloud resources by ensuring that only authorized Deployments are running on specific clusters.

To authorize Workspaces to clusters, see [Authorize Workspaces to a Cluster](manage-hybrid-clusters.md#authorize-workspaces-to-a-cluster).

### New Deployment health statuses and information in the Cloud UI

The Cloud UI now includes three additional [Deployment health statuses](deployment-metrics.md#deployment-health) that you might see when creating or pushing code to a Deployment.

- The **Creating** status indicates that Astro is still provisioning the resources for the Deployment.
- The **Deploying** status indicates that a code deploy is in progress. Hover over the status indicator to view specific information about the deploy, including whether it was an image deploy or a DAG-only deploy.
- The **Unknown** status indicates that Deployment status can't be determined.

Additionally, the Deployment information page in the Cloud UI now includes fields for **Docker Image** and **DAG Bundle Version** that show unique timestamps and tags based on your latest code deploy. Use this information as the source of truth for which version of your code is currently running on the Deployment. See [Deploy code](deploy-code.md#step-3-validate-your-changes).

### View OpenLineage facets for lineage job runs

[OpenLineage facets](https://openlineage.io/docs/spec/facets/) are JSON objects that provide additional context about a given job run. By default, a job run includes facets that show what kind of job was completed, whether the job run was successful, and who owns the job.

You can now view all available facets for a job run, including [custom facets](https://openlineage.io/docs/spec/facets/custom-facets), by opening the job run's **Lineage Graph** and then selecting the **Info** tab. You can check the status of your facets, including whether they are correctly formatted, so that you can resolve potential issues in your data pipelines. See [View metrics for a specific run or dataset](data-lineage.md#view-metrics-for-a-specific-run-or-dataset).

![Example OpenLineage facet page in the Cloud UI](/img/release-notes/view-facets.png)

### Additional improvements

- You can now create AWS clusters in `ap-northeast-1` and `ap-southeast-2` on an Astro - Hosted installation.
- You can now create GCP clusters in `australia-southeast1` on an Astro - Hosted installation.

### Security fixes

- Fixed [CVE-2023-0286](https://nvd.nist.gov/vuln/detail/CVE-2023-0286).

## February 7, 2023

### Additional improvements

- The instructions on the welcome page for new Astro users who are not yet part of an Organization have been improved to make getting started easier.

### Bug fixes

- Removed nonfunctioning date filtering functionality from the Lineage UI.
- Fixed an issue where triggering an image deploy from an older version of the Astro CLI could unintentionally turn off DAG deploys on a Deployment.

## January 31, 2023

### Bug fixes

- When you select **Mark Success** or **Clear** for Deployment task actions in the Airflow UI, you are now correctly redirected to the DAG **Tree** view instead of the **DAGs** homepage.
- Fixed [CVE-2022-41721](https://avd.aquasec.com/nvd/2022/cve-2022-41721/).

## January 24, 2023

### New Workspace Home page

When you select a Workspace in the Cloud UI, the **Home** page now appears first. On this page, you can:

- Check the status of your Deployments.
- Quickly access your most recently viewed Deployments and Cloud IDE projects.
- View release notes for all Astro products.

![Workspace home page in the Cloud UI](/img/release-notes/workspace-home.png)

See [Introducing Astro’s New Workspace Homepage](https://www.astronomer.io/blog/introducing-astros-new-workspace-homepage/) for more information.

### Additional improvements

- Ingress to the Airflow UI and API on Astro clusters is now limited to control plane IPs. This change will be implemented on all clusters in the coming weeks.
- You can now request custom tags for your AWS clusters by submitting a support request to [Astronomer support](https://cloud.astronomer.io/support). You can view your cluster tags in the Cloud UI by selecting **Clusters**, selecting a cluster, and then clicking the **Details** tab. See [View clusters](manage-hybrid-clusters.md##view-clusters).
- You can now create new clusters in France Central for Bring Your Own Cloud installations of Astro on Azure.
- Improved the speed of DAGs appearing in the Airflow after completing a DAG-only deploy.

### Bug fixes

- Fixed [CVE-2022-48195](https://avd.aquasec.com/nvd/2022/cve-2022-48195/).

## January 18, 2023

### Bug fixes

- Fixed an issue with Google Cloud Platform (GCP) clusters where the metadata database for a Deployment could persist after the Deployment was deleted.

## January 10, 2023

### New Astro Cloud IDE cell types

To simplify the creation of new tasks, the following new cell types are now available in the Astro Cloud IDE:

- **SQL**: Run a SQL query against an existing database connection and save the query results in an XCom file for use by other cells. Use this cell type to run smaller queries and store the results in Airflow for quick access by other cells.
- **Warehouse SQL**: Run a SQL query against an existing database connection and store the query results in your data warehouse. Use this cell type for data operations that require more storage and reliability.
- **Markdown**: Add inline Markdown comments to your generated DAG code. Use this cell type to document code decisions and to make it easier for team members to collaborate on shared pipelines.

For more information about a specific cell type, see [Run SQL in the Astro Cloud IDE](cloud-ide/run-sql.md), [Run Python in the Cloud IDE](cloud-ide/run-python.md), and [Add documentation to an Astro Cloud IDE pipeline](cloud-ide/document-pipeline.md).

### Additional improvements

- To reduce the time it takes for Airflow to parse new DAG files, the default value for `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` has been reduced from 5 minutes to 30 seconds for all Deployments regardless of Runtime version. For most users, this means that you will see new DAGs appear in the Airflow UI faster.
- In the Cloud UI, a banner now appears if there is an incident reported on the [Astro status page](https://status.astronomer.io/).

### Bug fixes

- Sorting the **Organization Role** column in the **People** tab of the Cloud UI now works as expected.
- Fixed an issue where lineage groups would occasionally not collapse as expected in the **Lineage Graph** view.

## December 20, 2022

### Additional improvements

- You can now configure OneLogin and Ping Identity as identity providers on Astro. See [Configure your identity provider](configure-idp.md#configure-your-identity-provider).
- Workspace Members can now view **Workspace settings** in the Cloud UI.
- Node groups that are collapsed in the lineage graph in the Cloud UI now show only the total number of connected **Jobs** and **Datasets**, instead of listing each job and dataset. This makes the lineage graph easier to navigate.

    ![Collapsed node in lineage graph of Cloud UI](/img/release-notes/collapsed-lineage-node.png)

### Bug fixes

- Fixed an issue where the lineage UI did not show dataset metrics when a dataset had no column-level metrics.
- Fixed an issue where some instances of a dataset's name were inconsistent in the lineage UI.

## December 13, 2022

### Improvements to the Cloud IDE

The [Cloud IDE](cloud-ide/overview.md) includes several new features which improve DAG authoring and testing:

- There is a new **Commit** button in the Cloud UI that is separate from the **Configuring GitHub** menu.
- The default CI/CD pipeline included in the Cloud IDE project supports DAG-only deploys. Deploying DAG changes to Astro using the CI/CD pipeline is now significantly faster.
- The **Configure GitHub** menu in the Cloud UI now includes a **Clone Repo** settings menu. Enabling this option makes other files in your GitHub repository, such as helper functions in the `include` folder of your project, accessible when you run DAGs in the Cloud IDE.
- You can now explicitly mark upstream dependencies for a task cell from the cell's configuration menu.

For more information about configuring GitHub and deploying code with the Cloud IDE, see [Deploy a project from the Cloud IDE to Astro](cloud-ide/deploy-project.md).

### Support for n2 worker types on GCP

You can now configure worker queues with the following `n2` worker types on Google Cloud Platform (GCP) clusters:

- `n2-standard-4`
- `n2-standard-8`
- `n2-standard-16`
- `n2-highmem-4`
- `n2-highmem-8`
- `n2-highmem-16`
- `n2-highcpu-4`
- `n2-highcpu-8`
- `n2-highcpu-16`

For more information about these worker types, see [N2 machine series](https://cloud.google.com/compute/docs/general-purpose-machines#n2_machines). For a list of all worker types available on GCP, see [Worker node size resource reference](resource-reference-gcp-hybrid.md#worker-node-size-resource-reference).

### Additional improvements

- In the **Clusters** tab of the Cloud UI, you can now click a cluster entry to see details about the cluster configuration, including which **Worker Types** are enabled for the cluster.
- The Deployment details page in the Cloud UI now includes an **ID** pane. A Deployment ID is required when you deploy code using a CI/CD process.
- The **OpenLineage URL** for your Organization is now available on the **Settings** page in the Cloud UI. An OpenLineage URL is required to [integrate data lineage from some external systems](set-up-data-lineage.md).
- Workspaces are now sorted alphabetically in the Cloud UI.
- In Astro CLI version 1.8.0 or later, running `astro deploy` with an empty or missing `dags` folder does not erase or override existing DAGs. Instead, the directory is excluded from the build and push process to Astro. This lets you manage your DAGs and project files in separate repositories when using [DAG-only deploys](deploy-code.md#deploy-dags-only).

### Bug fixes

- Fixed an issue where Astro temporarily stored DAGs for DAG-only deploys in a new directory named `/usr/local/airflow/dags/current`, which could cause import errors in user code.
- Fixed an issue where task runs triggered in the Cloud IDE did not have access to project environment variables.
- Fixed an issue where Deployment metrics for memory usage were not always accurate.  

## November 15, 2022

### Additional improvements

- In the Cloud UI, the **People** page now shows the IDs of users belonging to your Organization.
- In the Cloud UI, the **Deployments** page now shows the user or API key that most recently updated each Deployment and when they updated it.

### Bug fixes

- Availability zone (AZ) rebalancing has been disabled for worker node pools on AWS clusters. This change should result in fewer [zombie tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#zombie-undead-tasks) and less volatility across workers. AZ rebalancing is enabled for other system components on Astro.
- The **Updated at** field for a transferred Deployment now displays the correct time.
- `astro deploy --dags` now handles deferrable tasks correctly.

## November 8, 2022

### Deploy only DAGs with `astro deploy -—dags`

Using Astro CLI 1.7, you can run `astro deploy -—dags` to push only the `dags` directory of your Astro project to a Deployment on Astro. This is an additional option to `astro deploy` that makes for a faster development experience and gives you more flexibility in how you configure CI/CD processes.

For more information, see [Astro CLI 1.7](astro/cli/release-notes#deploy-only-dags-with-astro-deploy--dags) or [Deploy DAGs only](deploy-code.md#deploy-dags-only). For example CI/CD workflows with this feature enabled, see [CI/CD](ci-cd-templates/template-overview#dag-deploy-templates).

### Improved data lineage interface

The **Lineage** tab has new features and is better integrated into the Cloud UI.

![Updated lineage page](/img/release-notes/lineage-integrated.png)

Specifically, the tab includes the following improvements:

- The process for comparing runs uses a simpler interface and provides more information about the runs you're comparing. See [Compare lineage graphs from previous runs](data-lineage.md#compare-lineage-graphs-from-previous-runs).
- Names for UI elements have been updated to more clearly represent Airflow resources. For example, **jobs** is now **runs**, and the **Explore** tab is now **Runs**.
- Lineage graphs include new colors and animations to show the flow of data as it moves between runs and datasets.

### Transfer a Deployment

You can now transfer a Deployment from one Workspace to another in your Organization. This feature is helpful if you need to change the group of users that have access to a Deployment, or if you create a Deployment in the wrong Workspace.

See [Transfer a Deployment to another Workspace](deployment-settings.md#transfer-a-deployment-to-another-workspace).

### Additional improvements

- The Kubernetes API is no longer exposed to the public internet on AWS data planes. The allowlist is limited to control plane IPs. New clusters will be created with this configuration, while all existing clusters will be updated by end of next week.

## November 1, 2022

### Introducing the Astro Cloud IDE, a new Airflow development experience

Astronomer is excited to introduce the Astro Cloud IDE, which is a notebook-inspired development environment for writing, running, and deploying data pipelines. Now you can develop an entire Airflow project, including DAGs, dependencies, and connections entirely within the Cloud UI.

![Example page in the Astro Cloud IDE](/img/release-notes/ide-overview.png)

The Astro Cloud IDE was created with the following objectives:

- Configuring Airflow shouldn't be a barrier to running Airflow.
- Passing data between tasks should be seamless regardless of what language is used to write the task.
- Data pipelines should be quick to deploy and easy to test with CI/CD.

Most importantly, the Astro Cloud IDE was developed to make it easier for new Airflow users to get started and to provide experienced users with a robust development environment.

To create your first project in the Astro Cloud IDE, see the [Cloud IDE quickstart](cloud-ide/quickstart.md). To deploy your project to Astro, see [Deploy your Cloud IDE project to Astro](cloud-ide/deploy-project.md).

### Additional improvements

- In the Cloud UI, cluster selection menus are now alphabetized.

### Bug fixes

- Fixed an issue where the KubernetesPodOperator was not aware of available ephemeral storage in `m5d` and `m6id` worker nodes. This issue resulted in Pods being evicted to free up storage even when there was enough available storage for tasks.
- Fixed an issue in the Cloud UI where you could select a worker type before selecting a cluster when creating a Deployment.
- Fixed an issue where Deployments on Runtime 5.0.10 and earlier showed a nonfunctional **Configuration** tab in the Airflow UI.
- Fixed [CVE-2022-32149](https://nvd.nist.gov/vuln/detail/CVE-2022-32149).

## October 25, 2022

### Additional improvements

- In the Cloud UI, you can now view a cluster's external IP addresses in the **Clusters** tab.

### Bug fixes

- Fixed an issue where some Deployments were running tasks after being deleted.

## October 18, 2022

### Additional improvements

- In the Cloud UI, **Access** has been moved from the left menu to a tab on the **Workspace Settings** page.
- In the Cloud UI, **Workspace Settings** in the left menu is now available to all Workspace members.

### New Azure regions

You can now [create an Astro cluster on Azure](manage-hybrid-clusters.md#create-a-cluster) in the following regions:

- `japaneast`
- `southafricanorth`
- `southcentralus`
  
## October 11, 2022

### Additional improvements

- New worker node pools on Azure and Google Cloud Platform (GCP) clusters can now scale to zero. When you set your minimum worker count to 0, you don't incur costs for enabling a new worker type for your cluster until it's used in a Deployment.

### Bug fixes

- Fixed an issue where worker queues with a minimum worker count of zero would appear with a minimum worker count of one in the Cloud UI.

## October 4, 2022

### New permissions boundary for managed AWS Accounts

The operational roles that Astronomer assumes on dedicated customer AWS accounts now have new [permissions boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) that limit the roles to a subset of their permissions. The remote management role is now limited to the following actions across all contexts:

- `autoscaling:*`
- `cloudformation:*`
- `cloudwatch:*`
- `ec2:*`
- `ecr:*`
- `eks:*`
- `elasticloadbalancing:*`
- `iam:*OpenID*`
- `kms:DescribeKey`
- `lambda:*`
- `logs:*`
- `route53:AssociateVPCWithHostedZone`
- `s3:*`
- `secretsmanager:*`
- `servicequotas:*`
- `ssm:*`
- `tag:*`

These permissions might change in the future to enable new Astro features or to refine permissions for specific contexts.

### Additional improvements

- Users with the required permissions can now access a **Configuration** tab in the **Admin** menu of the Airflow UI. This page no longer shows sensitive values in plain-text and can be used to verify all configurations running on your Deployment.
- In the Cloud UI, the maximum time for Deployment metrics has been extended from 24 hours to 7 days.
- The [Deployment metrics overview](deployment-metrics.md#deployment-overview) now shows metrics for the `default` worker queue instead of an aggregate of all worker queues. Improved worker queue metrics coming soon.

### Bug fixes

- Added the global environment variable `AIRFLOW__LOGGING__DAG_PROCESSOR_LOG_TARGET=stdout` so that a scheduler's logs don't overcrowd its local storage
- Removed misleading maximum CPU and memory lines from Deployment metric graphs

## September 28, 2022

### Additional improvements

- All worker queue configurations in the **Worker Queues** tab of the Cloud UI now have tooltips.
- The **Worker CPU** and **Worker Memory** metrics in the **Analytics** tab of the Cloud UI now show metrics only for the default worker queue instead of an average across queues. Improved worker queue metrics coming soon.

### Bug fixes

- Values in the Organization **Settings** page no longer overlap with other UI elements.
- Organization Owners can now [push code](deploy-code.md) to a Deployment even if they aren't explicit members of the Deployment's Workspace.

## September 21, 2022

### A simpler Deployment page

All of a Deployment's configurations, including analytics, API keys, environment variables, and resource configurations, are now organized as tabs within the Deployment's page in the Cloud UI.

![New organization of Deployment-level pages in the Cloud UI](/img/release-notes/deployment-tabs.png)

This new UI moves the **Analytics** and **Logs** from the left sidebar to the main Deployment page so that you no longer have to filter those views separately by Deployment. The left sidebar now exclusively contains Workspace-level menus.

### New Account Dashboard

You can now access your Account Dashboard to manage your user account settings and find links to helpful resources. Access this page by going to `account.astronomer.io` in your browser or by clicking **Profile** > **Manage your Astro Account** in the Cloud UI. You must be authenticated to Astro.

![New user home page](/img/release-notes/user-home.png)

### Additional improvements

- You can now use the `m6id` worker node type series for Deployments on AWS clusters. This worker type is general purpose and includes significant storage as well as up to 15% better performance compared to `m5d` nodes. For more information, see [Worker instance types](resource-reference-aws-hybrid.md#worker-node-types).
- New worker node pools on Amazon Web Services (AWS) clusters can now scale to zero. This means that enabling a new worker type for your cluster does not cost you until it's used in a Deployment.

### Bug fixes

- Fixed an issue where the Cloud UI Deployment metrics showed a maximum worker CPU and memory that was inconsistent with your configured worker queues.

## September 14, 2022

### Additional improvements

- When you create a new worker queue, the default worker type in your cluster is now pre-selected in the **Worker Type** list.
- You can now configure multiple instances of the same identity provider (IdP). See [Configure an identity provider](configure-idp.md).
- You can now expand and collapse the **Workspace** menu in the Cloud UI.

### Bug fixes

- Fixed an issue where you could not open the Airflow UI from a Deployment.

## August 31, 2022

### Export Deployment metrics to Datadog

You can now export over 40 Airflow metrics related to the state of your Astro Deployment to [Datadog](https://www.datadoghq.com/) by adding a Datadog API key to the Deployment. Metrics include task successes, DAG processing time, frequency of import errors, and more.

For organizations already using the observability service, this integration allows your team to standardize on tooling and gain a more granular view of Deployment metrics in a single place. Once the integration is configured, Astro automatically exports all available metrics to Datadog. For a complete list of supported metrics, see [Data Collected](https://docs.datadoghq.com/integrations/airflow/?tab=host#data-collected).

To learn more, see [Export Airflow metrics to Datadog](deployment-metrics.md#export-airflow-metrics-to-datadog).

### Additional improvements

- The Cloud UI now automatically ensures that worker queue names are valid as you type in real time.
- The number of times that a user can enter the wrong credentials for Astro before being locked out has been reduced from 10 to 6.
- You can now configure [worker queues](deployment-settings.md#worker-queues) to have a minimum **Worker count** of 0 workers. Note that depending on your cloud provider and Deployment configurations, some Deployments still might not be able to scale to 0 workers.

### Bug fixes

- The timestamp shown in the **Updated** field of the Deployment view in the Cloud UI is now properly updated when you create or modify environment variables.
- Fixed an issue where logging in to the Airflow UI with unrecognized credentials could freeze you on an error page.

## August 24, 2022

### Additional improvements

- When you configure worker queues in the Cloud UI, the total CPU and memory capacity of each worker instance type is now shown instead of the nominal available resources.
- Improved error handling for creating new worker queues when soft-deleted worker queues might still exist on the data plane.

### Bug fixes

- Fixed an issue where running `astro deploy` with a Deployment API key could revert changes to a worker queue's size that were previously set in the Cloud UI.
- Fixed an issue where the **Lineage** tab in the Cloud UI showed all job durations as having a length of 0.

## August 18, 2022

### Create multiple worker queues

Worker queues are a new way to configure your Deployment to best fit the needs of your tasks. A worker queue is a set of configurations that apply to a group of workers in your Deployment. Within a worker queue, you can configure worker type and size as well as autoscaling behavior. By configuring multiple worker queues for different types of tasks, you can better optimize for the performance, reliability, and throughput of your Deployment.

In the Cloud UI, you can now create multiple worker queues. Once you create a worker queue, you can assign a task to that worker queue by adding a simple `queue='<worker-queue-name>'` argument in your DAG code.

![Worker queue configurations in the Cloud UI](/img/release-notes/worker-queues.png)

This feature enables the ability to:

- Use more than one worker type within a single Deployment and cluster. Previously, a single cluster on Astro supported only one worker type.
- Isolate long-running tasks from short-running tasks to avoid errors related to competing resource requests.
- Fine-tune autoscaling behavior for different groups of tasks within a single Deployment.

For example, if you have a task that requires significantly more CPU than memory, you can assign it to a queue that's configured with workers that are optimized for compute usage.

To learn more about configuring worker queues, see [Configure Deployment resources](deployment-settings.md#worker-queues).

### New worker sizing

This Astro release introduces a new, simple way to allocate resources to the workers in your Deployment. Instead of choosing a varying combination of CPU and memory, you can now select a worker type in the Cloud UI as long as it's enabled in your cluster. For example, `m5.2xlarge` or `c6i.8xlarge` on AWS. Once you select a worker type, Astronomer will create the biggest worker that that worker type can support to ensure that your tasks have enough resources to execute successfully.

Astro's worker sizing enables a few benefits:

- You can no longer configure a worker that is too large or otherwise not supported by your underlying cluster. Previously, misconfiguring worker size often resulted in task failures.
- A more efficient use of infrastructure. Astronomer has found that a lower number of larger workers is more efficient than a higher number of smaller workers.
- A higher level of reliability. This worker sizing model results in less volatility and a lower frequency of cluster autoscaling events, which lowers the frequency of errors such as zombie tasks and missing task logs.
- The legacy **AU** unit is no longer applicable in the context of the worker. You only have to think about CPU, memory, and worker type.

Worker sizing on Astro is now defined in the context of worker queues. For more information about worker sizing, see [Configure Deployment resources](deployment-settings.md#worker-queues). For a list of supported worker types, see the [AWS](resource-reference-aws-hybrid.md#worker-node-types), [GCP](resource-reference-gcp-hybrid.md#worker-node-types), and [Azure](resource-reference-azure-hybrid.md#worker-node-types) resource references.

### New Maximum Tasks per Worker setting

A new **Maximum Tasks per Worker** configuration is now available in the Deployment view of the Cloud UI. Maximum tasks per worker determines the maximum number of tasks that a single worker can process at a time and is the basis of worker autoscaling behavior. It is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow.

Previously, maximum tasks per worker was permanently set to 16 and was not configurable on Astro. Now, you can set maximum tasks per worker anywhere between 1 and 64 based on the needs of your tasks. It can be set per worker queue on a Deployment.

To learn more, see [Worker autoscaling logic](celery-executor.md#celery-worker-autoscaling-logic).

### New Worker Count (Min-Max) setting

A new **Worker Count (Min-Max)** configuration is now available in the Deployment view of the Cloud UI. This value defines the minimum and maximum number of workers that can run at a time.

Use this setting to fine-tune worker autoscaling behavior in your Deployment. By default, the minimum number of workers is 1 and the maximum is 10.

To learn more, see [Worker queue settings](deployment-settings.md#worker-queue-settings).

### Support for multiple Organizations

A single user account can now belong to multiple Organizations. A user with multiple Organizations can switch to another Organization by clicking on their current Organization's name in the Cloud UI and then clicking **Switch Organization**.

Note that switching Organizations with the Astro CLI is not yet supported. For more information, see [Switch Organizations](log-in-to-astro.md#switch-organizations).

### New Azure region (Australia East)

You can now [create an Astro cluster on Azure](manage-hybrid-clusters.md#create-a-cluster) in Australia East (New South Wales).

For a list of all Azure regions that Astro supports, see [Azure resource reference](resource-reference-azure-hybrid.md#supported-regions).

### New Google Cloud Platform regions

You can now [create an Astro cluster on GCP](manage-hybrid-clusters.md#create-a-cluster) in the following regions:

- `australia-southeast2` (Melbourne)
- `asia-east1` (Taiwan)
- `asia-south2` (Delhi)
- `asia-southeast2` - (Jakarta)
- `europe-north1` (Finland)
- `europe-southwest1` (Madrid)
- `europe-west8` (Milan)
- `europe-west9` (Paris)
- `northamerica-northeast2` (Toronto)
- `southamerica-west1` (Santiago)
- `us-east5` (Columbus)
- `us-south1` (Dallas)

### Bug fixes

- Fixed an issue where the Cloud UI's **Resource Settings** page wasn't showing units for CPU and Memory values.

## August 10, 2022

### Updated user permissions for Organization and Workspace roles

The following user roles have new and modified permissions:

- Organization Owners now have Workspace Admin permissions for all Workspaces in their Organization. This role can now access Organization Workspaces, Deployments, and usage data.
- Organization Billing Admins can now view [usage](deployment-metrics.md#astro-usage) for all Workspaces in their Organization regardless of their Workspace permissions.
- Workspace Editors can now delete any Deployment in their Workspace.

### Automatic access for new users authenticating with an identity provider

If your organization has [implemented an identity provider (IdP)](configure-idp.md), any new user who authenticates to Astro through your IdP is now automatically assigned the Organization Member role. This means that users authenticating through your IdP do not need to be invited by email before joining your Organization.

### Additional improvements

- Added a security measure that ensures Workspace roles can only be assigned to users who have an Organization role in the Organization in which the Workspace is hosted. This ensures that a user who does not belong to your Organization cannot be assigned a Workspace role within it.

## August 2, 2022

### Support for Astro on Azure Kubernetes Service (AKS)

Astro now officially supports Astro clusters on AKS. This includes support for an initial set of AKS regions.

For more information about the installation process and supported configurations, see [Install Astro on Azure](install-azure-hybrid.md) and [Resource Reference Azure](resource-reference-azure-hybrid.md).

### Bug fixes

- Pending invites no longer appear for active users in the Cloud UI.

## July 27, 2022

### New Deployment optimizations for high availability (HA)

This release introduces two changes that ensure a higher level of reliability for Deployments on Astro:

- [PgBouncer](https://www.pgbouncer.org/), a microservice that increases resilience by pooling database connections, is now considered highly available on Astro. Every Deployment must now have 2 PgBouncer Pods instead of 1, each assigned to a different node within the cluster. This change protects against pod-level connection issues resulting in [zombie tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#zombie-undead-tasks), which was previously seen during cluster downscaling events. PgBouncer is fully managed by Astronomer and is not configurable.

- The Airflow scheduler is now configured with an [anti-affinity policy](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) to limit the possibility of all schedulers for a single Deployment being impacted by an incident within a single node on an Astro cluster. For users who set **Scheduler Count** in the Cloud UI to 2, this means that those 2 scheduler Pods cannot be assigned to the same node and instead require a minimum of 2 nodes total. To avoid significant increases in cost, 3 or 4 schedulers can share the same 2 nodes and will not necessarily result in a higher node count minimum.

For more information on Deployment configurations, see [Deployment settings](deployment-settings.md).

### Additional improvements

- Added tooltips for [Deployment overview metrics](deployment-metrics.md#deployment-overview) in the Cloud UI.

## July 21, 2022

### Additional improvements

- You can now access an Organization's AWS external ID from the **Settings** tab of the Cloud UI.
- Organizations now need only a single AWS external ID for all clusters. Previously, each cluster required a unique external ID, which added complexity to the installation and cluster creation process.
- You can now remove a user from an Organization from the Cloud UI. See [Remove users from an Organization](manage-organization-users.md#remove-users-from-an-organization).
- Organization Billing Admins can now view task usage for all Workspaces regardless of their Workspace permissions.

## July 14, 2022

### Additional improvements

- The Cloud UI **Clusters** page now includes the cluster ID value.
- Organization Owners and Organization Billing Admins can now update the Organization name in the Cloud UI **Settings** page.
- The Cloud UI **Analytics** page can now show data for the last 30 minutes.

### Bug fixes

- When you change **Worker Resources** for a Deployment in the Cloud UI, any errors related to your worker size request are now based on the correct node instance type that your cluster is running.
- When you select a Workspace and click **Go back** in a browser, the page now reloads as expected.
- A **Page not found** error message no longer appears when you select a Deployment in the **Usage** page of the Cloud UI.
- The **Deployment Analytics** page now displays the correct date.
- Deprecated versions of Astro Runtime now appear correctly in the Deployment page of the Cloud UI. Previously, versions were appended with `-deprecated`.

## June 30, 2022

### New Google Cloud Platform regions

You can now [create an Astro cluster on GCP](manage-hybrid-clusters.md#create-a-cluster) in the following regions:

- `asia-northeast1` (Tokyo)
- `asia-northeast2` (Osaka)
- `asia-northeast3` (Seoul)
- `asia-south1` (Mumbai)
- `europe-central2` (Warsaw)
- `europe-west6` (Zurich)
- `northamerica-northeast1` (Montreal)
- `us-west3` (Salt Lake City)

For a list of all Google Cloud Platform (GCP) regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp-hybrid.md#gcp-region).

### Additional improvements

- You can now search for Organization members by name, email address, and role in the **People** tab of the Organization view in the Cloud UI. You can also search for members in the **Access** tab of the Workspace view.

### Bug fixes

- Fixed an issue where you could not use the KubernetesPodOperator to execute tasks in a Kubernetes cluster outside of your Astro cluster. See [KubernetesPodOperator](https://docs.astronomer.io/astro/kubernetespodoperator).

## June 23, 2022

### New Google Cloud Platform regions

You can now [create an Astro cluster on GCP](manage-hybrid-clusters.md#create-a-cluster) in the following regions:

- `asia-southeast1` (Singapore)
- `australia-southeast1` (Sydney)
- `europe-west1` (Belgium)
- `europe-west2` (England)
- `europe-west3` (Frankfurt)
- `southamerica-east1` (São Paulo)
- `us-west2` (Los Angeles)
- `us-west4` (Nevada)

For a list of all GCP regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp-hybrid.md#gcp-region).

## June 16, 2022

### Submit Support Requests in the Cloud UI

Support requests can now be created and submitted in the Cloud UI. You no longer need to open an account on the Astronomer support portal to reach the Astronomer team. To streamline the request process, the **Submit Support Request** form auto-populates your currently selected Workspace and Deployment in the Cloud UI.

![Location of the "Submit Support Request" button in the Cloud UI](/img/release-notes/support-form.png)

### Parallelism Now Autoscales with a Deployment's Worker Count

To better scale concurrent task runs, Astro now dynamically calculates [`parallelism`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is an Airflow configuration that determines the maximum number of tasks that can run concurrently within a single Deployment.

A Deployment's `parallelism` is now equal to the current number of workers multiplied by the [`worker_concurrency`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) value. This change ensures that your task runs won't be limited by a static parallelism limit as workers autoscale in your Deployment. See [Worker Autoscaling Logic](celery-executor.md#celery-worker-autoscaling-logic) for more information.

Note that you can still use a static `parallelism` value by setting `AIRFLOW__CORE__PARALLELISM` as an [environment variable](environment-variables.md).

### Bug Fixes

- Fixed a rare issue where some user emails would be associated with the wrong username.
- Fixed an issue where you could not properly sort entries in the **People** tab by name.

## June 9, 2022

### Update Deployment configurations with the Astro CLI

You can now programmatically update the configurations for your Astro Deployments using Deployment API keys and the Astro CLI. Updating a Deployment with an API key doesn't require manual user authentication, meaning that you can now add Deployment configuration steps to automated processes such as CI/CD pipelines.

Specifically, you can now run the following commands with Deployment API keys:

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment update`](cli/astro-deployment-update.md)
- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)

### Bug fixes

- Fixed an issue where a Deployment's logs wouldn't load in the Cloud UI if it was the only Deployment in the Workspace

## June 2, 2022

### Support for the `us-east4` GCP region

You can now [create an Astro cluster on GCP](manage-hybrid-clusters.md#create-a-cluster) in the `us-east4` region, which is located in northern Virginia, USA.

For a list of all GCP regions that Astro supports, see [GCP Resource Reference](resource-reference-gcp-hybrid.md#gcp-region).

## May 26, 2022

### New Datasets page in the Cloud UI

You can now use the new **Datasets** page in the **Lineage** tab to view a table of datasets that your DAGs have read or written to. This information can help you quickly identify dataset dependencies and data pipeline access requirements.

![Datasets page](/img/release-notes/datasets-page.png)

Click the name of a dataset to show its lineage graph. For more information, see [Data lineage on Astro](data-lineage.md#view-recently-accessed-datasets).

### Bug fixes

- Fixed an issue where the **Astro Runtime** field of the Cloud UI listed the running version as **Unknown**  for Deployments using an unsupported version of Astro Runtime

## May 5, 2022

### Data lineage Is now available on Astro

We are excited to introduce data lineage to Astro. You now have access to a new **Lineage** view in the Cloud UI that visualizes data movement across datasets in your Organization based on integrations with Airflow, Apache Spark, dbt, Great Expectations, and more.

Built around the [OpenLineage](https://openlineage.io/) open source standard, the data lineage graphs and metadata in the Cloud UI can help you better understand your ecosystem and diagnose issues that may otherwise be difficult to identify.

![Lineage graph example](/img/release-notes/lineage-example.png)

For example, if an Airflow task failed because the schema of a database changed, you might go to the Lineage page on Astro to determine which job caused that change and which downstream tasks failed because of it.

To learn more about data lineage and how you can configure it on Astro, see:

- [Integrate Airflow and OpenLineage](https://docs.astronomer.io/learn/airflow-openlineage)
- [Enable data lineage for External Services](set-up-data-lineage.md)
- [Data lineage on Astro](data-lineage.md)
- [OpenLineage Compatibility Matrix](https://openlineage.io/docs/integrations/about#capability-matrix)

:::info

This functionality is still early access and under active development. If you have any questions or feedback about this feature, reach out to [Astronomer support](https://cloud.astronomer.io/support).

:::

### Support for Astro on Google Cloud Platform (GCP)

Astro now officially supports Astro clusters on Google Cloud Platform (GCP). This includes support for an initial set of GCP regions as well as [Workload Identity](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) for secure connection to other GCP data services in your ecosystem.

For more information about the installation process and supported configurations, see [Install Astro on GCP](install-gcp-hybrid.md) and [Resource Reference GCP](resource-reference-gcp-hybrid.md).

### Support for Organization-Level user invites

You can now [invite users to an Astro Organization](manage-organization-users.md#add-a-user-to-an-organization) without having to first invite them to a specific Workspace. Users invited to an Organization will receive an activation email which brings them directly to the Organization view of the Cloud UI.

### Additional improvements

- Improved the templated emails sent out for user invites with clear instructions for how to get started on Astro
- Improved error messaging behavior on the **DAGs** and **Usage** pages of the Cloud UI
- New user accounts must now be verified via email before they can access Astro

## April 28, 2022

### New AWS node instance types available

To widen our support for various use cases and levels of scale, we've expanded the types of AWS node instances that are supported on Astro. You can now create clusters with:

- [General Purpose M6i instances](https://aws.amazon.com/ec2/instance-types/m6i/)
- [Compute Optimized C6i instances](https://aws.amazon.com/ec2/instance-types/c6i/)
- [Memory Optimized R6i instances](https://aws.amazon.com/ec2/instance-types/r6i/)

For a full list of node instance types that are supported on Astro, see [Resources required for Astro on AWS](resource-reference-aws-hybrid.md#node-instance-type). To modify an existing Astro cluster to use any of these instance types, see [Modify a Cluster](manage-hybrid-clusters.md).

### Additional improvements

- Improve the error message that renders in the Cloud UI if you try to create a worker that is too large for the Deployment's node instance type to support. This error message now specifies a clear call to action

## April 21, 2022

### Feedback in Cloud UI on worker size limits

The Cloud UI now renders an error if you try to modify the **Worker Resources** to a combination of CPU and memory that is not supported by the node instance type of the cluster that the Deployment is hosted on. This validation ensures that the worker size you request is supported by the infrastructure available in your Astro cluster, and minimizes silent task failures that might have occurred due to invalid resource requests.

If your Astro cluster is configured with the `m5d.8xlarge` node type, for example, the Cloud UI will show an error if you try to set **Worker Resources** to 350 AU. This is because the maximum worker size an `m5d.8xlarge` node can support is 307 AU.

![Worker size error](/img/release-notes/worker-size-error.png)

For a reference of all node instance types Astro supports and their corresponding worker size limits, see [Resources required for Astro on AWS](resource-reference-aws-hybrid.md#node-instance-type), [Resources required for Astro on Azure](resource-reference-azure-hybrid.md#node-instance-type), or  [Resources required for Astro on GCP](resource-reference-gcp-hybrid.md#node-instance-type).

## April 14, 2022

### Additional improvements

- The data plane now connects to various AWS services via [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-services-overview.html). This ensures that traffic to AWS services is kept private and does not traverse the NAT and Internet gateways, reducing the risk of exposing your resources to the internet.

### Bug fixes

- Fixed an issue where you could not add a new user to a Workspace if the user had an email address that contained uppercase characters

## March 31, 2022

### New analytics page in Cloud UI to monitor Deployments

The Cloud UI now includes a dedicated **Analytics** page that contains various Deployment-level metrics. These metrics are collected in real time and can provide insight into how your data pipelines are performing over time:

![Analytics menu location](/img/release-notes/access-analytics.png)

For more information about accessing the **Analytics** page and the available metrics, see [Deployment Analytics](deployment-metrics.md#deployment-analytics).

### Lineage backend upgrade scheduled for all Organizations

As part of [Astronomer's acquisition of Datakin](https://www.astronomer.io/blog/astronomer-acquires-datakin-the-data-lineage-tool/), data lineage features are coming soon to Astro. The first step in enabling these features is to implement lineage backends for existing Astro customers.

Starting on March 31st and continuing over the next couple of weeks, all Astro Deployments on Runtime 4.2.0+ will be upgraded to emit lineage events. As a result of this change, you might start seeing lineage-related scheduler logs such as the following:

```text
[2022-03-30, 12:17:39 UTC] {great_expectations_extractor.py:17} INFO - Did not find great_expectations_provider library or failed to import it
[2022-03-24, 23:40:01 UTC] {client.py:74} INFO - Constructing openlineage client to send events to https://api.astro-astronomer.datakin.com
```

A few additional notes about this upgrade:

- You can ignore any lineage logs that indicate an error or failed process, such as the first line in the example logs above. These logs will more accurately reflect the state of your lineage functionality once lineage features are launched on Astro.
- Deployments on Runtime 4.2.0+ will be updated to emit data lineage events only after you [push code](deploy-code.md). Until you do so, this change will not be applied.
- Because Astronomer is upgrading each customer individually over time, the exact date that you will start seeing these logs will vary.
- When you push code to a Deployment on Runtime 4.2.0+ and trigger this update, all other Deployments on Runtime 4.2.0+ in the same Workspace will also restart in order to receive the lineage backend update. If you plan to push code to any Deployment affected by this change, then we recommend doing so at a time where you can tolerate some Airflow components restarting. For more information about expected behavior, see [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

For more information about what to expect when lineage tools go live, read Astronomer's [OpenLineage and Airflow guide](https://docs.astronomer.io/learn/airflow-openlineage).

### New AWS regions available

You can now [create new Clusters](manage-hybrid-clusters.md#create-a-cluster) in:

- `af-south-1` (Cape Town)
- `ap-east-1` (Hong Kong)
- `ap-northeast-3` (Osaka)  
- `me-south-1` (Bahrain)

For a full list of AWS regions supported on Astro, see [Resources required for Astro on AWS](resource-reference-aws-hybrid.md#aws-region).

### Additional improvements

- The Cloud UI now includes a button that links to Astronomer [support](https://support.astronomer.io/) and [status](https://status.astronomer.io/) pages:

    ![Runtime Tag banner](/img/release-notes/support-button.png)

## March 25, 2022

### Maximum node count is now configurable per Cluster

As of this release, **Maximum Node Count** is now a configurable setting for new and existing clusters. On Astro, maximum node count represents the total number of EC2 nodes that your cluster can support at any given time. For an Astro cluster on AWS, EC2 nodes are the primary unit of infrastructure required to run a Deployment and its components, including workers and the Airflow scheduler. New clusters have a maximum node count of 20 by default, but the setting can be modified to any value from 2 to 100 at any time.

Previously, maximum node count was a fixed, global setting that applied to all customers on Astro and could not be configured per cluster. Now, your organization can modify this setting as your workloads evolve and more Deployments are created. Once the limit is reached, your cluster will not be able to auto-scale and worker pods may fail to schedule.

To update this setting for an existing cluster, reach out to [Astronomer support](https://cloud.astronomer.io/support) and provide the name of your cluster and the desired maximum node count.

### Additional improvements

- In **Resource Settings**, the maximum allowed value for **Worker Resources** has been increased to 400 AU.

## March 17, 2022

### Export task usage as a CSV file

In the Cloud UI, you can now export your task usage data from the **Usage** tab as a CSV file to perform more complex data analysis related to your Airflow usage and costs. For example, you can use the file as the basis for a pivot table that shows total task usage by Workspace.

To export your task usage data as a CSV file, click the **Export** button in the **Usage** tab:

![Export as CSV button in Usage tab](/img/release-notes/csv-file.png)

### Bug fixes

- Fixed an issue where saving new environment variables in the Cloud UI would occasionally fail

## March 10, 2022

### Running Docker image tag in Airflow UI

The Docker image that is running on the Airflow webserver of your Deployment is now shown as a tag in the footer of the Airflow UI. Depending on how your team deploys to Astro, this tag is either a unique identifier generated by a CI tool or a timestamp generated by the Astro CLI on `astro deploy`. Both represent a unique version of your Astro project.

![Runtime Tag banner](/img/docs/image-tag-airflow-ui-astro.png)

When you push code to a Deployment on Astro via the Astro CLI or CI/CD, reference this tag in the Airflow UI to verify that your changes were successfully applied.

This feature requires Astro Runtime [4.0.10+](runtime-release-notes.md#4010). To upgrade a Deployment to the latest Runtime version, see [Upgrade Runtime](upgrade-runtime.md).

:::info

While it is a good proxy, the tag shown in the Airflow UI does not forcibly represent the Docker image that is running on your Deployment's scheduler, triggerer, or workers.

This value is also distinct from the **Docker Image** that is shown in the Deployment view of the Cloud UI, which displays the image tag as specified in the Cloud API request that is triggered on `astro deploy`. The image tag in the Airflow UI can be interpreted to be a more accurate proxy to what is running on all components of your Deployment.

If you ever have trouble verifying a code push to a Deployment on Astro, reach out to [Astronomer support](https://cloud.astronomer.io/support).

:::

## March 3, 2022

### Additional improvements

- The threshold in order for bars in the **Worker CPU** and **Worker Memory** charts to appear red has been reduced from 95% to 90%. This is to make sure that you get an earlier warning if your workers are close to hitting their resource limits.

### Bug fixes

- Fixed an issue where malformed URLs prevented users from accessing the Airflow UI of some Deployments on Astro
- Fixed an issue where Astro Runtime 4.0.11 wasn't a selectable version in the **Astro Runtime** menu of the Deployment creation view in the Cloud UI

## February 24, 2022

### Bug fixes

- Removed the **Teams** tab from the Cloud UI. This view was not yet functional but coming back soon
- Fixed an issue where the number of users per Workspace displayed in the Organization view of the Cloud UI was incorrect
- Fixed an issue where if a secret environment value was updated in the Cloud UI and no other values were modified, the change was not applied to the Deployment

## February 17, 2022

### Introducing Astro and a new look

This week's release introduces a reimagined Astronomer brand that embraces **Astro** as a rename of Astronomer Cloud. The rebrand includes a new Astronomer logo, color palette, and font.

![New branding](/img/release-notes/new-branding.png)

The new Astronomer brand is now reflected both in the [Cloud UI](https://cloud.astronomer.io) as well as in the main [Astronomer website](https://astronomer.io) and [documentation](https://docs.astronomer.io).

In addition to visual changes, we've renamed the following high-level Astro components:

- **Astronomer Cloud CLI** is now **Astro CLI**
- **Astronomer UI** is now **Cloud UI**
- **Astro Runtime** is now **Astro Runtime**

We hope you find this exciting. We're thrilled.

### New Organization roles for users

The following Organization-level roles are now supported on Astro:

- **Organization Member**: This role can view Organization details and membership. This includes everything in the **People**, **Clusters**, and **Settings** page of the Cloud UI. Organization members can create new Workspaces and invite new users to an Organization.
- **Organization Billing Admin:** This role has all of the Organization Member's permissions, plus the ability to manage Organization-level settings and billing. Organization Billing Admins can access the **Usage** tab of the Cloud UI and view all Workspaces across the Organization.
- **Organization Owner:** This role has all of the Organization Billing Admin's permissions, plus the ability to manage and modify anything within the entire Organization. This includes Deployments, Workspaces, Clusters, and users. Organization Owners have Workspace Admin permissions to all Workspaces within the Organization.

Organization roles can be updated by an Organization Owner in the **People** tab of the Cloud UI. For more information about these roles, see [User permissions](user-permissions.md).

### Create new Workspaces from the Cloud UI

All users can now create a new Workspace directly from the **Overview** tab of the Cloud UI:

![Create Workspace button](/img/release-notes/add-workspace.png)

When you create a new Workspace, you will automatically become a Workspace Admin within it and can create Deployments. For more information about managing Workspaces, see [Manage Workspaces](manage-workspaces.md).

### Bug fixes

- Fixed an issue where authentication tokens to Astro weren't properly applied when accessing the Airflow UI for a Deployment. This would result in an authenticated user seeing `Error: Cannot find this astro cloud user` in the Airflow UI.
- Fixed an issue where long environment variable values would spill out of the **Value** column and onto the **Updated** column in the **Environment Variables** view of a Deployment in the Cloud UI.

## February 11, 2022

### Monitor DAG runs across all Deployments in a Workspace

You can view key metrics about recent DAG runs through the new **DAGs** page in the Cloud UI. Use this page to view DAG runs at a glance, including successes and failures, across all Deployments in a given Workspace. You can also drill down to a specific DAG and see metrics about its recent runs.

![DAGs page](/img/docs/dags-page.png)

For more information about the **DAGs** page, see [Deployment metrics](deployment-metrics.md#dag-runs).

### Additional improvements

- All resource settings in the Deployment view of the Astronomer UI now show exact CPU and Memory usage to the right of every slider, previously shown only in Astronomer Units (AUs). This makes it easy to know exactly how many resources you allocate to each component.
- A banner now appears in the Astronomer UI if a Deployment is running a version of Astro Runtime that is no longer maintained. To make the most of features and bug fixes, we encourage users to upgrade to recent versions as much as possible.
- Added more ways to sort pages that utilize card views, such as the **Deployments** page
- Added user account avatars next to usernames in several places across the Cloud UI

### Bug fixes

- Removed the **Environment** field from the Deployment view of the Astronomer UI. This field is not currently functional and will be re-added as soon as it is.

## February 3, 2022

### Support for third-party identity providers

You can now integrate both Azure AD and Okta as identity providers (IdPs) for federated authentication on Astro. By setting up a third-party identity provider, a user in your organization will be automatically logged in to Astro if they're already logged in via your IdP. By adding new Astro users through your IdP's own user management system, Workspace Admins can automatically add new users to their Workspace without those users needing to individually sign up for Astro.

For more information about this feature read [Set up an identity provider](configure-idp.md).

### Support for the Astro CLI

The Astro CLI (`astro`) is now generally available as the official command-line tool for Astro. It is a direct replacement of the previously released `astro` executable and comes with various significant improvements. We encourage all customers to upgrade.

For more information on the Astro CLI, see [CLI Release Notes](cli/release-notes.md). For install instructions, read [Install the CLI](cli/install-cli.md).

### Multiple authentication methods for a single user account

Astro now supports multiple authentication methods for a single user account. This means that as long as you're using a consistent email address, you now have the flexibility to authenticate with GitHub, Google, username/password, and/or [an external identity provider (idP)](configure-idp.md) at any time. Previously, a single user account could only be associated with one authentication method, which could not be changed after the account was created.

This also means that all Organizations now have GitHub, Google, and username/password authentication methods enabled by default for all users.

### Additional improvements

- Changed the default RDS instance type for new clusters from `db.r5.xlarge` to `db.r5.large`, which represents a monthly cost reduction of ~50% for newly provisioned clusters. Customers with existing clusters will need to request a downscale via [Astronomer support](https://cloud.astronomer.io/support)

## January 13, 2022

### Identity-based login flow

Astro now utilizes an identity-based login flow for all users. When you first log in via the Cloud UI, you now only need to enter the email address for your account. Astro assumes your Organization and brings you directly to your Astro Organization's login screen.

This change serves as a foundation for future SSO and authentication features. In upcoming releases, users will be able to authenticate via custom identity providers like Okta and Azure Active Directory.

### Additional improvements

- Significant improvements to the load times of various Cloud UI pages and elements.
- In the Cloud UI, the tooltips in the **Resource Settings** section of a Deployment's page now show the definition of 1 AU. This should make it easier to translate AU to CPU and Memory.
- Scheduler logs in the Cloud UI no longer show `DEBUG`-level logs.
- To ensure that all workers have enough resources to run basic workloads, you can no longer allocate less than 10 AU to **Worker Resources**.

## January 6, 2022

### Improvements to "Scheduler Logs" in the Cloud UI

The **Scheduler Logs** tab in the Cloud UI has been updated to make logs easier to read, separate, and parse. Specifically:

- You can now filter logs by type (`DEBUG`, `INFO`, `WARN`, and `ERROR`).
- The page now shows logs for the past 24 hours instead of the past 30 minutes.
- The page now shows a maximum of 500 logs instead of a lower maximum.
- When looking at a Deployment's logs, you can return to the Deployment's information using the **Deployment Details** button.

![Logs page in the UI](/img/release-notes/log-improvements.png)

### Removal of worker termination grace period

The **Worker Termination Grace Period** setting is no longer available in the Cloud UI or API. Previously, users could set this to anywhere between 1 minute and 24 hours per Deployment. This was to prevent running tasks from being interrupted by a code push. Today, however, existing Celery workers don't have to terminate in order for new workers to spin up and start executing tasks. Instead, existing workers will continue to execute running tasks while a new set of workers gets spun up concurrently to start executing the most recent code.

To simplify Deployment configuration and reflect current functionality:

- The worker Termination Grace Period was removed from the Cloud UI
- This value was permanently set to 24 hours for all Deployments on Astro

This does not change or affect execution behavior for new or existing Deployments. For more information, read [What Happens During a Code Deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Additional improvements

- Removed _Kubernetes Version_ column from the **Clusters** table. This value was previously inaccurate and is not needed. The Kubernetes version of any particular Astro cluster is set and modified exclusively by Astro as part of our managed service.

## December 16, 2021

### View scheduler error logs from the Cloud UI

The new **Logs** tab in the Cloud UI shows scheduler error and warning logs for all Deployments in your Workspace. When you select a Deployment in this menu, all error logs generated over the last 30 minutes appear in the UI.

![Logs page in the UI](/img/release-notes/logs-page.png)

To access logs directly for a given Deployment, click the new **Logs** button on the Deployment's page or in the **Deployments** table.

![Logging direct access button](/img/release-notes/logs-button.png)

For more information on how to view logs, read [View logs](view-logs.md).

### Bug fixes

Fixed various bugs in the Cloud UI to better handle nulls and unknowns in Deployment metrics

## December 9, 2021

### Additional improvements

- In the Cloud UI, the **Open Airflow** button now shows more specific status messages when a Deployment's Airflow UI is inaccessible.

### Bug fixes

- Fixed Deployment table scrolling and alignment issues in the UI

## December 6, 2021

### New "Usage" tab in the Cloud UI

Total task volume for your Organization is now available in a new **Usage** tab in the Cloud UI. Astro is priced based on successful task runs, so this view can help you monitor both Astro cost as well as Airflow usage in aggregate and between Deployments.

![Usage tab in the Cloud UI](/img/docs/usage.png)

For more information about the **Usage** tab, read [Deployment metrics](deployment-metrics.md#usage).

### New AWS regions available

You can now create new clusters in:

- `us-west-1`
- `ap-northeast-1`
- `ap-southeast-1`
- `ap-northeast-2`
- `ap-southeast-2`
- `ap-south-1`
- `us-west-1`
- `us-west-2`

For a full list of AWS regions supported on Astro, see [Resources required for Astro on AWS](https://docs.astronomer.io/resource-reference-aws#aws-region).

### Additional improvements

- You can now see your Deployment's **Namespace** in the **Deployments** menu and on the Deployment information screen in the Cloud UI. Namespace is a required argument to run tasks with the KubernetesPodOperator. It is also required to submit an issue to [Astronomer support](https://cloud.astronomer.io/support).

    ![Deployment namespace available on a Deployment's information page](/img/docs/namespace.png)

- The Cloud UI now shows a warning if you attempt to exit Environment Variable configuration without saving your changes.
- A Deployment's health status is now based on the health of both the Airflow webserver and scheduler. Previously, a Deployment's health status was only based on the health of the webserver. Now, the Cloud UI will show that your Deployment is "Healthy" only if both components are running as expected.

### Bug fixes

- The Cloud UI now has error handling for attempts to access a Deployment that does not exist.
- If you attempt to modify an existing secret environment variable, the **Value** field is now blank instead of showing hidden characters.

### Data plane improvements

- Amazon EBS volumes have been upgraded from gp2 to [gp3](https://aws.amazon.com/about-aws/whats-new/2020/12/introducing-new-amazon-ebs-general-purpose-volumes-gp3/) for improved scale and performance.
- EBS volumes and S3 buckets are now encrypted by default.
- The ability to enable public access to any Amazon S3 bucket on an Astro data plane is now blocked per a new AWS account policy. Previously, public access was disabled by default but could be overridden by a user creating a new S3 bucket with public access enabled. This AWS account policy could be overridden by AWS account owners, but Astronomer strongly recommends against doing so.

## November 19, 2021

### Secret environment variables

You can now set secret environment variables via the Cloud UI. The values of secret environment variables are hidden from all users in your Workspace, making them ideal for storing sensitive information related to your Astro projects.

![Secrets checkbox available in the Cloud UI](/img/release-notes/secrets-feature.png)

For more information, read [Set environment variables via the Cloud UI](environment-variables.md#set-environment-variables-via-the-astro-ui).

### Additional improvements

- You can now create new clusters in AWS `sa-east-1`.
- Extra whitespace at the end of any environment variable that is set via the Cloud UI is now automatically removed to ensure the variable is passed correctly.

## November 11, 2021

### Deployment metrics dashboard

In the Cloud UI, your Deployment pages now show high-level metrics for Deployment health and performance over the past 24 hours.

![New metrics in the Cloud UI](/img/docs/deployment-metrics.png)

For more information on this feature, read [Deployment metrics](deployment-metrics.md).

### Bug fixes

- Resolved a security vulnerability by setting `AIRFLOW__WEBSERVER__COOKIE_SECURE=True` as a global environment variable

## November 5, 2021

### Bug fixes

- Fixed an issue where a new user could not exit the Cloud UI "Welcome" screen if they hadn't yet been invited to a Workspace

## October 29, 2021

### Cloud UI redesign

The Cloud UI has been redesigned so that you can more intuitively manage Organizations, Workspaces, and your user profile.

To start, the homepage is now a global view. From here, you can now see all Workspaces that you have access to, as well as information and settings related to your **Organization**: a collection of specific users, teams, and Workspaces. Many features related to Organizations are coming soon, but the UI now better represents how Organizations are structured and what you can do with them in the future:

![New global menu in the UI](/img/docs/ui-release-note1.png)

You can now also select specific Workspaces to work in. When you click in to a Workspace, you'll notice the left menu bar is now entirely dedicated to Workspace actions:

- The Rocket icon brings you to the **Deployments** menu.
- The People icon brings you to the **Workspace Access** menu.
- The Gear icon brings you to the **Workspace Settings** menu.

To return to the global menu, you can either click the Astro "A" or click the Workspace name to produce a dropdown menu with your Organization.

![New Workspace menu in the UI](/img/docs/ui-release-note2.png)

All user configurations can be found by clicking your user profile picture in the upper right corner of the UI. From the dropdown menu that appears, you can both configure user settings and access other Astronomer resources such as documentation and the Astronomer Registry.

![New profile menu in the UI](/img/docs/ui-release-note3.png)

### Additional improvements

- You can now create new clusters in `us-east-2` and `ca-central-1`.
- In the Deployment detail page, **Astro Runtime** now shows the version of Apache Airflow that the Deployment's Astro Runtime version is based on.
- You can now create or modify an existing Astro cluster to run any size of the `t2`,`t3`, `m5`, or `m5d` [AWS EC2 instances](resource-reference-aws-hybrid.md).

### Bug fixes

- Fixed an issue where a new Deployment's health status did not update unless you refreshed the Cloud UI

## October 28, 2021

### Bug fixes

- Fixed an issue where you couldn't push code to Astro with a Deployment API key via a CI/CD process
- Fixed an issue where you couldn't update or delete an API key after creating it

## October 25, 2021

### Additional improvements

- When deleting a Deployment via the UI, you now have to type the name of the Deployment in order to confirm its deletion.

### Bug fixes

- Fixed an issue where you could not access Airflow's REST API with a Deployment API key
- Fixed an issue where calling the `imageDeploy` API mutation with a Deployment API key would result in an error

## October 15, 2021

### Additional improvements

- When creating a new Deployment, you can now select only the latest patch version for each major version of Astro Runtime.
- When creating a new Deployment in the Cloud UI, the cluster is pre-selected if there is only one cluster available.
- The name of your Astro Deployment now appears on the main DAGs view of the Airflow UI.
- You can now see the health status for each Deployment in your Workspace on the table view of the **Deployments** page in the Cloud UI:

   ![Deployment Health statuses visible in the Deployments table view](/img/release-notes/health-status-table.png)

- In the Cloud UI, you can now access the Airflow UI for Deployments via the **Deployments** page's card view:

    ![Open Airflow button in the Deployments page card view](/img/docs/open-airflow-card.png)

- The Cloud UI now saves your color mode preference.

## October 1, 2021

### Additional improvements

- In the Cloud UI, the **Open Airflow** button is now disabled until the Airflow UI of the Deployment is available.
- Workspace Admins can now edit user permissions and remove users within a given Workspace.

## September 28, 2021

:::danger

This release introduces a breaking change to code deploys via the Astro CLI. Starting on September 28, you must upgrade to v1.0.0+ of the CLI to deploy code to Astro. [CI/CD processes](set-up-ci-cd.md) enabled by Deployment API keys will continue to work and will not be affected. For more information, read the [CLI release notes](cli/release-notes.md).

:::

### Additional improvements

- In the Cloud UI, a new element on the Deployment information screen shows the health status of a Deployment. Currently, a Deployment is considered unhealthy if the Airflow webserver is not running and the Airflow UI is not available:

    ![Deployment Health text in the UI](/img/docs/deployment-health.png)

- The documentation home for Astro has been moved to `docs.astronomer.io`, and you no longer need a password to access the page.

### Bug fixes

- The Cloud UI now correctly renders a Deployment's running version of Astro Runtime.

## September 17, 2021

### Support for Deployment API keys

Astro now officially supports Deployment API keys, which you can use to automate code pushes to Astro and integrate your environment with a CI/CD tool such as GitHub Actions. For more information on creating and managing Deployment API keys, see [Deployment API keys](api-keys.md). For more information on using Deployment API keys to programmatically deploy code, see [CI/CD](set-up-ci-cd.md). Support for making requests to Airflow's REST API using API keys is coming soon.

## September 3, 2021

### Bug fixes

- Added new protections to prevent S3 remote logging connections from breaking
- Fixed an issue where environment variables with extra spaces could break a Deployment
- Fixed an issue where Deployments would occasionally persist after being deleted via the UI
- In the UI, the **Organization** tab in **Settings** is now hidden from non-admin users
- In the UI, the table view of Deployments no longer shows patch information in a Deployment's **Version** value

## August 27, 2021

### Additional improvements

- You can now remain authenticated to Astro across multiple active browser tabs. For example, if your session expires and you re-authenticate to Astro on one tab, all other tabs running Astro will be automatically updated without refreshing.
- If you try to access a given page on Astro while unauthenticated and reach the login screen, logging in now brings you to the original page you requested.

### Bug fixes

- Fixed an issue where an incorrect total number of team members would appear in the **People** tab

## August 20, 2021

### Support for the Airflow REST API

You can now programmatically trigger DAGs and update your Deployments on Astro by making requests to Airflow's [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html). Currently this feature works only with temporary tokens, which are available at `cloud.astronomer.io/token`. Support for Deployment API keys is coming soon. For more information on using this feature, read [Airflow API](airflow-api.md).

### Additional improvements

- Set `AIRFLOW_HOME = 'usr/local/airflow'` as a permanent global environment variable
- In the Cloud UI, long environment variable keys and values now wrap to fit the screen
- Added links for the Astronomer Registry and certification courses to the left-hand navbar
- Moved the **Teams** and **People** tabs into the **Settings** page of the UI
- Added **Cluster** information to the metadata section of a Deployment's information page in the UI
- Renamed various UI elements to better represent their functionality
- Increased the maximum **Worker Termination Grace Period** from 600 minutes (10 hours) to 1440 minutes (24 hours)

### Bug fixes

- The left-hand navbar in the UI is no longer cut off when minimized on smaller screens
- Fixed an issue where you could not delete a Workspace via the UI
- Fixed an issue where expired tokens would occasionally appear on `cloud.astronomer.io/token`
- Fixed an issue where the UI would initially load an inaccurate number of team members on the **Access** page
- Fixed alphabetical sorting by name in the **People** tab in the UI
- Removed placeholder columns from various tables in the UI

## August 6, 2021

### Additional improvements

- Informational tooltips are now available on the **New Deployment** page.

### Bug fixes

- Fixed an issue where adding a user to a Workspace and then deleting the user from Astro made it impossible to create new Deployments in that Workspace
- Improved error handling in the Airflow UI in cases where a user does not exist or does not have permission to view a Deployment

## July 30, 2021

### Improvements

- Increased the limit of **Worker Resources** from 30 AU to 175 AU (17.5 CPU, 65.625 GB RAM). If your tasks require this many resources, reach out to us to make sure that your cluster is sized appropriately
- Collapsed the **People** and **Teams** tabs on the left-hand navigation bar into a single **Access** tab
- Added a **Cluster** field to the Deployments tab in the Cloud UI. Now, you can reference which cluster each of your Deployments is in
- Replaced our white "A" favicon to one that supports color mode
- Informational tooltips are now available in **Deployment Configuration**

### Bug fixes

- Fixed an issue where a deleted user could not sign up to Astro again
- Removed Deployment-level user roles from the Cloud UI. Support for them coming soon
- Fixed an issue where a newly created Deployment wouldn't show up on the list of Deployments in the Workspace
