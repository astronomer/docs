---
title: "Upgrade to Astronomer Software v0.28"
sidebar_label: "Upgrade to v0.28"
id: upgrade-to-0-28
description: "How to upgrade the Astronomer Software Platform."
---

## Overview

Astronomer releases are made generally available to Software customers on a quarterly basis as part of a long-term support (LTS) release model.

This guide provides steps for upgrading your Astronomer Software platform from v0.25.x to v0.28.x, which is the latest available LTS release.

A few important notes before you start:

- In version 0.26+, the the Astronomer airflow chart uses Apache’s airflow chart as a subchart dependency to provide users with access to new Airflow features more quickly. There are some differences in the schema. If you are setting airflow-chart defaults in your `config.yaml`, you will need to make small adjustment to the file. More information below.
- You must be on Astronomer Software v0.25+ in order to upgrade to Astronomer v0.28+. If you are running v0.23, please follow the instructions for [upgrading from v0.23 to v0.25](https://docs.astronomer.io/software/0.25/upgrade-to-0-25). If you are running a version of Astronomer that's lower than v0.23, submit a request to [Astronomer Support](https://support.astronomer.io/) and our team will help you define an alternate upgrade path.
- The guidelines below only apply to users who are upgrading to the Astronomer v0.28 series for the first time. Once you've completed the upgrade to any v0.28 version, you'll be free to upgrade to subsequent v0.28.x patch versions as they are released by our team. For instructions, read [Upgrade to a Patch Version](https://docs.astronomer.io/software/upgrade-astronomer-stable).

## Step 1: Check Version Compatibility

Ensure that the following software is updated to the appropriate version:

- **Kubernetes**: Your version must be 1.19 or greater. If you need to upgrade Kubernetes, contact your cloud provider's support or your Kubernetes administrator.
- **Airflow Images**: You must be using an Astronomer Certified Airflow image, and the version of your image must be 1.10.5 or greater. In addition, your image should be in the following format:

    `quay.io/astronomer/ap-airflow:<airflow-version>-<build-number>-<distribution>-onbuild`

    For example, all of the following images would work for this upgrade:

    `quay.io/astronomer/ap-airflow:2.0.0-3-buster-onbuild`

    `quay.io/astronomer/ap-airflow:2.0.2-buster-onbuild`

    `quay.io/astronomer/ap-airflow:``1.10.15-7-buster`

    > Note: While -onbuild and <build-number> are optional, we recommend including them for most upgrades. If you have your own build, test, and publish workflows that are layered on top of the Astronomer Airflow images, then removing <build-number> is appropriate because images including <build-number> are immutable.
    >
- **Helm**: Your version must be 3.6 ≤ 3.8.

## Step 2: Check Permissions

Minor version upgrades can be initiated only by a user with System Admin permissions on Astronomer. To confirm you're an Astronomer SysAdmin, confirm that you have access to **System Admin** features in the Software UI:

![https://assets2.astronomer.io/main/docs/enterprise_quickstart/admin_panel.png](https://assets2.astronomer.io/main/docs/enterprise_quickstart/admin_panel.png)

You also need permission to create Kubernetes resources. To confirm you have those permissions, run the following commands:

`kubectl auth can-i create pods --namespace <your-astronomer-namespace>`

`kubectl auth can-i create sa --namespace <your-astronomer-namespace>`

`kubectl auth can-i create jobs --namespace <your-astronomer-namespace>`

If all commands return `yes`, then you have the appropriate Kubernetes permissions.

## Step 3: Backup Your Database

Backup your entire Astronomer database instance using your cloud provider's functionality for doing so, or make a backup request to your database administrator based on your organization's guidelines.

## Step 4: Check the Status of Your Kubernetes Pods

Before you proceed with the upgrade, ensure that the Kubernetes Pods in your platform namespace are healthy. To do so, run:

`kubectl get pods -n <your-astronomer-namespace>`

All pods should be in either the `Running` or `Completed` state. If any of your pods are in a `CrashLoopBackOff` state or are otherwise unhealthy, make sure that's expected behavior before you proceed.

## Step 5: Extract a Copy of Your Astronomer `config.yaml` File And Save Backup

Ensure you have a copy of the `config.yaml` file for your platform namespace.

To do this, you can run:
`helm get values <your-platform-release-name> -n <your-platform-namespace>  > config.yaml`

Review this configuration and delete the line `"USER-SUPPLIED VALUES:"` if you see it.

Create a copy of `config.yaml` called `old_config.yaml`. This should saved in case you need to rollback.

## Step 6: Update Config File (if necessary)

Check your `config.yaml` to see if you have anything listed under `astronomer.houston.config.deployments.helm`. If so, you may need to adjust some values.

For example, this config file is overriding the `webserver.allowPodLogReading` config.

```yaml
astronomer:
  houston:
    config:
      deployments:
        helm:
          webserver:
            allowPodLogReading: true

```

In this example, you will need to add an `airflow` key after `helm`.

```yaml
astronomer:
  houston:
    config:
      deployments:
        helm:
          airflow:  ## added this key as this config is coming from the subchart
            webserver:
              allowPodLogReading: true
```

Most commonly, this is the only change that is needed however you should compare your values with the [default values from airflow-chart](https://github.com/astronomer/airflow-chart/blob/master/values.yaml) and [open-source Airflow chart](https://github.com/apache/airflow/blob/main/chart/values.yaml).

## Step 6: Upgrade Astronomer to v0.28

Run the following script to begin the upgrade process:

```bash
#!/bin/bash
set -xe

RELEASE_NAME=<astronomer-platform-release-name>
NAMESPACE=<astronomer-platform-namespace>
ASTRO_VERSION=0.28

helm3 repo add astronomer [https://helm.astronomer.io](https://helm.astronomer.io/)
helm3 repo update

# upgradeDeployments false ensures that Airflow charts are not upgraded when this script is ran
# If you deployed a config change that is intended to reconfigure something inside Airflow,
# then you may set this value to "true" instead. When it is "true", then each Airflow chart will
# restart. Note that some stable version upgrades require setting this value to true regardless of your own configuration.

helm3 upgrade --namespace $NAMESPACE \
-f ./config.yaml \
--reset-values \
--version $ASTRO_VERSION \
--set astronomer.houston.upgradeDeployments.enabled=false \
$RELEASE_NAME \
astronomer/astronomer
```

While your platform is upgrading, monitor your pods to ensure that no errors occur. To do so, first find the names of your pods by running the following command:

`kubectl get pods | grep upgrade-astronomer`

Then, run the following command for each pod you find:

`kubectl logs <your-pod-name>`

## Step 7: Confirm That the Upgrade to 0.28 Was Successful

If the upgrade was successful, you should be able to:

- Log in to Astronomer at `https://app.BASEDOMAIN`.
- See Workspaces and Airflow Deployments in the Software UI.
- Access the **Settings** tab for each of your Deployments in the Software UI.
- See metrics on the **Metrics** tab in the Software UI.
- Successfully run `$ astro deploy` using the Astronomer CLI.
- Open the Airflow UI for each of your Deployments
- Access logs for your DAGs in the Airflow UI.
- Create a new Airflow Deployment and ensure it comes up healthy

If there is a problem when creating your Airflow Deployment, check the commander logs for references. Here is an example of what you will be looking for:

```
2022-04-14T05:10:45 INFO Calling commander method #updateDeployment
2022-04-14T05:10:48 INFO Response from #updateDeployment: {"result":{"message":"values don't meet the specifications of the schema(s) in the following chart(s):\nairflow:\ ... },"deployment":{}}
2022-04-14T05:10:48 INFO Deployment some-deployment successfully updated

```

Make corrections as needed, and rerun the upgrade command from Step 6. Do not continue to Step 8 until you have successfully created a new Airflow Deployment.

## Step 8: Upgrade the Astronomer CLI to v0.28

To ensure reliability and full access to features included in Astronomer Software v0.28, all users must upgrade to v0.28 of the Astronomer CLI. We recommend the latest available version, though you may choose to install a particular patch release within the v0.28 series.

To upgrade to the latest available v0.28 version of the Astronomer CLI, run:

`curl -sSL https://install.astronomer.io | sudo bash -s -- v0.28.0`

To do so via Homebrew, run:

`brew install astronomer/tap/astro@0.28`

Earlier versions of the Astronomer CLI are backwards incompatible with Astronomer v0.28. All team members within your organization must upgrade the Astronomer CLI individually before taking any further action on the platform or in a local Airflow environment. For a detailed breakdown of CLI changes between versions, refer to [Astronomer CLI releases](https://github.com/astronomer/astro-cli/releases). For detailed install guidelines and more information on the Astronomer CLI, refer to [Astronomer CLI Quickstart](https://docs.astronomer.io/software/0.25/cli-quickstart).

## Roll Back to Software v0.25

If you encounter an issue during your upgrade that requires you to recover your original platform, you can roll back to Astronomer v0.25 by restoring the Astronomer database from the backup from Step 3. After restoring, the configs will be the ones from you backup `config.yaml` from Step 5. If you need to make any config changes after for 0.25.x or are reattempting the upgrade, please use the backup `config.yaml` as the base.
