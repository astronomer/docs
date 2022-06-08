---
title: 'Configure a Kubernetes Namespace Pool for Astronomer Software'
sidebar_label: 'Configure Namespace Pools'
id: namespace-pools
description: Manually create Kubernetes namespaces for new Deployments.
---

## Overview

This guide explains how to configure and use pre-created namespaces on Astronomer Software.

Hosting Astronomer Software in a multi-tenant Kubernetes cluster poses challenges around security and resource contention. To address these challenges, you can configure a pool of pre-created namespaces and limit Astronomer Software's permissions exclusively to these namespaces.

Every Deployment requires an individual [Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) within your wider Astronomer Software installation. If a pool of pre-created namespaces is configured, Astronomer users will be required to select a namespace from that pool whenever they create a new Deployment. Once the Deployment is created, its corresponding namespace will no longer be available for other new Deployments. If a Deployment is deleted, its namespace will be returned to the pool and again become available for use.

### When To Use Pre-Created Namespaces

Configuring a pool of pre-created namespaces comes with two primary benefits:

- It limits the cluster-level permissions your organization needs to give to Astronomer Software.
- It can save on costs and protect against unwanted resource usage.

By configuring a pool of pre-created namespaces, Astronomer Software requires permissions only for the individual namespaces you configure. If your organization does not want Astronomer Software to have cluster-level permissions in a multi-tenant cluster, then we recommend configuring this feature.

A pre-created namespace pool can also enable resource protection. By default, Astronomer Software allows users to create Deployments until there is no more unreserved space in your cluster. If you use a pool, you can limit the number of active Deployments running at any given time. This is especially important if you run other Elastic workloads on your Software cluster and need to prevent users from accidentally claiming your entire pool of unallocated resources.

:::info Technical Deep Dive

When a user creates a new Deployment via the UI or CLI, Astronomer Software creates the necessary Airflow components and isolates them in a dedicated Kubernetes namespace. These Airflow components depend on Kubernetes resources, some of which are stored as secrets.

By default, Astronomer protects your Deployment's Kubernetes secrets by using dedicated service accounts for parts of your Deployment that need to interact with external components. To manage this process, Astronomer Software needs extensive cluster-level permissions that provide it some level of access to all namespaces running in your cluster.

In Kubernetes, there are two main levels of permissions. You can grant a service account permissions for an entire cluster, or you can grant permissions for existing namespaces. Astronomer uses cluster-level permissions because, by default, the amount of Deployments to manage is unknown. This level of permissions is appropriate if Astronomer Software is running in its own dedicated cluster, but can pose security risks when other applications are running in the same cluster.

For example, consider Astronomer's Commander service, which controls creating, updating, and deleting Deployments. By default, Commander has permissions to interact with secrets, roles, and service accounts for all applications in your cluster. The only way to mitigate this risk is by implementing pre-created namespaces.

:::

## Prerequisites

To configure pre-created namespaces, you need:

- [Helm](https://helm.sh/).
- [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) with access to the cluster hosting Astronomer Software.

## Step 1: Configure Namespaces

For every namespace you want to add to a pool, you must create a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [role](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole), and [rolebinding](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#rolebinding-and-clusterrolebinding) for Astronomer Software to access the namespace with. The `rolebinding` must be scoped to the `astronomer-commander` service account and the `namespace` you are creating.

1. In a new manifest file, add the following configuration. Make sure to replace `<your-namespace-name>` with the namespace you want to add to the pool.

    ```yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: <your-namespace-name>
    ---
    apiVersion: rbac.authorization.k8s.io/v1
       kind: Role
       metadata:
         name: deployment-commander-role
         namespace: <your-namespace-name>
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
         verbs: ["get", "list", "patch", "update", "watch"]
       - apiGroups: [""]
         resources: ["serviceaccounts"]
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

2. Save this file and name it `commander.yaml`.
3. In the Kubernetes cluster hosting Astronomer Software, run `kubectl apply -f commander.yaml`.
4. Repeat steps 1-3 for every namespace you want to add to your pool.

## Step 2: Configure a Namespace Pool in Astronomer

To enable pre-created namespaces on Astronomer Software:

1. Set the following values in your `config.yaml` file, making sure to specify all of the namespaces you configured in the `preCreatedNamespaces` object:

    ```yaml
    global:
      # Make fluentd gather logs from all available namespaces
      manualNamespaceNamesEnabled: true
      clusterRoles: false

    astronomer:
      houston:
        config:
          deployments:

            # Enable manual namespace names
            manualNamespaceNames: true
            # Pre-created namespace names
            preCreatedNamespaces:
              - name: <namespace-name-1>
              - name: <namespace-name-2>
              - name: <namespace-name-x>

            # Allows users to immediately reuse a pre-created namespace by hard deleting the associated Deployment
            # If set to false, you'll need to wait until a cron job runs before the Deployment record is deleted and the namespace is added back to the pool
            hardDeleteDeployment: true

      commander:
        env:
          - name: "COMMANDER_MANUAL_NAMESPACE_NAMES"
            value: true
    ```

2. Save the changes in your `config.yaml` and update Astronomer Software as described in [Apply a Config Change](apply-platform-config.md).

You should now be able to create new Deployments using a namespace from your pre-created namespace pool.

## Creating Deployments in Pre-Created Namespaces

After enabling the pre-created namespace pool, the namespaces you registered earlier will appear as an option when creating a new Deployment via the Software UI.

![Kubernetes Namespace option in the UI](https://assets2.astronomer.io/main/docs/astronomer-ui/kubernetes-namespace.png)

When you create Deployments via the CLI, you will be prompted to select one of the available namespaces for your new Deployment.

If no namespaces are available, you will receive an error when creating new Deployments in both the UI and CLU. To reuse a pre-created namespace, you first need to return the namespace to the pool by deleting its associated Deployment.

## Troubleshooting

### My Deployment Is in an Unknown State

If a Deployment is not coming up, check the Commander pods for confirmation on whether the Deployment commands have successfully executed. When using a pre-created namespace pool with scoped roles, it’s possible that the `astronomer-commander` service account does not have enough permissions to perform a required action. If Commander was able to do its job, you should see the below reference:

```
time="2021-07-21T16:30:23Z" level=info msg="releaseName <release-name>, chart astronomer-ee/airflow,     chartVersion 0.20.0, namespace <your-namespace-name>" function=InstallRelease package=helm
time="2021-07-21T16:30:23Z" level=info msg="CHART PATH: /home/commander/.cache/helm/repository/airflow-    0.20.0.tgz\n" function=InstallRelease package=helm
```

If something went wrong, you may see a reference such as:

```
time="2022-02-17T22:52:40Z" level=error msg="serviceaccounts is forbidden: User \"system:serviceaccount:astronomer:astronomer-commander\" cannot create resource \"serviceaccounts\" in API group \"\" in the namespace <your-namespace>" function=InstallDeployment package=kubernetes
```

This error shows that Astronomer Software does not have the ability to create service accounts in the pre-created namespaces, so the role needs to be updated accordingly.

### My Namespace is not Returning to the Pool

Unless you are using hard deletion, pre-created namespaces may take several days to become available again after deleting their associated Deployment. To enable hard deletes, refer to [Delete a Deployment](configure-deployment.md#delete-a-deployment).
