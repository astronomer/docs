---
title: 'Configure Pre-Created Kubernetes Namespaces for Astronomer Software'
sidebar_label: 'Pre-Create Namespaces'
id: pre-create-namespaces
---

## Overview

This document provides steps for using pre-created Kubernetes namespaces for Deployments. Pre-created namespaces provide more control over how new Deployments are created.

Once you create a Deployment using a given pre-created namespace, that namespace is unavailable until the Deployment has been deleted. If no pre-created namespaces are available, then no new Deployments can be created on your platform.

You might want to configure this feature to limit the number of active Deployments in a given installation, or to indicate ownership of a specific Deployment to a given department in your organization.

## Prerequisites

Deploying code to a platform with pre-created namespaces requires an Astronomer CLI version of 0.25.5 or higher.

## Enable Pre-Created Namespaces

To give users access to pre-created namespaces, you first need to create the namespaces, enable the feature, and specify your created namespaces in your platform configuration. The namespaces you specify will be available for every Workspace and Deployment on your platform.

To start using pre-created namespaces:

1. Create all of the namespaces you plan to use as described in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/#create-new-namespaces).

2. Set all of the following values in your `config.yaml` file:

    ```yaml
    global:
      # Make fluentd gather logs from all available namespaces
      manualNamespaceNamesEnabled: true

    astronomer:

      houston:
        config:
          deployments:

            # Enable manual namespace names
            manualNamespaceNames: true

            # Precreated namespace names
            preCreatedNamespaces:
              - name: <namespace-name1>
              - name: <namespace-name2>
              - name: <namespace-etc>

            # Allows users to immediately reuse a pre-created namespace by hard deleting the associated Deployment
            hardDeleteDeployment: true

      commander:
        env:
          - name: "COMMANDER_MANUAL_NAMESPACE_NAMES"
            value: true

    ```

    > **Note:** If you want to add more namespaces in the future, you first need to ensure that those namespaces exist in Kubernetes before specifying their names in your `config.yaml` file.

3. Save the changes in your `config.yaml` file and push them to Astronomer as described in [Apply a Config Change](apply-platform-config.md).

## Using Pre-Created Namespaces

Once you enable pre-created namespaces, the namespaces you specified appear as an option when configuring a new Deployment via the Software UI.

![Kubernetes Namespace option in the UI](/img/software/kubernetes-namespace.png)

Alternatively, when you run `astro deployment create` command via the Astronomer CLI, you will be prompted to select one of the available namespaces for your new Deployment.

If no namespaces are available, you will receive an error when creating a new Deployment in both the UI and the CLI. To reuse a pre-created namespace, you need to first delete the Deployment using it.

> **Note:** Pre-created namespaces may take several days to become available again after deleting their associated Deployment. To immediately reuse a pre-created namespace, you need to hard-delete its associated Deployment as described in [Delete a Deployment](configure-deployment.md#delete-a-deployment).
