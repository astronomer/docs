---
sidebar_label: 'Migration'
title: 'Migrating to Astro'
id: install-gcp
description: Get started on Astro by creating your first Astro cluster on Google Cloud Platform (GCP).
sidebar_custom_props: { icon: 'img/gcp.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This is where you'll find instructions for migrating to Astro from another managed Airflow environment. This guide will
cover migrating from:

- (GCC) [Google Cloud Composer](https://cloud.google.com/composer/docs/concepts/overview)
- (
  MWAA) [Amazon Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
- Other Astronomer products like Astronomer Nebula

To complete the migration process, you will:

- Create Target Environment in Astro
- Migrate Metadata from your source Airflow
- Migrate DAGs and additional Airflow components
- Complete the *Cutover process*

## Set Up

### Requirements and prerequisites

This process should be undertaken with assistance from your Astronomer Data Engineer, and is intended to be started
after your cluster has been activated. [Networking connectivity](connect-aws.md) should already be established during
activation, and any [IDP should be configured](configure-idp.md) as desired.

### Other requirements

- Access to your Astro organization and the [ability to create workspaces](manage-workspaces.md)
- `astro` CLI is [installed](cli/install-cli.md) and [configured](log-in-to-astro.md)
    - note: the `astro` CLI requires `docker`)
- Access to source Airflow environment to migrate
    - you can utilize cloud provider CLIs such as `aws` and `gcloud` to expedite some steps in this guide
    - note: You may also need access to a cloud storage bucket utilized by the source environment
- Read access to any source control supporting the source Airflow
- Create access for new source control repositories for your new Astro Airflow
- Access to Secrets Backend credentials, _if in use in the source Airflow_
- Administrative access to create new CI/CD, _if in use in the source Airflow_

### Not supported 

This process supports Airflow 2.x. Your source Airflow will need to be upgraded prior to migration if they are in the
Airflow 1.x series, and Astronomer Professional services can help that process

## Prepare Source and Target Environments

### Install Astronomer Starship to Source Airflow

On the selected source Airflow environment, install
the [Astronomer Starship](https://pypi.org/project/astronomer-starship/) migration utility.

This utility will connect to both your source and target Airflow instances to migrate Airflow Connections,
Variables, and assist in migrating your DAGs between instances.

The Starship migration utility can either function as an Airflow Plugin with a user interface, or an Airflow operator if you are migrating from a more restricted Airflow environment. Please refer to the table below for compatability:


#### Starship Compatability Matrix
| Source Airflow      | [Starship Plugin](https://github.com/astronomer/starship/tree/master/astronomer-starship) | Starship Operator |
| --- | --- | --- |
| Airflow 1.x | ❌ | ❌ |
| GCC 1 - Airflow 2.x |  | ✅ |
| GCC 2 - Airflow 2.x | ✅ |  |
| MWAA v2.0.2 |  | ✅ |
| MWAA v2.2.2 | ✅ |  |
| OSS Airflow VM | ✅ |  |
| Astronomer Nebula  | ✅ |  |
| Astronomer Software | ✅ |  |

#### Installation 
<Tabs defaultValue="plugin" values="{[{label: 'MWAA', value: 'mwaa'}, {label: 'Cloud Composer', value: 'gcc'}]}" >
<TabItem value="mwaa">
To install `astronomer-starship` to your MWAA instance, you'll need to edit the `requirements.txt` file in your S3 Bucket. You can find more [detailed instructions here.](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-dependencies.html#best-practices-dependencies-different-ways).

You'll want to add `astronomer-starship` on a new line, in your `requirements.txt` file, then re-upload the file to your S3 bucket, and edit your Airflow Environment to refer to the new version of this file.
</TabItem>
<TabItem value="gcc">
::: caution 

[//]: # (TODO )
https://cloud.google.com/composer/docs/composer-2/install-python-dependencies

:::
</TabItem>
</Tabs>

We will cover usage of the Starship migration utility later in this document

[//]: # (TODO )
### Create Astro Workspace
- Create Workspaces in the Astro UI
- Add users and set permissions accordingly

### Create Astro Deployment
Create Target deployments in the recently created workspace in Astro UI with the Astro CLI using `astro deployment create`
  - Mirror deployment settings from source in terms of number of schedulers, min/max workers, size

See [Create a Deployment](create-deployment.md).

## Migrate Airflow Metadata
### Migrate Airflow Metadata with Starship from Source Environment
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
    
    <aside>
    💡 At this point, understand the `Dockerfile` and it’s purpose, modification beyond setting the version will not be needed in these migrations.
    
    </aside>
    
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
