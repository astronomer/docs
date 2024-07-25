---
sidebar_label: 'Overview'
title: 'Configure component size-limits'
id: configure-component-size-limits
description: Learn the ways you can configure the maximum and minimum size of platform and Airflow components on Astronomer Software
---

Astronomer Software allows you to customize the minimum and maximum sizes of most Astronomer platform and Airflow components.

### Astro Units (AU's) {#what-is-an-au}
Resources are increased or decreased by units of size know as AU's (Astro Units). Adding or removing an AstroUnit changes a deployments size by changing:
* the size of a component by one-tenth of a v-core
* the size of the component by 384Mi of memory
* the limit of connections to the Postgres server by half of a connection
* the limit of connections used internally by Airflow to the database connection pooler by 5
* the size of the deployment-namespace's overall cumulative limits (ResourceQuota and LimitRange) by one-tenth of a v-core and 834Mi of memory.
* the limit of pods in the namespace by one pod (ResourceQuota)

### Configuring deployment-wide limits on individual pod sizes {#configuring-max-pod-size}
`astronomer.houston.config.deployments.maxPodAu` can be used to configure the maximum size any individual pod can be.

```yaml
astronomer:
  houston:
    config:
      deployments:
        maxPodAu: 35 # default is 35
```

### Configuring deployment-wide limits on resource usage {#configuring-cumulative-resource-limits}
Astronomer Software limits the amount of resources that can be used by all pods in an Airflow deployment by creating and managing a `LimitRange` and `ResourceQuota` for the namespace associated with each Airflow deployment.

These values are automatically adjusted to account for the resource requirements of various components.

You can add additional resources, beyond the standard amount allocated based on the resource-requirements of standing components, to the `LimitRange` and `ResourceQuota` by configuring `astronomer.houston.config.deployments.maxExtraAu` to account for the requirements of KubernetesExecutor and KubernetesPodOperator tasks.
```yaml
astronomer:
  houston:
    config:
      deployments:
        maxExtraAu: 400 # default is 400
```

### Configuring the sizes of individual deployment-level components {#configuring-individual-deployment-components}

Components represent different parts of the Astronomer Software deployment. You can customize the default configuration for a component by defining it in `astronomer.houston.config.deployments.components`.

A list of configurable components and options is provided in [Configurable Components](#list-of-configurable-components).

:::tip
KubernetesExecutor Task pod-sizes are created on an as-needed basis and don't have standing resource-requirements. Their resource-requirements are [configured at the task level](#configuring-kubernetes-task-pod-size).
:::

When defining components, the **full definition** of the component must be included in the list entry undernearth the components key, not just the portions you wish to change.

For example, to increase the maximum size a Celery worker task can be from 30 AU (3 Vcpu/11.5Gi) to 50AU (3 Vcpu/192Gi), add the full Celery worker component definition to `astronomer.houston.config.deployments.components` in your `values.yaml` with a higher limit (defined in AUs) as per the following example:

:::tip
When raising cpu/memory limits, ensure the [maximum pod size](#configuring-max-pod-size) is large enough to avoid errors during pod-creation.
:::

```yaml
astronomer:
  houston:
    config:
      deployments:
        components:
        - name: workers
          au:
            default: 10
            minimum: 1
            limit: 50 # default was 30
          extra:
            - name: terminationGracePeriodSeconds
              default: 600
              minimum: 0
              limit: 36000
            - name: replicas
              default: 1
              minimum: 1
              limit: 10
        # any additional component configurations go here
        # - name: another-component
        #   au:
        #     default: 10
        #     ...
```

### Configurable Components {#list-of-configurable-components}

:::info
When [defining components](#configuring-individual-deployment-components) the **full definition** of the component must be included in the list entry undernearth the components key, not just the portions you wish to change.
:::

:::tip
KubernetesExecutor Task pod-sizes are created on an as-needed basis and don't have standing resource-requirements. Their resource-requirements are [configured at the task level](#configuring-kubernetes-task-pod-size).
:::

Configurable components include:

**Airflow Scheduler**

   ```yaml
   - name: scheduler
     au:
       default: 5
       minimum: 5
       limit: 30
     extra:
       - name: replicas
         default: 1
         minimum: 1
         limit: 4
         minAirflowVersion: 2.0.0
   ```

**Airflow Webserver**

   ```yaml
   - name: webserver
     au:
       default: 5
       minimum: 5
       limit: 30
   ```

**StatsD**

   ```yaml
   - name: statsd
     au:
       default: 2
       minimum: 2
       limit: 30
   ```

**Database Connection Pooler (PgBouncer)**

   ```yaml
   - name: pgbouncer
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

**Celery Diagnostic Web Interface (Flower)**

   ```yaml
   - name: flower
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

**Redis**

   ```yaml
   - name: redis
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

**Celery Workers**

   ```yaml
   - name: workers
     au:
       default: 10
       minimum: 1
       limit: 30
     extra:
       - name: terminationGracePeriodSeconds
         default: 600
         minimum: 0
         limit: 36000
       - name: replicas
         default: 1
         minimum: 1
         limit: 10
   ```

**Triggerer**

   ```yaml
   - name: triggerer
     au:
       default: 5
       minimum: 5
       limit: 30
     extra:
       - name: replicas
         default: 1
         minimum: 0
         limit: 2
         minAirflowVersion: 2.2.0
   ```

### Configuring the size of KubernetesExecutor Task Pods {#configuring-kubernetes-task-pod-size}

Kubernetes Executor task-pods are defined at the task-level with the dag by passing resource-requests as part of `executor_config` into the Operator, as per the example below:

When not defined, these tasks default to using 1 AU (one-tenth of a Vcpu/384 Mi of memory).

:::tip
Ask your Astronomer Resident Architect about options for customizing the default task pod size.
:::

:::danger
Astronomer Software does not automatically raise then namespace-level cumulative resource-limits for pods created by KubernetesExecutor. To avoid pod-creation failures, increase `maxExtraAu`s to support your desired level of resourcing and concurrency.
:::


:::tip
When setting cpu/memory requests/limits, ensure the [maximum pod size](#configuring-max-pod-size) is large enough to avoid errors during pod-creation.
:::

E.g.
```
# import kubernetes.client.models as k8s
from kubernetes.client import models as k8s

# define an executor_config with the desired resources
my_executor_config={
  "pod_override": k8s.V1Pod(
      spec=k8s.V1PodSpec(
          containers=[
              k8s.V1Container(
                  name="base",
                  resources=k8s.V1ResourceRequirements(
                      requests={
                          "cpu": "50m",
                          "memory": "384Mi"
                      },
                      limits={
                          "cpu": "1000m",
                          "memory": "1024Mi"
                      }
                  )
              )
          ]
      )
  )
}

# pass in executor_config=my_executor_config to any Operator

#@task(executor_config=my_executor_config)
#def some_task():
 #   ...

#task = PythonOperator(
#    task_id="another_task",
#    python_callable=my_fun,
#    executor_config=my_executor_config
#)

```

KubernetesExecutor task-pods are limited to the LimitRanges and Quotas defined within the pod namespace.

### Customizing Astro Units (AU's) {#redefining-the-au}

:::danger
Consult with your Astronomer Resident Architect before changing the amount of cpu/memory granted by an AU.
:::

Configurable options include:
* `astronomer.houston.config.deployments.astroUnit.cpu` - the amount an AU contributes to the size of a component (in thousandths-of-a-Vcpu) and the size of the LimitRange/ResourceQuota (defaults to 100)
* `astronomer.houston.config.deployments.astroUnit.memory` - the amount an AU contributes to the size of a component (in Mi) and the size of the LimitRange/ResourceQuota (defaults to 384)
* `astronomer.houston.config.deployments.astroUnit.pods` - the amount an AU contributes to the maximum amount of pods permitted by ResourceQuota (defaults to 1)
* `astronomer.houston.config.deployments.astroUnit.actualConns` - the amount an AU contributes to the limit of connections to the Postgres server (defaults to 0.5)
* `astronomer.houston.config.deployments.astroUnit.airflowConns` - the amount an AU contributes to the limit of connections used internally by Airflow to the database connection pooler (defaults to 5)

E.g.


```yaml
astronomer:
  houston:
    config:
      deployments:
        astroUnit:
          # values are listed with their default values
          cpu: 100
          memory: 384
          pods: 1
          actualConns: 0.5 # upstream connections to postgres
          airflowConns: 5  # downstream connections to airflow
```