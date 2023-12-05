---
title: 'Upgrade Astronomer Software'
sidebar_label: 'Upgrade Astronomer'
id: upgrade-astronomer
description: Upgrade to a new LTS, stable, or patch version of Astronomer Software.
---

## Overview

For Astronomer Software customers, new product features are regularly made available in stable and long-term support (LTS) releases as described in [Release and Lifecycle Policy](release-lifecycle-policy.md). Patch versions of Astronomer Software with additional bug and security fixes are also released on a regular basis.

Follow this guide to upgrade to any version of Astronomer Software. For information on new features and changes, refer to [Software Release Notes](release-notes.md).

A few notes before you get started:
- The upgrade process will not affect running Airflow tasks as long as `upgradeDeployments.enabled=false` is set in your upgrade script.
- Updates will not cause any downtime to Astronomer services, including the Software UI, the Astro CLI, and the Houston API.

## Step 1: Review Upgrade Considerations

The [Upgrade Considerations](upgrade-astronomer.md#upgrade-considerations) section of this document contains upgrade information for specific Astronomer versions. Review these notes before starting the upgrade process.

## Step 2: Check Permissions

You need Astronomer System Admin permissions to complete version upgrades. To confirm that you're a System Admin, check that you have access to the **System Admin** menu in the Software UI:

![System Admin panel](/img/software/admin_panel.png)

You also need permissions to create Kubernetes resources. To confirm that you have the required permissions, run the following commands:

```sh
kubectl auth can-i create pods --namespace <your-astronomer-namespace>
kubectl auth can-i create sa --namespace <your-astronomer-namespace>
kubectl auth can-i create jobs --namespace <your-astronomer-namespace>
```

If all commands return `yes`, then you have the appropriate Kubernetes permissions.

## Step 3: Back Up Your Database

Before you perform an upgrade, back up your Astronomer database. To create a backup, follow the instructions provided by your cloud provider, or ask your organization's database administrator for assistance.

## Step 4: Check the Status of Your Kubernetes Pods

Then, ensure that all Kubernetes Pods in your Astronomer namespace are healthy by running:

```sh
kubectl get pods -n <your-astronomer-namespace>
```

All Pods should be in either the `Running` or `Completed` state. If any of your Pods are in a `CrashLoopBackOff` state or are otherwise unhealthy, make sure that that is expected behavior before you proceed.

## Step 5: Get a Copy of Your `config.yaml` File and Confirm Values

1. Run the following command to retrieve your current platform configuration:

    ```sh
    helm get values <your-platform-release-name> -n <your-platform-namespace>  > config.yaml
    ```

2. Review this configuration. If you see the line `"USER-SUPPLIED VALUES:"`, delete it.
3. Create a copy of `config.yaml` called `old_config.yaml`. Save this in case you need to roll back your upgrade.

## Step 6: Verify Your Current Platform Version

To verify your current version of Astronomer, run:

```sh
helm list --all-namespaces | grep astronomer
```

## Step 7: Run Astronomer's Upgrade Script

Review and run the script below to upgrade to the version of your choice.

```sh
#!/bin/bash
set -xe

RELEASE_NAME=<astronomer-platform-release-name>
NAMESPACE=<astronomer-platform-namespace>
ASTRO_VERSION=<astronomer-version>

helm3 repo add astronomer https://helm.astronomer.io
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

Make sure to substitute the following 3 variables with your own values:

- `<astronomer-platform-release-name>`
- `<astronomer-platform-namespace>`
- `<astronomer-patch-version>`

To upgrade to Astronomer Software v0.27.0, for example, set `ASTRO_VERSION=0.27.0`.

:::tip

If you do not specify a patch version above, the script will automatically pull the latest Astronomer Software patch available in the [Astronomer Helm Chart](https://github.com/astronomer/astronomer/releases). If you set `ASTRO_VERSION=0.26` for example, Astronomer v0.26.5 will be installed if it is the latest v0.26 patch available.

:::

## Step 8: Confirm That the Installation Was Successful

If the upgrade was successful, you should be able to:

- Log in to Astronomer at `https://app.<BASEDOMAIN>`.
- See Workspaces and Airflow Deployments in the Software UI.
- Access the **Settings** tab for each of your Deployments in the Software UI.
- See metrics on the **Metrics** tab in the Software UI.
- Run `$ astro deploy` for an existing Deployment using the Astro CLI.
- Open the Airflow UI for each of your Deployments.
- Access task logs for your DAGs in the Airflow UI.
- Create a new Airflow Deployment that is healthy.

If there is a problem creating a new Airflow Deployment, check the commander logs to troubleshoot. Here is an example of what to look for:

```
2022-04-14T05:10:45 INFO Calling commander method #updateDeployment
2022-04-14T05:10:48 INFO Response from #updateDeployment: {"result":{"message":"values don't meet the specifications of the schema(s) in the following chart(s):\nairflow:\ ... },"deployment":{}}
2022-04-14T05:10:48 INFO Deployment some-deployment successfully updated

```

Make changes as needed and rerun the upgrade command from Step 7. Do not continue to Step 8 until you have successfully created a new Airflow Deployment.

## Upgrade Considerations

This topic contains information about upgrading to specific versions of Astronomer Software. This includes notes on breaking changes, database migrations, and other considerations that might depend on your use case.

### Upgrading to 0.29

:::danger

If you are currently on Astronomer Software 0.25, 0.26, or 0.27, you must upgrade to version 0.28 before upgrading to 0.29. A direct upgrade to 0.29 from a version lower than 0.28 is not possible.

Follow the standard installation guide to upgrade to Software 0.28, then repeat the process to upgrade to 0.29.

:::

#### Resync Astronomer's Signing Certificate  

As part of the 0.29 release, Astronomer deprecated its usage of [kubed](https://appscode.com/products/kubed/) for performance and security reasons. Kubed was responsible for syncing Astronomer's signing certificate to Deployment namespaces and is now replaced by an in-house utility. While this change does not directly affect users, you need to run a one-time command to reset Astronomer's signing certificate as part of the upgrade process to 0.29.

When upgrading to 0.29 from any earlier minor version, run the following command between Steps 2 and 3 in the standard procedure to annotate the certificate secret:

```bash
kubectl -n <your-platform-namespace> annotate secret astronomer-houston-jwt-signing-certificate "astronomer.io/commander-sync"="platform=astronomer"
```

If you upgraded to Astronomer Software 0.29 without annotating this secret, you can still complete the sync by running the following command after the upgrade:

```bash
kubectl create job -n <release-namespace> --from=cronjob/astronomer-config-syncer upgrade-config-synchronization
```

### Upgrading to Astronomer Software 0.28

#### Version Compatibility

Before upgrading to Astronomer Software 0.28, ensure that the following tools are running compatible versions:

- **Kubernetes**: Your version must be 1.19 or greater. If you need to upgrade Kubernetes, contact your cloud provider or your Kubernetes administrator.
- **Airflow Images**: You must be using an Astronomer Certified Airflow image, and the version of your image must be 1.10.15 or greater.

    For example, all of the following images would work for this upgrade:

    - `quay.io/astronomer/ap-airflow:1.10.15-7-buster`
    - `quay.io/astronomer/ap-airflow:2.0.0-3-buster-onbuild`
    - `quay.io/astronomer/ap-airflow:2.0.2-buster-onbuild`
    - `quay.io/astronomer/ap-airflow:2.2.2-onbuild`

- **Helm**: Your version must be 3.6 ≤ 3.8.

#### Modify `config.yaml` values

During Step 5 of the upgrade process, check your `config.yaml` file to see if you have any configuration listed under `astronomer.houston.config.deployments.helm`. You must update all key-value pairs in this section to be under `astronomer.houston.config.deployments.helm.airflow` instead.

For example, consider an existing `config.yaml` file that includes an override of `webserver.allowPodLogReading`:

```yaml
astronomer:
  houston:
    config:
      deployments:
        helm:
          webserver:
            allowPodLogReading: true
```

In this case, you need to modify the configuration to include an `airflow` key after `helm`:

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

Once you complete this change, compare any values under the `airflow` section with the [default values from airflow-chart](https://github.com/astronomer/airflow-chart/blob/master/values.yaml) and [open source Airflow chart](https://github.com/apache/airflow/blob/main/chart/values.yaml) to ensure that they are formatted correctly. Incorrectly formatted values for these configurations might result in an error during upgrade.

### Upgrading to Astronomer Software 0.25

#### Version Compatibility

Before upgrading to 0.25, ensure that the following software is updated to the appropriate version:

- **Astronomer**: Your current Software version must be at least v0.23.
- **Kubernetes**: Your version must be 1.17 or 1.18. If you need to upgrade Kubernetes, contact your cloud provider's support or your Kubernetes administrator.
- **Airflow Images**: You must be using an Astronomer Certified Airflow image, and the version of your image must be 1.10.5 or greater. In addition, your image should be in the following format:

    ```
    quay.io/astronomer/ap-airflow:<airflow-version>-<build-number>-<distribution>-onbuild
    ```

    For example, all of the following images would work for this upgrade:

    ```sh
    quay.io/astronomer/ap-airflow:1.10.10-5-alpine3.10-onbuild
    quay.io/astronomer/ap-airflow:2.0.0-3-buster-onbuild
    quay.io/astronomer/ap-airflow:2.0.2-buster-onbuild
    quay.io/astronomer/ap-airflow:1.10.5-9-buster
    ```

    > **Note:** While `-onbuild` and `<build-number>` are optional, we recommend including them for most upgrades. If you have your own build, test, and publish workflows that are layered on top of the Astronomer Airflow images, then removing `<build-number>` is appropriate because images including `<build-number>` are immutable.

- **Helm**: Your version must be 3.6 or greater.

#### Change to Upgrade Script

Upgrading to 0.25 requires a non-standard upgrade script. Ignore Step 4 in the standard upgrade process and run the following command instead:

```sh
kubectl apply -f https://raw.githubusercontent.com/astronomer/astronomer/v0.25.15-final/migrations/scripts/lts-to-lts/0.23-to-0.25/manifests/upgrade-0.23-to-0.25.yaml
```
