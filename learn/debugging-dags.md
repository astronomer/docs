---
title: "Debug DAGs"
sidebar_label: "Debug DAGs"
description: "Troubleshoot Airflow DAGs in a local environment"
id: debugging-dags
---

This guide explains how to identify and resolve common Airflow DAG issues, as well as steps to take if you cannot find a solution to your issue.

This guide was written for Airflow 2+, if you are running pre-2.0 Airflow we highly recommend upgrading in order to prevent compatibility issues and become able to use state of the art Airflow features. For assistance in upgrading see the documentation on [Upgrading from 1.10 to 2](https://airflow.apache.org/docs/apache-airflow/stable/howto/upgrading-from-1-10/index.html).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Get started with Airflow tutorial](get-started-with-airflow.md).
- Basic knowledge of Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).

## General Airflow debugging approach

Due to Airflow being a multifunctional tool at the heart of the data engineering stack it is impossible to list all issues that can arise. These questions will give you a starting point when troubleshooting:

- Is the problem with Airflow or with another system Airflow connects to? Test if the action can be performed in the external system from its UI, a script or the command-line.
- What is the state of your [Airflow components](airflow-components.md)? Inspect the logs of each component and restart your Airflow environment.
- Does Airflow have access to all relevant files? This is especially relevant when running Airflow in Docker, for example using the Astro CLI.
- Are the [Airflow connections](connections.md) set correctly with correct credentials? See also [Troubleshooting connections](#troubleshooting-connections).
- Is the issue with all DAGs or isolated to one DAG?
- Can you collect the relevant logs? For more information on log location and configuration see the [Airflow logging](logging.md) guide.
- Which versions of Airflow and Airflow providers are you using? Check if the documentation you are following matches your package versions.
- Can you reproduce the problem in a new local Airflow instance using the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)?

Answering these questions will help you narrow down what kind of issue your dealing with and inform your next steps. 

## Airflow is not starting

The 3 most common ways to run Airflow locally are the [Astro CLI]((https://docs.astronomer.io/astro/cli/install-cli)), a [standalone instance](https://airflow.apache.org/docs/apache-airflow/stable/start.html) or running [Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). 

To first get started we recommend using the free and open-source Astro CLI, which in most cases is easy to set up. The most common causes for issues when starting the Astro CLI are:

- The Astro CLI was not correctly installed. Run `astro version` and consider upgrading if your version is outdated.
- The Docker Daemon is not running. Make sure to start Docker Desktop before starting the Astro CLI.
- Errors caused by custom commands in the Dockerfile, conflicts or dependencies in the packages located in `packages.txt` and `requirements.txt`. 
- The components are in a crash-loop because of errors in custom code in features like plugins or a custom XCom backend. Check out the scheduler logs with `astro dev logs -s` to troubleshoot.

:::info

To troubleshoot infrastructure issues when running Airflow on other platforms, for example in Docker, on Kubernetes using the [Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html) or on managed services please refer to the relevant documentation and customer support.

:::

## Common DAG issues

This section covers common issues related to DAGs you might encounter when developing locally.

### DAGs don't appear in the Airflow UI

If a DAG isn't appearing in the Airflow UI, it's typically because Airflow is unable to parse the DAG. If this is the case, you'll see an `Import Error` in the Airflow UI. 

![Import Error](/img/guides/import_error_2.png)

The error message often helps you in troubleshooting and resolving the issue. In the example above a task in the DAG located in the `expand_tg.py` file is missing the mandatory `task_id` parameter.

:::tip

You can fetch import errors using the Astro CLI by running `astro dev run dags list-import-errors`. (Airflow CLI: `airflow dags list-import-errors`).

:::

If you don't see an import error message, here are some debugging steps you can try:

- Make sure your DAG file is located in the `dags` folder.
- Airflow scans the `dags` folder for new DAGs every [`dag_dir_list_interval`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval), which defaults to 5 minutes but can be modified. You might have to wait until this interval has passed before a new DAG appears in the Airflow UI or restart your Airflow environment. 
- Ensure that you have permission to see the DAGs, and that the permissions on the DAG file are correct.
- Run `astro dev run dags list` with the Astro CLI (Airflow CLI: `airflow dags list`) to make sure that Airflow has registered the DAG in the metadata database. If the DAG appears in the list but not in the UI, try restarting the webserver.
- Try restarting the scheduler with `astro dev restart`.
- If you see an error similar to the following image indicating that the scheduler is not running, check the scheduler logs to see if an error in a DAG file is causing the scheduler to crash. If you are using the Astro CLI, run `astro dev logs -s` and then try restarting.

    ![No Scheduler](/img/guides/scheduler_not_running_2.png)

At the code level ensure that each DAG:

- has a unique `dag_id`.
- contains either the word `airflow` or `dag` (the scheduler will only parse files fulfilling this condition).
- that was defined with the `@dag` decorator is called. See also [Introduction to Airflow decorators](airflow-decorators.md).

### Import Errors due to dependency conflicts

A frequent cause of DAG import errors is not having the necessary packages installed in your Airflow environment. These packages include additional [provider packages](https://registry.astronomer.io/providers) from which you are using operators or hooks or Python packages used in Airflow tasks.

You can install OS level packages by adding their name to the `packages.txt` file. Python packages which are needed by Airflow tasks can be installed by adding them to the `requirements.txt` file. If you need to install packages using a specific package manager consider adding a bash command to your Dockerfile.

To prevent compatibility issues when new packages are released it is best practice to pin the version you want to work with like this: `astronomer-providers[all]==1.14.0`. If no version is pinned Airflow will always use the latest version available.

If you are using the Astro CLI, packages will be installed in the scheduler container. You can confirm that a package is installed correctly by running:

```
astro dev bash --scheduler "pip freeze | grep <package-name>"
```

If you need conflicting package versions or a specific Python version for different Airflow tasks you have a variety of options:

- [KubernetesPodOperator](kubepod-operator.md): runs a task in a separate Kubernetes Pod.
- [ExternalPythonOperator](external-python-operator): runs a task in a predefined virtual environment.
- [PythonVirtualEnvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator): runs a task in a temporary virtual environment. 

### DAGs are not running correctly

If your DAGs are either not running or running differently than you intended, consider checking the following common causes:

- DAGs need to be unpaused in order to run on their schedule. You can unpause a DAG by clicking the toggle on the lefthand side of the Airflow UI or via the [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause).

    ![Paused DAG](/img/guides/paused_dag_2.png)

    DAGs are paused by default as shown in the screenshot, you can change this behavior by setting [`dags_are_paused_at_creation=False`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval) in your Airflow config. If you do this, remember to set `catchup=False` in your DAGs to prevent automatic backfilling of DAG runs.

- Double check that each DAG has a unique `dag_id`. If two DAGs with the same id are present in one Airflow instance the scheduler will pick one at random every 30 seconds to display.
- Make sure your DAG has a `start_date` in the past.
- Test the DAG using `astro dev dags test <dag_id>`. (Airflow CLI: `airflow dags test <dag_id>`).
- If no DAGs are running, check the state of your scheduler 
using `astro dev logs -s`. 
- If many runs of your DAG are being scheduled after you unpause it, you most likely need to set the DAG parameter `catchup=False`.

If your DAG is running but not at the schedule you intended review the [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md) guide. If you are using a custom timetable, ensure that the data interval for your DAG run does not precede the DAG start date.

## Common Task issues

This section covers common issues related to tasks within DAGs you might encounter when developing locally. If a whole DAG is not running, please refer to the [DAGs are not running correctly](#dags-are-not-running-correctly) section above.

### Tasks are not running correctly

Your DAG is starting but one of more of your tasks are not running as intended. 

- Double check your DAGs `start_date` is in the past. A future `start_date` will result in a successful DAG run even though no tasks ran.
- If your tasks stay in a `scheduled` or `queued` state, ensure your scheduler is running properly. If needed, restart the scheduler or increase scheduler resources in your Airflow infrastructure.
- If you added tasks to an existing DAG that with the `depends_on_past` parameter set to `True`, those newly added tasks won't run until their state is set for prior task runs.
- When running many instances of a task or DAG be mindful of scaling parameters and configurations. Airflow has default settings that limit the amount of concurrently running DAGs and tasks. See [Scaling Airflow to optimize performance](airflow-scaling-workers.md) to learn more.
- If you are using task decorators and your tasks are not showing up in the Graph and Grid view make sure you are calling your tasks. See also [Introduction to Airflow decorators](airflow-decorators.md).
- Double check your task dependencies and trigger rules. See also [Manage DAG and task dependencies in Airflow](managing-dependencies.md). Consider recreating your DAG structure with [EmptyOperators](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/empty/index.html).
- If you are using the CeleryExecutor and tasks get stuck in the `queued` state consider turning on [`stalled_task_timeout`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#stalled-task-timeout).

### Tasks are failing 

There are many possible reasons for tasks to end in a failed state. 

On a high level most task failure issues fall into one of 3 categories:

- Issues with operator parameter inputs.
- Issues within the operator.
- Issues in an external system.

Failed tasks appear as red squares in the Grid view, where you can also directly access task logs.

![Grid View Task failure](/img/guides/grid_view_task_failure.png)

Task logs can also be accessed from the Graph view and have plenty of configuration options. Learn more in the [Airflow Logging](logging.md) guide.

![Get Logs](/img/guides/access_logs_grid_view.png)

The task logs provide information about the error that caused the failure. 

![Error Log](/img/guides/error_log_2.png)

To help identify and resolve task failures, you can set up error notifications. See [Error Notifications in Airflow](error-notifications-in-airflow.md).

Task failures in newly developed DAGs with error messages such as `Task exited with return code Negsignal.SIGKILL` or containing a `-9` error code are often caused by a lack of memory. Increase the resources for your scheduler, webserver, or pod, depending on whether you're running the Local, Celery, or Kubernetes executors respectively.

:::info

After resolving your issue you may want to rerun your DAGs or tasks, see [Rerunning DAGs](rerunning-dags.md). 

:::

### Issues with dynamically mapped tasks

[Dynamic task mapping](dynamic-tasks.md) is a powerful feature that was introduced in Airflow 2.3 to allow you to dynamically adjust the number of tasks based on changing input parameters at runtime. Starting with Airflow 2.5.0 you can even dynamically map over task groups.

Common reasons for errors when dealing with dynamically mapped tasks are:

- Make sure you are providing a keyword argument to the `.expand()` function. 
- When using `.expand_kwargs()` provide the mapped parameters in the form of a `List(Dict)`.
- Attempting to map over an empty list will cause the mapped task to be skipped.
- The limit for how many mapped task instances can be created of a task depends on the Airflow core config [`max_map_length`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#max-map-length) and is 1024 by default. 
- The number of mapped task instances of a specific task that can run in parallel across all runs of a given DAG depend on the task level parameter `max_active_tis_per_dag`.  
- Not all parameters are mappeable. If a parameter does not support mapping you will receive an Import Error like in the screenshot below.

    ![Unmappeable Error](/img/guides/error_unmappeable.png)

When creating complex patterns with dynamically mapped tasks we recommend to first create your DAG structure using EmptyOperators and decorated Python operators. Once the structure works as intended you can start adding your tasks. Refer to the [Create dynamic Airflow tasks](dynamic-tasks.md) guide for code examples.

:::tip

It is very common that the output of an upstream operator is in a slightly different format than what you need to map over. Use [`.map()`](https://docs.astronomer.io/learn/dynamic-tasks#transform-outputs-with-map) to transform elements in a list using a Python function. 

:::

## Missing Logs

When you check your task logs to debug a failure, you may not see any logs. On the log page in the Airflow UI, you may see a spinning wheel, or you may just see a blank file. 

Generally, logs fail to appear when a process dies in your scheduler or worker and communication is lost. The following are some debugging steps you can try:

- Try rerunning the task by [clearing the task instance](rerunning-dags.md#rerun-tasks) to see if the logs appear during the rerun.
- Increase your `log_fetch_timeout_sec` parameter to greater than the 5 second default. This parameter controls how long the webserver waits for the initial handshake when fetching logs from the worker machines, and having extra time here can sometimes resolve issues.
- Increase the resources available to your workers (if using the Celery executor) or scheduler (if using the local executor).
- If you're using the Kubernetes executor and a task fails very quickly (in less than 15 seconds), the pod running the task spins down before the webserver has a chance to collect the logs from the pod. If possible, try building in some wait time to your task depending on which operator you're using. If that isn't possible, try to diagnose what could be causing a near-immediate failure in your task. This is often related to either lack of resources or an error in the task configuration.
- Increase the CPU or memory for the task.
- Ensure that your logs are retained until you need to access them. The default log retention period on Astronomer is 15 days, so any logs outside of the retention period are not available. 
- Check your scheduler and webserver logs for any errors that might indicate why your task logs aren't appearing.

## Troubleshooting connections

Typically, Airflow connections are needed to allow Airflow to communicate with external systems. Most hooks and operators expect a defined connection parameter. Because of this, improperly defined connections are one of the most common issues Airflow users have to debug when first working with their DAGs. 

While the specific error associated with a poorly defined connection can vary widely, you will typically see a message with "connection" in your task logs. If you haven't defined a connection, you'll see a message such as `'connection_abc' is not defined`. 

The following are some debugging steps you can try:

- Review the [Manage connections in Apache Airflow](connections.md) guide to learn how connections work.
- Make sure you have the necessary provider packages installed in order to be able to use a specific connection type.
- Change the `default` connection to use your connection details or define a new connection with a different name and pass the new name to the hook or operator.
- Define connections using Airflow environment variables instead of adding them in the Airflow UI. Make sure you're not defining the same connection in multiple places. If you do, the environment variable takes precedence.
- Test if your credentials work when used in a direct API call to the external tool.
- Use the test connection feature that many connection types have available.

    ![Test Connections](/img/guides/test_connections_2.png)

To find information about what parameters are required for a specific connection:

1. Use the Docs tab of your provider in the Astronomer Registry to access the Apache Airflow documentation for the provider. Most commonly used providers will have documentation on each of their associated connection types. For example, you can find information on how to set up different connections to Azure in the Azure provider docs.
2. Check the documentation of the external tool you are connecting to and see if it offers guidance on how to authenticate.
3. Refer to the source code of the hook that is being used by your operator.

## I need more help

The information provided here should help you resolve the most common issues. If your issue was not covered in this guide and you are looking for more assistance we recommend the following avenues:

- Post your question to [Stackoverflow](https://stackoverflow.com/), tagged with `airflow` and other relevant tools you are using. Using Stackoverflow is ideal when you are unsure which tool is causing the error, since experts for different tools will be able to see your question.
- Join the Apache Airflow Slack and open a thread in `#newbie-questions` or `#troubleshooting`. The Airflow slack is the best place to get answers to more complex Airflow specific questions. 
- If you found a bug in Airflow or one of its core providers, please open an issue in the [Airflow GitHub repository](https://github.com/apache/airflow/issues). For bugs in Astronomer open source tools please open an issue in the relevant [Astronomer repository](https://github.com/astronomer).

To help the helpers and get more tailored answers, please include the following information in your question or issue:

- The way you are running Airflow (Astro CLI, standalone, Docker, managed services).
- Your Airflow version and the version of relevant providers.
- The full error with the error trace if applicable. 
- The full code of the DAG causing the error if applicable.
- What you are trying to accomplish in as much detail as possible.
- If something has worked before and stopped working: what has recently changed?

::: info

Found an error in one of our guides, tutorials or docs? Please tell us via an issue in the [Astronomer docs repository](https://github.com/astronomer/docs/issues). :)

:::
