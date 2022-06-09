---
title: 'Upgrade to a Stable or Patch Version of Astronomer Software'
sidebar_label: 'Upgrade Astronomer'
id: upgrade-astronomer-stable
description: Upgrade to a new stable or patch version of Astronomer Software.
---

## Overview

For Astronomer Software customers, new product features are regularly made available in stable and long-term support (LTS) releases as described in [Release and Lifecycle Policy](release-lifecycle-policy.md). Patch versions of Astronomer Software with additional bug and security fixes are also released on a regular basis.

Follow this guide to upgrade to any stable or patch version of Astronomer Software. For information on new features and changes, refer to [Software Release Notes](release-notes.md).

A few notes before you get started:
- The upgrade process will not affect running Airflow tasks as long as `upgradeDeployments.enabled=false` is set in your upgrade script.
- Updates will not cause any downtime to Astronomer services, including the Software UI, the Astro CLI, and the Houston API.

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

To upgrade to Astronomer Software v0.27.0, for example, set `ASTRO_VERSION=0.27.0`.

:::tip

If you do not specify a patch version above, the script will automatically pull the latest Astronomer Software patch available in the [Astronomer Helm Chart](https://github.com/astronomer/astronomer/releases). If you set `ASTRO_VERSION=0.26` for example, Astronomer v0.26.5 will be installed if it is the latest v0.26 patch available.

:::

## Upgrade Considerations

This topic contains information about upgrading to specific versions of Astronomer Software. This includes notes on breaking changes, database migrations, and other considerations that might depend on your use case.

### Upgrading from Earlier Minor Versions to 0.29

As part of the 0.29 release, Astronomer has deprecated its usage of [kubed](https://appscode.com/products/kubed/) for performance and security reasons. Kubed was responsible for syncing Astronomer's signing certificate to Deployment namespaces and is now replaced by an in-house utility. While this change does not directly affect users, you need to run a one-time command during upgrade in order to sync Astronomer's signing certificate.

When upgrading to v0.29 from any earlier minor version, complete the following additional setup between Steps 2 and 3 in the standard procedure:

1. Locate your Astronomer Software `config.yaml`. To retrieve it programmatically, run the following:

    ```bash
    # platform-release-name is usually "astronomer"
    helm get values <your-platform-release-name> astronomer/astronomer -n <your-platform-namespace>
    ```

2. Run the following command to annotate the certificate secret:

    ```bash
    kubectl -n <your-platform-namespace> annotate secret astronomer-houston-jwt-signing-certificate "astronomer.io/commander-sync"="platform=astronomer"
    ```

### Upgrading from Astronomer Software v0.25

If you are upgrading from Astronomer Software v0.25, you first need to upgrade to the latest patch version of v0.26.x before upgrading to any subsequent stable release. To complete this upgrade:

1. Complete the upgrade steps as described in this document. When you get to Step 3, set `ASTRO_VERSION` in Step 3 of this guide to the [latest patch version of Software v0.26](https://docs.astronomer.io/software/0.26/release-notes).
2. Complete the same upgrade process. This time, when you get to Step 3, set `ASTRO_VERSION` to your desired v0.27+ version.
