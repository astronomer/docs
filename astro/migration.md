---
sidebar_label: 'Migrating to Astro'
title: 'Migrating to Astro'
id: migration
description: Get started on Astro by migrating your Airflow instance from Google Cloud Composer or Amazon Managed Workflows for Apache Airflow
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This is where you'll find instructions for migrating to Astro from another managed Airflow environment. This guide will
cover migrating an Airflow Instance from:

- [Google Cloud Composer (GCC)](https://cloud.google.com/composer/docs/concepts/overview)
- [Amazon Managed Workflows for Apache Airflow (MWAA)](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
- Other Astronomer products like Astronomer Nebula

The process for migrating from OSS Airflow that you host yourself can be similar, but more complicated, and it is advised that you work directly
with your Astronomer Data Engineer or Astronomer Professional Services for these migrations for further instruction.

To complete the migration process, you will:

- Prepare your source Airflow environment and setup your Astro Airflow environment
- Migrate Metadata from your source Airflow environment
- Migrate DAGs and additional Airflow components
- Complete the *Cutover process*

## Prerequisites
This process should be undertaken with assistance from your Astronomer Data Engineer, and these steps should be started 
after your cluster has been activated. [Networking connectivity](connect-aws.md) should already be established during
activation, and an [IDP should already be configured](configure-idp.md) if it is desired. Contact your Astronomer 
representative if this is not the case.

### Requirements

To complete this guide, you will need:
- Access to your Astro organization and the [ability to create workspaces](manage-workspaces.md)
- `astro` CLI is [installed](cli/install-cli.md) and [configured](log-in-to-astro.md)
    - *note that* the `astro` CLI requires a functional `docker` installation
- Access to the source Airflow environment to migrate
    - you can utilize cloud provider CLIs such as `aws` and `gcloud` to expedite some steps in this guide
    - *note that* you may also need access to a cloud storage bucket utilized by the source environment
- Read access to any source control supporting your source Airflow environment (e.g. Github)
- Create access for new source control repositories for your new Astro Airflow
- Access to Secrets Backend credentials, *if in use in the source Airflow*
- Administrative access to create new CI/CD, *if in use in the source Airflow*

### Not supported 

This process supports **Airflow 2.x**. Your source Airflow environment will need to be upgraded prior to migration 
if they are in the **Airflow 1.x** series, and Astronomer Professional services can help you with that process.

:::caution

How do we not have a link for this???

:::

## Prepare Source and Target Environments

### Step 1: Install Astronomer Starship to Source Airflow

On the selected source Airflow environment, install
the [Astronomer Starship](https://pypi.org/project/astronomer-starship/) migration utility.

This utility will connect to both your source and Astro Airflow deployment to migrate Airflow Connections,
Variables, and assist in migrating your DAGs between instances.

The Starship migration utility can either function as a
[plugin](https://github.com/astronomer/starship/tree/master/astronomer-starship) with a user interface, 
or an Airflow operator if you are migrating from a more restricted Airflow environment. 

Please refer to the table below for compatability:

#### Starship Compatability Matrix

| Source Airflow      | Starship Plugin | Starship Operator |
|---------------------|-----------------|-------------------|
| Airflow 1.x         | ❌               | ❌                 |
| GCC 1 - Airflow 2.x |                 | ☑️                |
| GCC 2 - Airflow 2.x | ☑️              |                   |
| MWAA v2.0.2         |                 | ☑️                |
| MWAA v2.2.2         | ☑️              |                   |
| OSS Airflow VM      | ☑️              |                   |
| Astronomer Nebula   | ☑️              |                   |
| Astronomer Software | ☑️              |                   |

#### Installation 

<Tabs defaultValue="mwaa" groupId="installation" values="{[ {label: 'MWAA', value: 'mwaa'}, {label: 'Cloud Composer', value: 'gcc'} ]}">
<TabItem value="mwaa">
To install Starship to your MWAA instance, you'll need to edit the `requirements.txt` file in your S3 Bucket. 
You can find more [detailed instructions here.](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-dependencies.html#best-practices-dependencies-different-ways)
You'll want to add `astronomer-starship` on a new line, in your `requirements.txt` file, then re-upload the file to your S3 bucket, 
and edit your Airflow Environment to refer to the new version of this file.

:::cli
You can accomplish this easily with the `aws` CLI, in a terminal:
```sh
# Modify these values:
export MWAA_NAME=<MWAA>
export MWAA_BUCKET=<MWAA BUCKET>
aws s3 cp "s3://$MWAA_BUCKET/requirements.txt" requirements.txt
echo 'astronomer-starship' >> requirements.txt
aws s3 cp requirements.txt s3://<MWAA BUCKET>/requirements.txt
aws mwaa update-environment $MWAA_NAME --requirements-s3-object-version=""$(aws s3api head-object --bucket=$MWAA_BUCKET --key=requirements.txt --query="VersionId")""
```
:::
</TabItem>
<TabItem value="gcc">
To install Starship to your Cloud Composer 1 or Cloud Composer 2 instance, you'll modify your instance's `PYPI Packages` tab.
There you can add `astronomer-starship` as an entry by clicking `Edit`.
You can find more [detailed instructions here.](https://cloud.google.com/composer/docs/composer-2/install-python-dependencies)

:::cli
You can accomplish this easily with the `gcloud` CLI, in a terminal:
```sh
# Modify this value:
export GCC_NAME=<GCC_NAME>
gcloud composer environments update $GCC_NAME --update-pypi-package=astronomer-starship
```
:::
</TabItem>
</Tabs>

We will cover usage of the Starship migration utility later in this document

### Step 2: Create Astro Workspace

Astro has Workspaces - which are collections of Deployments that can be accessed by a specific group of users. 

You can [read this document](manage-workspaces.md) that goes into more detail about creating workspaces with the Astro UI

Afterwards, make sure to [add users](add-user.md) to your new Workspace, and [refer to this document](user-permissions.md) 
for details on user permissions.

To complete this step - create a workspace to hold your migrated Airflow Deployments.

### Step 3: Create Astro Deployment

Deployments in Astro are your Airflow Environments. There are a number of strategies and considerations while creating 
your Astro Deployment that will mirror your migration environment.

You will want to retrieve the following information from your source Airflow Environment:

- Name
- Airflow Version
- Environment Class or Size
- Number of Schedulers
- Minimum Number of Workers
- Maximum Number of Workers
- Execution Role Permissions
- Airflow Configuration modifications
- Environment Variables

:::info
A mapping of Astronomer Runtime releases to Airflow versions is available [in the Release Notes](https://docs.astronomer.io/astro/release-notes)
This table is included as a quick but potentially incomplete reference. 
Where exact version matches are not available, the nearest version was picked.

| Airflow Version | Runtime Version  |
|-----------------|------------------|
| 2.0.2           | 3.0.4 (AF 2.1.1) |
| 2.2.2           | 4.2.9 (AF 2.2.5) |
| 2.4.3           | 6.3.0            |
:::

:::info
Scheduler size is measured in AUs, our recommended equivalents are:

|        | AUs |
|--------|-----|
| Small  | 5   |
| Medium | 10  |
| Large  | 15  |
:::

:::note
You will likely only have one instance type associated with your cluster at this point, later on in the process you can 
[add other instance types](modify-cluster#manage-worker-types).
:::

You can create your Deployment in the Astro UI or Astro CLI.

<Tabs defaultValue="ui" groupId="deployment" values="{[ {label: 'Option 1: Astro UI', value: 'ui'}, {label: 'Option 2: Astro CLI, Deployments-as-Code', value: 'cli'} ]}">
<TabItem value="ui">
To create your target Astro Deployment, refer to [Create a Deployment](create-deployment.md) and [Configure Deployment Resources](configure-deployment-resources.md).
1) **Name your Deployment** to match your existing environment, optionally give it a description
2) Pick the **Cluster** that was previously activated with your Astronomer Representative
3) Select the appropriate **Astronomer Runtime** version
4) Set your **Worker Type**, if available, or pick the default
5) Ensure you set your **Worker Count** minimum and maximum values are set, per the source environment
6) Ensure the **number of Schedulers** is set, per the source environment
7) Adjust the **Scheduler Size**, roughly approximate to the source environment Size by converting to AUs based on the reference above
8) After creating your Deployment - you can add [Environment Variables](environment-variables.md) in the `Variables` Tab of your new Deployment
9) You can set Airflow Configuration variables as [Environment Variables](environment-variables.md) in the `Variables` Tab of your new Deployment
10) Set the [Alert Email](configure-deployment-resources#add-or-delete-a-deployment-alert-email) to your email address, or a good contact for the Airflow instance
</TabItem>
<TabItem value="cli">
To create your target Astro Deployment via the CLI, refer to [Manage Deployments as code](manage-deployments-as-code). 
We will begin by creating a file called `config.yaml` in a new directory.
Fill it with the following:
```yaml
deployment:
    environment_variables:
        - is_secret: false 
          key: FOO 
          value: BAR
    configuration:
        name: [NAME]
        description: [DESCRIPTION]
        runtime_version: [RUNTIME VERSION]
        dag_deploy_enabled: true
        scheduler_au: [SCHEDULER AU]
        scheduler_count: [NUM SCHEDULERS]
        cluster_name: [CLUSTER NAME] 
        workspace_name: [WORKSPACE NAME] 
    worker_queues:
        - name: default
          max_worker_count: [MAX WORKER COUNT] 
          min_worker_count: [MIN WORKER COUNT]
          worker_concurrency: 16
          worker_type: [WORKER TYPE]
    alert_emails:
        - [ALERT EMAIL] 
```
1) **Name your Deployment** to match your existing environment by replacing `[NAME]`, optionally replace `[DESCRIPTION]`
2) Replace `[CLUSTER]` with the name of the **Cluster** that was previously activated with your Astronomer Representative
3) Select the appropriate **Astronomer Runtime** version for `[RUNTIME VERSION]`
4) Set your **Worker Type** in `[WORKER TYPE]` by picking the default, unless you have already [added other instance types](modify-cluster#manage-worker-types)
:::info
The default instance type for a new cluster are: 
| AWS       | GCP           | AZ              |
|-----------|---------------|-----------------|
| M5.XLARGE | E2-STANDARD-4 | STANDARD_D4D_V5 |
A more complete reference is available in the [Cluster Settings Reference](resource-reference-aws.md) pages.
:::
5) Ensure you set your **Worker Count** minimum with `[MIN WORKER COUNT]` and maximum with `[MAX WORKER COUNT]`, per the source environment
6) Ensure the **number of Schedulers** is set on `[NUM SCHEDULERS]`, per the source environment
7) Adjust the **Scheduler Size**, roughly approximate to the source environment Size by converting to AUs based on the reference above
8) Add [Environment Variables](environment-variables.md) `environment_variables` section. 
9) You can set Airflow Configuration variables as [Environment Variables](environment-variables.md) in the `environment_variables` section.
10) Set `[ALERT EMAIL]` to your email address, or a good contact for the Airflow instance. More information [here](configure-deployment-resources#add-or-delete-a-deployment-alert-email)
After you have finished creating `config.yaml` file, you can create the deployment with:
```shell
astro deployment create --deployment-file config.yaml
```
</TabItem>
</Tabs>

## Migrate Airflow Metadata

### Step 4: Migrate Airflow Metadata with Starship from Source Environment

- Migrate Connections
- Migrate Variables
- Test connections via Starship when possible
- Migrate Env Variables
    - Note: not all Env Vars are [configurable on Astro](https://docs.astronomer.io/astro/platform-variables)
- Create pools, as needed

## Migrate DAGs 
### Initialize new repository skeleton
1. Using the same name as the chosen environment, create a new directory for your project
2. Initialize a git repository with `git init`, using the git CLI and/or your Source Control Tool’s UI
3. Initialize the Astro Project with `astro dev init`

### Copy core Airflow code
1. Copy `/dags` folder from source control or blob storage
2. Edit `Dockerfile` to match Astro Runtime version to customer’s Source environment Airflow version
    - Some Airflow versions are not supported - lowest supported version is Airflow 2.2.x
    - Reference runtime release notes [here](https://docs.astronomer.io/astro/runtime-release-notes) to determine which Airflow version corresponds with which runtime version
    
    💡 At this point, understand the `Dockerfile` and it’s purpose, modification beyond setting the version will not be needed in these migrations.
    
3. Add `requirements.txt` , as needed.

### Copy accessory Airflow code
Following recommended [project structure](https://docs.astronomer.io/learn/managing-airflow-code#project-structure):

- Copy `/plugins` folder from source control or blob storage, as needed

### Configure Additional Components
- Add CICD if already being used in Source environment
- Add Secrets Backend if already being used in Source environment
- Add Trust Policies between Astro and Cloud Roles, as needed.

### Test locally and check for import errors
Test the environment locally with the CLI using `astro dev parse`  and `astro dev start` - inspect errors in the CLI and/or the localhost webserver

### Deploy
Deploy with astro deploy 

## Test and Cutover
### **Test and Cutover**
- Confirm successful migration of connections & variables in Target environment
- Validate and test DAGs in Target environment
- Utilize Starship in Source Environment to pause DAGs in Source and unpause DAGs in Target
### **Tune instance**
- Monitor analytics as DAGs turn on
- Add new instance types to match worker size from source
- Add any intentionally set Airflow Configuration settings
    - Note: not all configurations are [configurable on Astro](https://docs.astronomer.io/astro/platform-variables)
- Add `DAGs-only Deployment` , if desired
### Continue and repeat
- Customer continues to **Test and Cutover DAGs** on Astro with support from Astro Data Engineers via Slack, engaging in additional calls, as needed.
- Repeat Migration for all Environments after initial airflow environment is fully migrated
