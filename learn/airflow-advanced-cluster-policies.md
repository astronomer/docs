---
title: "Airflow cluster policies"
sidebar_label: "Cluster policies"
description: "Learn about everything you need to use the Apache Airflow cluster policies."
id: airflow-cluster-policies
tags: [cluster policies]
---

Cluster policies are a set of functions that Airflow administrators can define to mutate or perform custom logic on a few important Airflow objects:

- DAG
- Task
- Task Instance
- Pod
- Airflow Context variables

These policies allow administrators to centrally manage how Airflow users or DAG writers are interacting with the Airflow Cluster. They can modify or restrict their capability based on organization policy or ensure that users conform to common standards. For example, you want to ensure all the DAGs have `tags` before being deployed to production.

These cluster policies can be used to:

- Check if the DAGs/Tasks meet certain standards
- Setting default arguments on DAGs/Tasks
- Perform custom routing/skipping logic on the DAGs or Tasks

In this guide, you'll learn about the types of cluster policies, how these policies work, and how to implement these in Airflow.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Astro CLI. See [Get started with Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started-cli)

## Main types of cluster policies

- `dag_policy`: This policy is applicable to a DAG object, and takes a DAG object `dag` as a parameter. It runs at load time of the DAG from the `DagBag`.
- `task_policy` : This policy is applicable to a Task object. It gets executed when the task is created during parsing of the task from DagBag at load time. This means that the whole task definition can be altered in the task policy. It does not relate to a specific task running in a `DagRun`. The `task_policy` defined is applied to all the task instances that will be executed in the future.
- `task_instance_mutation_hook` : This policy is applicable to a Task Instance, which is an instance of a Task object and is created at run time. It takes a TaskInstance object `task_instance` as a parameter. This policy applies not to a task but to the instance of a task that relates to a particular `DagRun`. It is only applied to the currently executed run (i.e. instance) of that task. It is applied to a task instance in an Airflow worker, not in the dag file processor, just before the task instance is executed. 

## How the cluster policies work

Cluster policies can be implemented using either the `airflow_local_settings.py` or the `pluggy` interface. Any attributes defined using cluster policies take precedence over the attributes defined in your DAG or Task. 

The DAG and Task cluster policies can raise the `AirflowClusterPolicyViolation` exception to indicate that the DAG or Task they were passed are not compliant and should not be loaded. This is exception is displayed on the Airflow web UI as an `import error`. 

You can use `AirflowClusterPolicySkipDag` exception to skip a DAG. Note that this exception will not be displayed on the Airflow web UI.

### DAG policy

DAG policy allows you to overwrite or reconfigure DAG’a parameters as required. It allows you to: 

- Mutate a DAG object after it is loaded in the DagBag.
- Run code after your DAG has been fully generated. 

This means that the DAG processor still parses all DAG files even if it is skipped using a DAG policy.

**Example implementations:**

- Enforce default owner for the DAGs.
- Enforce certain tags for DAGs, either default or based on conditions.
- Enforce development DAGs do not run in production.
- Stop a DAG from being executed by raising a `AirflowClusterPolicyViolation` exception

Note that, `dag_policy` is applied before `task_policy` and after the DAG has been completely loaded. Hence, overriding the `default_args` parameter has no effect using `dag_policy`. If you want to override the default operator settings, use task policies instead.

```python
@hookimpl
def ensure_dags_are_tagged(dag: "DAG") -> None:
    tag_labels = [tag.split(":")[0] 
    for tag in dag.tags]
        if not "Owner" in tag_labels:
            raise AirflowClusterPolicyViolation(f"{dag.dag_id} does not have a 'Owner' tag defined.")
```

### Task policy

Task policy allows you to overwrite or reconfigure a task’s parameters. 

- Mutates tasks after they have been added to a DAG.
- It expects a `BaseOperator` as a parameter and you can configure skip/deny exceptions.

**Example implementations:**

- Enforce a task timeout policy.
- Using a different environment for different operators.
- Override a `on_success_callback` or `on_failure_callback` for a task.

```python
@hookimpl
def task_policy(task: "BaseOperator") -> None:
	min_timeout = datetime.timedelta(hours=24)
	if not task.execution_timeout or task.execution_timeout > min_timeout:
		raise AirflowClusterPolicyViolation(f"{task.dag.dag_id}:{task.task_id} time out isgreater than {min_timeout}")
```

### Task Instance mutation hook

Task Instance policy allows you to alter task instances before being queued by the Airflow scheduler. This is different from the `task_policy` function, which inspects and mutates tasks “as defined”, whereas task instance policies inspect and mutate task instances before execution.

**Example implementations:**

- Enforce a specific queue for certain Airflow Operators.
- Modify a task instance between retries.

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

This policy is applicable to Kubernetes Pod created at run time when using the `KubernetesPodOperator` or `KubernetesExecutor`. This is a original policy function that allows altering `kubernetes.client.models.V1Pod` object before they are passed to the Kubernetes client for scheduling.

This could be used, for instance, to add sidecar or init containers to every worker pod launched.

**Example implementation:**

- Set resource requests and limits.
- Increase resources assigned to a Pod.

```python
from kubernetes.client import models as k8s
from airflow.policies import hookimpl

@hookimpl
def pod_mutation_hook(pod) -> None:
    print("hello from pod_mutation_hook ",type(pod))
    print("spec : ", pod.spec)
    print("container base ", pod.spec.containers[0])
    print("container base type", type(pod.spec.containers[0]))

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

Policies can be implemented using using the `pluggy` interface. `pluggy` is used for plugin management, and gives the ability to have multiple implementations of the policy functions. You can implement `pluggy` interface using a setup-tools entrypoint in a custom module.

:::info

Using the `pluggy` method is available only in Airflow version 2.6 and above. For versions earlier than 2.6, you can use `config/airflow_local_settings.py` file under your `$AIRFLOW_HOME` to define your policies. See [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html#how-do-define-a-policy-function).

:::

### Create a package for your plugin

Create a package with the following structure for your plugin named `my_plugin`.

```bash
my_plugin/
│
├── my_plugin/
│   ├── __init__.py
│   ├── policy.py
│
├── pyproject.toml
├── README.md
├── LICENSE
└── setup.cfg
```

1. In the `pyproject.toml` file, add the following:

```bash
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my_plugin"
version = "0.1.0"

dependencies = ["apache-airflow>=2.6"]
[project.entry-points.'airflow.policy']
_ = 'my_plugin.policy'
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

3. In `setup.cfg` add the following:

```bash

[metadata]
name = my-plugin
version = 0.1.0
author = your name
author_email = youremail@email.com
description = Policy plugin

[options]
packages = my_plugin

[options.entry_points]
airflow.policy =
policy = my_plugin.policy

```

4. Build the `wheel` file:

```bash
python3 -m pip wheel . 
```

### Setup your Astro project

1. Initialize your Astro project using [Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started-cli).
    
2. Run `astro dev init` to initialize a new Astro project or open your Astro project. 
    
3. Copy over the `wheel` file you built in [Create a package for your plugin](#create-a-package-for-your-plugin) to the `include` folder of your Astro project.

4. Add the following line to your `Dockerfile`

```docker
RUN pip install include/my_plugin-0.1.0-py3-none-any.whl
```

5. For local Airflow, run `astro dev restart` to rebuild the Astro project. For Astro, run `astro deploy` to build and deploy to your Deployment.