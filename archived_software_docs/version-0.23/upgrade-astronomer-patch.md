---
title: 'Upgrade to a Patch Version of Astronomer Software'
sidebar_label: 'Upgrade to a Patch Version'
id: upgrade-astronomer-stable
---

## Overview

For Astronomer Software customers, new product features are regularly made available in stable and long-term support (LTS) releases as described in [Release and Lifecycle Policy](release-lifecycle-policy.md). Patch versions of Astronomer Software with additional bug and security fixes are also released on a regular basis.

All stable and patch releases of Astronomer Software require a simple upgrade process. When an [LTS version](release-lifecycle-policy.md#release-channels) is released, additional upgrade guidance specific to that version will be made available.

Follow this guide to upgrade to any stable or patch version of Astronomer Software. For information on new features and changes, refer to [Software Release Notes](release-notes.md).

A few notes before you get started:
- The following guidelines are only for upgrading to the latest Astronomer v0.23 patch version. To determine whether the latest version of Astronomer is a minor or patch version, read the Astronomer Platform Versioning guidelines below.
- The patch upgrade process will NOT affect running Apache Airflow® tasks as long as `upgradeDeployments.enabled=false` is set in the script below.
- Patch version updates will NOT cause any downtime to Astronomer services (Software UI, Houston API, Astronomer CLI).

> **Note:** Astronomer v0.16.5 and beyond includes an improved upgrade process that allows Apache Airflow® Deployments to remain unaffected through a platform upgrade that includes changes to the [Astronomer Apache Airflow® Chart](https://github.com/astronomer/airflow-chart).
>
> Now, Airflow Chart changes only take effect when another restart event is triggered by a user (e.g. a code push, Environment Variable change, resource or executor adjustment, etc).

## Astronomer Platform Versioning

Astronomer platform releases follow a semantic versioning scheme. All versions are written as a 3-component number in the format of `x.y.z`. In this syntax,

- X: Major Version
- Y: Minor Version
- Z: Patch/Hotfix

For example, upgrading Astronomer from v0.16.4 to v0.16.5 would be considered upgrading to a patch version, whereas upgrading from v0.15.0 to v0.16.0 would be considered upgrading to the latest minor version.

## Step 1: Ensure You Have a Copy of Your Astronomer config.yaml File

First, ensure you have a copy of the `config.yaml` file of your platform namespace if you don't already.

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

## Step 3: Run Astronomer's Patch Upgrade Script

Now, review and run the script below to upgrade to the patch version of your choice.

Make sure to substitute the following 3 variables with your own values:

- `RELEASE_NAME`
- `NAMESPACE`
- `ASTRO_VERSION`

```sh
#!/bin/bash
set -xe

RELEASE_NAME=<astronomer-platform-release-name>
NAMESPACE=<astronomer-platform-namespace>
ASTRO_VERSION=0.23.<astronomer-patch-version>

helm3 repo add astronomer https://helm.astronomer.io
helm3 repo update

# upgradeDeployments false ensures that Apache Airflow® charts are not upgraded when this script is ran
# If you deployed a config change that is intended to reconfigure something inside Airflow,
# then you may set this value to "true" instead. When it is "true", then each Airflow chart will
# restart.
helm3 upgrade --namespace $NAMESPACE \
            -f ./config.yaml \
            --reset-values \
            --version $ASTRO_VERSION \
            --set astronomer.houston.upgradeDeployments.enabled=false \
            $RELEASE_NAME \
            astronomer/astronomer
```

> **Note:** If you do not specify a patch version above, the script will automatically pull the latest Astronomer Software patch available in the [Astronomer Helm Chart](https://github.com/astronomer/astronomer/releases). If you set `ASTRO_VERSION=0.23` and `--version 0.23`, for example, Astronomer v0.23.9 will be installed if it is the latest v0.23 patch available.
