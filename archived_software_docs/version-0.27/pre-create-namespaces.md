---
title: 'Configure Pre-Created Kubernetes Namespaces for Astronomer Software'
sidebar_label: 'Pre-Create Namespaces'
id: pre-create-namespaces
description: Manually create Kubernetes namespaces for new Deployments.
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

            # Pre-created namespace names
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

## Create Namespace-Scoped Permissions for Astronomer

The Astronomer Commander service is responsible for provisioning resources to your Kubernetes clusters. By default, the Commander service uses a [`ClusterRole`](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#clusterrole-example) to access pre-created namespaces, meaning that it has the same permissions for all namespaces on your cluster.

If your organization uses pre-created namespaces and you want to limit Astronomer's permissions to individual namespaces, you can create an alternative [`Role`](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-example) for the Astronomer Commander service and apply this role to each pre-created namespace individually.

### Prerequisites

This setup assumes that you have:

- An Astronomer installation.
- A pre-created Kubernetes namespace [configured for Astronomer](pre-create-namespaces.md#enable-pre-created-namespaces).
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).

### Setup

To give the Astronomer Commander service permissions to an individual namespace:

1. Set the following value in your `config.yaml` file and [push your changes to Astronomer](apply-platform-config.md):

    ```yaml
    global:
      # Use cluster roles
      clusterRoles: false
    ```

2. In a new file named `commander.yaml`, add the following permissions so that the Astronomer Commander service can access your pre-created namespace:

    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: deployment-commander-role
      namespace: <your-namespace-name> # Should be namespace you are granting access to
    rules:
    - apiGroups: ["*"]
      resources: ["*"]
      verbs: ["list", "watch"]
    - apiGroups: [""]
      resources: ["configmaps"]
      verbs: ["create", "delete", "get", "list", "patch", "update", "watch"]
    - apiGroups: ["keda.k8s.io"]
      resources: ["scaledobjects"]
      verbs: ["get", "create", "delete"]
    - apiGroups: [""]
      resources: ["secrets"]
      verbs: ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"]
    - apiGroups: [""]
      resources: ["namespaces"]
      verbs: ["create", "delete", "deletecollection", "get", "list", "update", "watch"]
    - apiGroups: [""]
      resources: ["serviceaccounts"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["rbac.authorization.k8s.io"]
      resources: ["clusterroles"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["rbac.authorization.k8s.io"]
      resources: ["roles"]
      verbs: ["*"]
    - apiGroups: [""]
      resources: ["persistentvolumeclaims"]
      verbs: ["create", "delete", "deletecollection", "get", "list", "update", "watch", "patch"]
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list", "watch"]
    - apiGroups: [""]
      resources: ["endpoints"]
      verbs: ["create", "delete", "get", "list", "update", "watch"]
    - apiGroups: [""]
      resources: ["limitranges"]
      verbs: ["create", "delete", "get", "list", "watch", "patch"]
    - apiGroups: [""]
      resources: ["nodes"]
      verbs: ["get", "list", "watch"]
    - apiGroups: [""]
      resources: ["nodes/proxy"]
      verbs: ["get"]
    - apiGroups: [""]
      resources: ["persistentvolumes"]
      verbs: ["create", "delete", "get", "list", "watch", "patch"]
    - apiGroups: [""]
      resources: ["replicationcontrollers"]
      verbs: ["list", "watch"]
    - apiGroups: [""]
      resources: ["resourcequotas"]
      verbs: ["create", "delete", "get", "list", "patch", "watch"]
    - apiGroups: [""]
      resources: ["services"]
      verbs: ["create", "delete", "get", "list", "patch", "update", "watch"]
    - apiGroups: ["apps"]
      resources: ["statefulsets"]
      verbs: ["create", "delete", "get", "list", "patch", "watch"]
    - apiGroups: ["apps"]
      resources: ["daemonsets"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["apps"]
      resources: ["deployments"]
      verbs: ["create", "delete", "get", "patch","update"]
    - apiGroups: ["autoscaling"]
      resources: ["horizontalpodautoscalers"]
      verbs: ["list", "watch"]
    - apiGroups: ["batch"]
      resources: ["jobs"]
      verbs: ["list", "watch", "create", "delete"]
    - apiGroups: ["batch"]
      resources: ["cronjobs"]
      verbs: ["create", "delete", "get", "list", "patch", "watch"]
    - apiGroups: ["extensions"]
      resources: ["daemonsets", "replicasets"]
      verbs: ["list", "watch"]
    - apiGroups: ["extensions"]
      resources: ["deployments"]
      verbs: ["create", "delete", "get", "list", "patch", "update", "watch"]
    - apiGroups: [""]
      resources: ["events"]
      verbs: ["create", "delete", "patch"]
    - apiGroups: ["extensions"]
      resources: ["ingresses"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["extensions"]
      resources: ["ingresses/status"]
      verbs: ["update"]
    - apiGroups: ["networking.k8s.io"]
      resources: ["ingresses"]
      verbs: ["get", "create", "delete", "patch"]
    - apiGroups: ["networking.k8s.io"]
      resources: ["ingresses/status"]
      verbs: ["update"]
    - apiGroups: ["networking.k8s.io"]
      resources: ["networkpolicies"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["rbac.authorization.k8s.io"]
      resources: ["clusterrolebindings"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["rbac.authorization.k8s.io"]
      resources: ["rolebindings"]
      verbs: ["create", "delete", "get", "patch"]
    - apiGroups: ["authentication.k8s.io"]
      resources: ["tokenreviews"]
      verbs: ["create", "delete"]
    - apiGroups: ["authorization.k8s.io"]
      resources: ["subjectaccessreviews"]
      verbs: ["create", "delete"]
    - apiGroups: ["kubed.appscode.com"]
      resources: ["searchresults"]
      verbs: ["get"]
    - apiGroups: ["policy"]
      resources: ["poddisruptionbudgets"]
      verbs: ["create", "delete", "get"]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: deployment-commander-rolebinding
      namespace: <your-namespace-name> # Should be namespace you are granting access to
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: deployment-commander-role # Should match name of Role
    subjects:
    - namespace: astronomer # Should match namespace where SA lives
      kind: ServiceAccount
      name: astronomer-commander # Should match service account name, above
    ```

3. Apply the file to your pre-created namespace:

    ```yaml
    kubectl apply -f commander.yaml
    ```

4. To confirm that the configuration was successful, create a new Deployment with a [custom release name](configure-deployment.md#customize-release-names) in your custom namespace. If you check the logs of the Commander pod running in your custom namespace, you should see that Commander was able to immediately install Apache Airflow®® charts for the new Deployment:

    ```text
    time="2021-07-21T16:30:23Z" level=info msg="releaseName <release-name>, chart astronomer-ee/airflow,     chartVersion 0.20.0, namespace <your-namespace-name>" function=InstallRelease package=helm
    time="2021-07-21T16:30:23Z" level=info msg="CHART PATH: /home/commander/.cache/helm/repository/airflow-    0.20.0.tgz\n" function=InstallRelease package=helm
    ```
