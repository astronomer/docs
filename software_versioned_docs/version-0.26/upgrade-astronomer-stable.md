---
title: 'Upgrade to a Stable or Patch Version of Astronomer Software'
sidebar_label: 'Upgrade Astronomer'
id: upgrade-astronomer-stable
description: Upgrade to a new stable or patch version of Astronomer Software.
---

## Overview

For Astronomer Software customers, new product features are regularly made available in stable and long-term support (LTS) releases as described in [Release and Lifecycle Policy](release-lifecycle-policy.md). Patch versions of Astronomer Software with additional bug and security fixes are also released on a regular basis.

All stable and patch releases of Astronomer Software require a simple upgrade process. When an [LTS version](release-lifecycle-policy.md#release-channels) is released, additional upgrade guidance specific to that version will be made available.

Follow this guide to upgrade to any stable or patch version of Astronomer Software. For information on new features and changes, refer to [Software Release Notes](release-notes.md).

A few notes before you get started:
- The patch upgrade process will not affect running Airflow tasks as long as `upgradeDeployments.enabled=false` is set in the script below.
- Patch and stable version updates will not cause any downtime to Astronomer services, including the Software UI, the Astronomer CLI, and the Houston API.

:::info

Astronomer v0.16.5 and beyond includes an improved upgrade process that allows Airflow Deployments to remain unaffected through a platform upgrade that includes changes to the [Astronomer Airflow Chart](https://github.com/astronomer/airflow-chart).

Now, Airflow Chart changes only take effect when another restart event is triggered by a user (e.g. a code push, Environment Variable change, resource or executor adjustment, etc).

:::

:::caution

If you are upgrading from Astronomer Software v0.25, you first need to upgrade to the latest patch version of v0.26.x before upgrading to any subsequent stable release. To complete this upgrade:

1. Complete the upgrade steps as described in this document. When you get to Step 3, set `ASTRO_VERSION` in Step 3 of this guide to the [latest patch version of Software v0.26](https://docs.astronomer.io/software/0.26/release-notes).
2. Complete the same upgrade process. This time, when you get to Step 3, set `ASTRO_VERSION` to your desired v0.27+ version.

:::

## Step 1: Ensure You Have a Copy of Your Astronomer `config.yaml` File

First, ensure you have a copy of the `config.yaml` file of your platform namespace.

To do this, you can run:

```sh
helm get values <your-platform-release-name> -n <your-platform-namespace>  > config.yaml
```

Review this configuration and delete the line `"USER-SUPPLIED VALUES:"` if you see it.

## Step 2: Verify Your Current Platform Version

To verify the version of Astronomer you're currently operating with, run:

```sh
helm list --all-namespaces | grep astronomer
```

## Step 3: Run Astronomer's Upgrade Script

Now, review and run the script below to upgrade to the version of your choice.

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

To upgrade to Astronomer Software v0.26.5, for example, set `ASTRO_VERSION=0.26.5`.

:::tip

If you do not specify a patch version above, the script will automatically pull the latest Astronomer Software patch available in the [Astronomer Helm Chart](https://github.com/astronomer/astronomer/releases). If you set `ASTRO_VERSION=0.26`, for example, Astronomer v0.26.5 will be installed if it is the latest v0.26 patch available.

:::
