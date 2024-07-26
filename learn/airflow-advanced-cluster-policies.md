---
title: "Airflow cluster policies"
sidebar_label: "Cluster policies"
description: "Learn about everything you need to use the Apache Airflow cluster policies."
id: airflow-cluster-policies
tags: [cluster policies]
---

Cluster policies are sets of rules that Airflow administrators can define to mutate or perform custom logic on a few important Airflow objects:

- DAG
- Task
- Task Instance
- Pod
- Airflow Context variables

These policies allow administrators to centrally manage how Airflow users or DAG writers are interacting with the Airflow Cluster. Cluster policies can modify or restrict a user's capability based on organization policy or ensure that users conform to common standards. For example, you might want to ensure all DAGs have `tags` in your production Airflow environment.

Cluster policies can be used to, for example, centrally:

- Enforce Task or DAG-level retries
- Verify a DAG's `catchup` parameter based on production or development environment
- Limit the resources requested by a `KubernetesPodOperator`
- Routing critical jobs to a specific Celery `queue` or Airflow `pool`
- Add missing `tags` or `owner` emails

In this guide, you'll learn about the types of cluster policies, how the policies work, and how to implement them in Airflow.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- The Astro CLI. See [Get started with Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started-cli)

## Types of cluster policies

You can use four types of cluster policies in Airflow:

- `dag_policy`: This policy is applicable to a DAG object, and takes a DAG object `dag` as a parameter. It runs at the time the DAG is loaded from the `DagBag`.
- `task_policy` : This policy is applicable to a Task object. It gets executed when the task is created during parsing of the task from `DagBag` at load time. This means that the whole task definition can be altered in the task policy. It does not relate to a specific task running in a `DagRun`. The `task_policy` defined is applied to all the task instances that will be executed in the future.
- `task_instance_mutation_hook` : This policy is applicable to a Task Instance, which is an instance of a Task object and is created at run time. It takes a TaskInstance object `task_instance` as a parameter. This policy applies not to a task but to the instance of a task that relates to a particular `DagRun`. It is only applied to the currently executed run (i.e. instance) of that task. The policy is applied to a task instance in an Airflow worker before the task instance is executed, not in the dag file processor. 
- `pod_mutation_hook`: This policy is applicable to a Kubernetes Pod launched by `KubernetesPodOperator` or `KubernetesExecutor` at runtime. It takes a Pod object `pod` as a parameter. This policy is applied to the `kubernetes.client.models.V1Pod` object before it is passed to the Kubernetes client for scheduling. This cluster policy is available only from Aiflow version `2.6`.

## How cluster policies work

Cluster policies can be implemented using either your `airflow_local_settings.py` file or the `pluggy` interface. Any attributes defined using cluster policies take precedence over the attributes defined in your DAG or Task. In Astro, you can only implement policies using the `pluggy` interface.

Once implemented, if a DAG or task is not compliant with your set policies, the policy will raise the `AirflowClusterPolicyViolation` exception and the DAG will not be loaded. This exception is displayed on the Airflow web UI as an `import error`. 

You can also use the `AirflowClusterPolicySkipDag` exception to skip a DAG. For example, you may want to skip month-end DAGs from daily processing or skip any DAGs with the wrong environment tag. Another possible use case could be when you are migrating from a deprecated source system to a new one. You might want to skip the old DAGs to avoid any failures and alerts. Note that this exception will not be displayed on the Airflow web UI.

### DAG policy

The DAG policy allows you to overwrite or reconfigure a DAG’s parameters based on the criteria you set. It allows you to: 

- Mutate a DAG object after it is loaded in the DagBag.
- Run code after your DAG has been fully generated. 

This means that the DAG processor still parses all DAG files even if it is skipped using a DAG policy.

Some example implementations include:

- Enforce a default owner for your DAGs.
- Enforce certain tags for DAGs, either default or based on conditions.
- Ensure development DAGs do not run in production.
- Stop a DAG from being executed by raising an `AirflowClusterPolicyViolation` exception.

Note that the `dag_policy` is applied before the `task_policy` and after the DAG has been completely loaded. Hence, overriding the `default_args` parameter has no effect using `dag_policy`. If you want to override the default operator settings, use task policies instead.
#### Example
```python
@hookimpl
def ensure_dags_are_tagged(dag: "DAG") -> None:
    tag_labels = [tag.split(":")[0] 
    for tag in dag.tags]
        if not "Owner" in tag_labels:
            raise AirflowClusterPolicyViolation(f"{dag.dag_id} does not have a 'Owner' tag defined.")
```

### Task policy

The task policy allows you to overwrite or reconfigure a task’s parameters. 

- Mutates tasks after they have been added to a DAG.
- It expects a `BaseOperator` as a parameter and you can configure skip/deny exceptions.

Some example implementations include:

- Enforce a task timeout policy.
- Using a different environment for different operators.
- Override a `on_success_callback` or `on_failure_callback` for a task.

#### Example

```python
@hookimpl
def task_policy(task: "BaseOperator") -> None:
    min_timeout = datetime.timedelta(hours=24)
    if not task.execution_timeout or task.execution_timeout > min_timeout:
        raise AirflowClusterPolicyViolation(f"{task.dag.dag_id}:{task.task_id} time out isgreater than {min_timeout}")
```

### Task Instance mutation hook

:::info

If you are on Airflow version `2.9.1` or lower, you might see some inconsistencies in the application of `task_instance_mutation_hook`. This was fixed in Airflow `2.9.2`.

:::

Task Instance policy allows you to alter task instances before being queued by the Airflow scheduler. This is different from the `task_policy` function, which inspects and mutates tasks “as defined”, whereas task instance policies inspect and mutate task instances before execution.

Some example implementations include:

- Enforce a specific queue for certain Airflow Operators.
- Modify a task instance between retries.

#### Example

```python
@hookimpl
def task_instance_mutation_hook(task_instance:TaskInstance):
    if task_instance.try_number >= 3:
        task_instance.queue = "big-machine"
```

:::tip

Note that since priority weight is determined dynamically using weight rules, you cannot alter the `priority_weight` of a task instance within the Task Instance mutation hook.

:::

### Pod mutation hook

This policy is applicable to Kubernetes Pod created at run time when using the `KubernetesPodOperator` or `KubernetesExecutor`. This is a policy function that allows altering `kubernetes.client.models.V1Pod` object before they are passed to the Kubernetes client for scheduling.

This could be used, for instance, to alter the resoures for a Pod or to add sidecar or init containers to every worker pod launched. Astro, however, does not allow adding init or sidecar containers. [Astro](https://www.astronomer.io/docs/astro/deployment-metrics) provides advanced logging, metrics collection, and multiple ways to manage your environment without the need to run separate containers to collect stats or apply environment settings.

Some example implementations include:

- Set resource requests and limits.
- Increase resources assigned to a Pod.

#### Example

```python
from kubernetes.client import models as k8s
from airflow.policies import hookimpl

@hookimpl
def pod_mutation_hook(pod) -> None:
    print("hello from pod_mutation_hook ",type(pod))

    resources = k8s.V1ResourceRequirements(
        requests={
            "cpu": "100m",
            "memory": "256Mi",
        },
        limits={
            "cpu": "1000m",
            "memory": "1Gi",
        },
    )
    pod.spec.containers[0].resources = resources
```

## Implementation

Policies can be implemented using the `pluggy` interface. `pluggy` is used for plugin management, and allows you to have multiple implementations of the policy functions. You can implement `pluggy` interface using a setup-tools entrypoint in a custom module.

:::info

Using the `pluggy` method is available only in Airflow version 2.6 and above. For versions earlier than 2.6, you can use `config/airflow_local_settings.py` file under your `$AIRFLOW_HOME` to define your [policies](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html#how-do-define-a-policy-function). Note, that Astro only allows to use `pluggy` interface for implementing cluster policies.

:::

### Create a package for your policies

You can build a package for the cluster policies you want to apply to your Airflow environment. You can add this package to the `plugin` folder of your Astro project. You could then install it by [customizing your `Dockerfile`](https://www.astronomer.io/docs/astro/cli/customize-dockerfile). 

For example, you can create a package `my_package` with the following structure:

```bash
my_package/
│
├── my_package/
│   ├── __init__.py
│   ├── policy.py
│
├── pyproject.toml
├── README.md
├── LICENSE
```

1. In the `pyproject.toml` file, add the following:

    ```bash
    [build-system]
    requires = ["setuptools >= 61.0"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "my_package"
    version = "0.1.0"

    dependencies = ["apache-airflow>=2.6"]
    [project.entry-points.'airflow.policy']
    _ = 'my_package.policy'
    ```

2. Define the policies in `policy.py`

    ```python
    from airflow.policies import hookimpl
    from airflow.exceptions import AirflowClusterPolicyViolation

    @hookimpl
    def task_policy(task):
        print("Hello from task_policy")
        doc_str = "This is a test doc string"
        task.doc = doc_str

    @hookimpl
    def dag_policy(dag):
        """Ensure that DAG has at least one tag and skip the DAG with `only_for_beta` tag."""
        print("Hello from DAG policy")
        if not dag.tags:
            raise AirflowClusterPolicyViolation(
                f"DAG {dag.dag_id} has no tags. At least one tag required. File path: {dag.fileloc}"
            )
    ```

3. (Optional) Build the python package to generate the `wheel` file.

    ```bash
    python -m build
    ```

### Setup your Astro project

1. Initialize your Astro project using [Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started-cli).
    
2. Run `astro dev init` to initialize a new Astro project or open your Astro project. 
    
3. Copy over the plugin package to the `plugins` dirctory of an Astro project. 

4. Add the following line to your `Dockerfile`

    ```docker
    COPY plugins plugins
    RUN pip install ./plugins
    ```

:::tip Alternate setup
You can copy over the `wheel` file you built in Step 3 of [Create a package for your policies](#create-a-package-for-your-policies) to the `include` folder of your Astro project and add the following line to your `Dockerfile`:
```docker
RUN pip install include/my_package-0.1.0-py3-none-any.whl
```
:::

5. For local Airflow, run `astro dev restart` to rebuild the Astro project. For Astro, run `astro deploy` to build and deploy to your Deployment.