---
title: "Upgrade to Astronomer Enterprise v0.25"
sidebar_label: "Upgrade to v0.25"
id: upgrade-to-0-25
description: "How to upgrade the Astronomer Enterprise Platform."
---

## Overview

Astronomer releases are made generally available to Enterprise customers on a quarterly basis as part of a long-term support (LTS) release model.

This guide provides steps for upgrading your Astronomer Enterprise platform from v0.23.x to [v0.25](release-notes.md), which is the latest available LTS release.

A few important notes before you start:

- You must be on Astronomer Enterprise v0.23.x in order to upgrade to Astronomer v0.25+. If you are running a version of Astronomer that's lower than v0.23, submit a request to [Astronomer Support](https://support.astronomer.io) and our team will help you define an alternate upgrade path.
- The guidelines below only apply to users who are upgrading to the Astronomer v0.25 series for the first time. Once you've completed the upgrade to any v0.25 version, you'll be free to upgrade to subsequent v0.25.x patch versions as they are released by our team. For instructions, read [Upgrade to a Patch Version](upgrade-astronomer-stable.md).

## Step 1: Check Version Compatibility

Ensure that the following software is updated to the appropriate version:

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

## Step 2: Check Permissions

Minor version upgrades can be initiated only by a user with System Admin permissions on Astronomer. To confirm you're an Astronomer SysAdmin, confirm that you have access to **System Admin** features in the Astronomer UI:

![Admin](https://assets2.astronomer.io/main/docs/enterprise_quickstart/admin_panel.png)

You also need permission to create Kubernetes resources. To confirm you have those permissions, run the following commands:

```sh
kubectl auth can-i create pods --namespace <your-astronomer-namespace>
kubectl auth can-i create sa --namespace <your-astronomer-namespace>
kubectl auth can-i create jobs --namespace <your-astronomer-namespace>
```

If all commands return `yes`, then you have the appropriate Kubernetes permissions.

## Step 3: Backup Your Database

Backup your entire Astronomer database instance using your cloud provider's functionality for doing so, or make a backup request to your database administrator based on your organization's guidelines.

## Step 4: Check the Status of Your Kubernetes Pods

Before you proceed with the upgrade, ensure that the Kubernetes Pods in your platform namespace are healthy. To do so, run:

```
kubectl get pods -n <your-astronomer-namespace>
```

All pods should be in either the `Running` or `Completed` state. If any of your pods are in a `CrashLoopBackOff` state or are otherwise unhealthy, make sure that's expected behavior before you proceed.

## Step 5: Switch to Your Default Namespace

Switch to the default namespace in your Kubernetes context by running the following command:

```sh
kubectl config set-context --current --namespace=default
```

## Step 6: Upgrade Astronomer

Run the following command to begin the upgrade process:

```sh
kubectl apply -f https://raw.githubusercontent.com/astronomer/astronomer/release-0.25/migrations/scripts/lts-to-lts/0.23-to-0.25/manifests/upgrade-0.23-to-0.25.yaml
```

While your platform is upgrading, monitor your pods to ensure that no errors occur. To do so, first find the names of your pods by running the following command:

```sh
kubectl get pods | grep upgrade-astronomer
```

Then, run the following command for each pod you find:

```sh
kubectl logs <your-pod-name>
```

## Step 7: Confirm That the Upgrade Was Successful

If the upgrade was successful, you should be able to:

* Log in to Astronomer at `https://app.BASEDOMAIN`.
* See Workspaces and Airflow Deployments in the Astronomer UI.
* Access the **Settings** tab for each of your Deployments in the Astronomer UI.
* See metrics on the **Metrics** tab in the Astronomer UI.
* Successfully run `$ astro deploy` using the Astronomer CLI.
* Open the Airflow UI for each of your Deployments
* Access logs for your DAGs in the Airflow UI.

## Step 8: Clean Up Kubernetes Resources

We recommend cleaning up any remaining Kubernetes resources after your upgrade. To do so, run the following command:

```sh
kubectl delete -f https://raw.githubusercontent.com/astronomer/astronomer/release-0.25/migrations/scripts/lts-to-lts/0.23-to-0.25/manifests/upgrade-0.23-to-0.25.yaml
```

## Step 9: Upgrade the Astronomer CLI to v0.25

To ensure reliability and full access to features included in Astronomer Enterprise v0.25, all users must upgrade to v0.25 of the Astronomer CLI. We recommend the latest available version, though you may choose to install a particular patch release within the v0.25 series.

To upgrade to the latest available v0.25 version of the Astronomer CLI, run:

```sh
curl -sSL https://install.astronomer.io | sudo bash -s -- v0.25.0
```

To do so via Homebrew, run:

```sh
brew install astronomer/tap/astro@0.25
```

Earlier versions of the Astronomer CLI are backwards incompatible with Astronomer v0.25. All team members within your organization must upgrade the Astronomer CLI individually before taking any further action on the platform or in a local Airflow environment. For a detailed breakdown of CLI changes between versions, refer to [Astronomer CLI releases](https://github.com/astronomer/astro-cli/releases). For detailed install guidelines and more information on the Astronomer CLI, refer to [Astronomer CLI Quickstart](cli-quickstart.md).

## Roll Back to Enterprise v0.23

If you encounter an issue during your upgrade that requires you to recover your original platform, you can roll back to Astronomer v0.23. To do so:

1. Apply the rollback automation script by running the following command:
```sh
kubectl apply -f https://raw.githubusercontent.com/astronomer/astronomer/release-0.25/migrations/scripts/lts-to-lts/0.23-to-0.25/manifests/rollback-0.23-to-0.25.yaml
```
This restores the platform database and the Helm state of the Astronomer Helm chart.

2. Wait a few minutes for your platform to come back up.

3. Confirm that the rollback completed. To do so, watch your pods until they have stabilized; every pod in your Astronomer namespace should be `Running` with full readiness or `Completed`. You can check the status of your pods using the following command:
```sh
watch kubectl get pods -n <your-astronomer-namespace>
```

4. Clean up any remaining Kubernetes resources after your rollback. To do so, run the following command:
```sh
kubectl delete -f https://raw.githubusercontent.com/astronomer/astronomer/release-0.25/migrations/scripts/lts-to-lts/0.23-to-0.25/manifests/rollback-0.23-to-0.25.yaml
```
