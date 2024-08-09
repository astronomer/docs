---
sidebar_label: 'Overview'
title: 'Configure component size-limits'
id: configure-component-size-limits
description: Learn the ways you can configure the maximum and minimum size of platform and Airflow components on Astronomer Software
---

Astronomer Software allows you to customize the minimum and maximum sizes of most Astronomer platform and Airflow components.

### Astro Units (AU's) {#what-is-an-au}
You can increase or decrease resources on Astro by units of size know as AU's (Astro Units). Adding or removing an AstroUnit changes a Deployment's size by changing the following:
* the size of a component by one-tenth of a v-core
* the size of the component by 384Mi of memory
* the limit of connections to the Postgres server by half of a connection
* the limit of connections used internally by Airflow to the database connection pooler by 5
* the size of the deployment-namespace's overall cumulative limits (ResourceQuota and LimitRange) by one-tenth of a v-core and 834Mi of memory.
* the limit of pods in the namespace by one pod (ResourceQuota)

### Configure Deployment-level limits for individual pod sizes {#configure-max-pod-size}
You can use `astronomer.houston.config.deployments.maxPodAu` to configure the maximum size any individual pod can be.

```yaml
astronomer:
  houston:
    config:
      deployments:
        maxPodAu: 35 # default is 35
```

### Configure Deployment-level limits for resource usage {#configure-cumulative-resource-limits}
Astronomer Software limits the amount of resources that can be used by all pods in a Deployment by creating and managing a `LimitRange` and `ResourceQuota` for the namespace associated with each Deployment.

These values are automatically adjust to account for the resource requirements of various components.

You can add additional resources, beyond the standard amount allocated based on the resource-requirements of standing components, to the `LimitRange` and `ResourceQuota`. Add resources by configuring `astronomer.houston.config.deployments.maxExtraAu` to account for the requirements of KubernetesExecutor and KubernetesPodOperator tasks.
```yaml
astronomer:
  houston:
    config:
      deployments:
        maxExtraAu: 400 # default is 400
```

### Configure the sizes of individual Deployment-level components {#configure-deployment-components}

Components represent different parts of the Astronomer Software Deployment. You can customize the default configuration for a component by defining it in `astronomer.houston.config.deployments.components`.

A list of configurable components and options is provided in [Configurable Components](#configurable-components).

:::tip
KubernetesExecutor Task pod sizes are created on an as-needed basis, and don't have persisting resource requirements. Their resource requirements are [configured at the task level](#configure-kubernetes-task-pod-size).
:::

When defining components, you must include the full definition of the component in the list entry after the components key, instead of only the components you want to define.

For example, to increase the maximum size a Celery worker task from 30 AU (3 Vcpu/11.5Gi) to 50AU (3 Vcpu/192Gi), add the full Celery worker component definition to `astronomer.houston.config.deployments.components` in your `values.yaml` with a higher limit (defined in AUs):

:::tip
When increasing CPU or memory limits, ensure the [maximum pod size](#configure-max-pod-size) is large enough to avoid errors during pod creation.
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

### Configurable Components

:::info
When [defining components](#configure-individual-deployment-components), you must include the full definition of the component in the list entry after the components key, instead of only the components you want to define.
:::

:::tip
KubernetesExecutor task pod sizes are created on an as-needed basis and don't have persisting resource requirements. Their resource requirements are [configured at the task level](#configure-kubernetes-task-pod-size).
:::

Configurable components include:

- **Airflow Scheduler**

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

- **Airflow Webserver**

   ```yaml
   - name: webserver
     au:
       default: 5
       minimum: 5
       limit: 30
   ```

- **StatsD**

   ```yaml
   - name: statsd
     au:
       default: 2
       minimum: 2
       limit: 30
   ```

- **Database Connection Pooler (PgBouncer)**

   ```yaml
   - name: pgbouncer
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

- **Celery Diagnostic Web Interface (Flower)**

   ```yaml
   - name: flower
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

- **Redis**

   ```yaml
   - name: redis
     au:
       default: 2
       minimum: 2
       limit: 2
   ```

- **Celery Workers**

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

- **Triggerer**

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

### Configure the size of KubernetesExecutor task pods {#configure-kubernetes-task-pod-size}

Kubernetes Executor task pods are defined at the task level when the DAG passes resource requests as part of `executor_config` into the Operator. When not defined, these tasks default to using 1 AU, which is one-tenth of a Vcpu/384 Mi of memory. This means that when you define resource requests or limits for CPU and memory, ensure the [maximum pod size](#configure-max-pod-size) is large enough to avoid errors during pod creation.

:::danger
Astronomer Software does not automatically raise then namespace-level cumulative resource-limits for pods created by KubernetesExecutor. To avoid pod-creation failures, increase `maxExtraAu`s to support your desired level of resourcing and concurrency.
:::

The following example demonstrates how to configure resource limits and requests:
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

Note that KubernetesExecutor task pods are limited to the `LimitRanges` and `quotas` defined within the pod namespace.

### Customize Astro Units (AU's) {#customize-au}

:::danger
Consult with your Astronomer Resident Architect before changing the amount of CPU or memory granted by an AU.
:::

Configurable options include:
* `astronomer.houston.config.deployments.astroUnit.cpu` - the amount an AU contributes to the size of a component, in thousandths of a vCPU, and the size of the `LimitRange` or `ResourceQuota`, defaults to `100`.
* `astronomer.houston.config.deployments.astroUnit.memory` - the amount an AU contributes to the size of a component, in Mi, and the size of the `LimitRange` or `ResourceQuota`, set to `384` by default.
* `astronomer.houston.config.deployments.astroUnit.pods` - the amount an AU contributes to the maximum amount of pods permitted by `ResourceQuota`, set to `1` by default.
* `astronomer.houston.config.deployments.astroUnit.actualConns` - the amount an AU contributes to the limit of connections to the Postgres server, set to `0.5` by default.
* `astronomer.houston.config.deployments.astroUnit.airflowConns` - The amount an AU contributes to the limit of connections used internally by Airflow to the database connection pooler, set to `5` by default.

The following code example shows how to set the resources per individual AU:

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