---
title: "Debug DAGs"
sidebar_label: "Debug DAGs"
description: "Troubleshoot Airflow DAGs"
id: debugging-dags
---

This guide explains how to identify and resolve common Airflow DAG issues. It also includes resources to try out if you can't find a solution to an Airflow issue.
While the focus of the troubleshooting steps provided lies on local development, much of the information is also relevant for running Airflow in a production context.

:::tip

Consider implementing systematic testing of your DAGs to prevent common issues. See the [Test Airflow DAGs](testing-airflow.md) guide.

:::

:::tip Related content

Other ways to learn:

- Webinar: [Debugging your Airflow DAGs](https://www.astronomer.io/events/webinars/debugging-your-airflow-dags/).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Get started with Airflow tutorial](get-started-with-airflow.md).
- Basic knowledge of Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).

## General Airflow debugging approach

To give yourself the best possible chance of fixing a bug in Airflow, contextualize the issue by asking yourself the following questions:

- Is the problem with Airflow, or is it with an external system connected to Airflow? Test if the action can be completed in the external system without using Airflow.
- What is the state of your [Airflow components](airflow-components.md)? Inspect the logs of each component and restart your Airflow environment if necessary.
- Does Airflow have access to all relevant files? This is especially relevant when running Airflow in Docker or when using the [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- Are your [Airflow connections](connections.md) set up correctly with correct credentials? See [Troubleshooting connections](#troubleshooting-connections).
- Is the issue with all DAGs, or is it isolated to one DAG?
- Can you collect the relevant logs? For more information on log location and configuration, see the [Airflow logging](logging.md) guide.
- Which versions of Airflow and Airflow providers are you using? Make sure that you're using the correct version of the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html).
- Can you reproduce the problem in a new local Airflow instance using the [Astro CLI](https://docs.astronomer.io/astro/cli/overview)?

Answering these questions will help you narrow down what kind of issue you're dealing with and inform your next steps. 

:::info

You can debug your DAG code with IDE debugging tools using the `dag.test()` method, which was added in Airflow 2.5. See [Debug interactively with dag.test()](testing-airflow.md#debug-interactively-with-dagtest).

:::

## Airflow is not starting on the Astro CLI

The 3 most common ways to run Airflow locally are using the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli), running a [standalone instance](https://airflow.apache.org/docs/apache-airflow/stable/start.html), or running [Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). This guide focuses on troubleshooting the Astro CLI, which is an open source tool for quickly running Airflow on a local machine. 

The most common issues related to the Astro CLI are:

- The Astro CLI was not correctly installed. Run `astro version` to confirm that you can successfully run Astro CLI commands. If a newer version is available, consider upgrading. 
- The Docker Daemon is not running. Make sure to start Docker Desktop before starting the Astro CLI.
- There are errors caused by custom commands in the Dockerfile, or dependency conflicts with the packages in `packages.txt` and `requirements.txt`. 
- Airflow components are in a crash-loop because of errors in custom plugins or XCom backends. View scheduler logs using `astro dev logs -s` to troubleshoot.

To troubleshoot infrastructure issues when running Airflow on other platforms, for example in Docker, on Kubernetes using the [Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html) or on managed services, please refer to the relevant documentation and customer support.

You can learn more about [testing and troubleshooting locally](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally) with the Astro CLI in the Astro documentation.

## Common DAG issues

This section covers common issues related to DAG code that you might encounter when developing.

### DAGs don't appear in the Airflow UI

If a DAG isn't appearing in the Airflow UI, it's typically because Airflow is unable to parse the DAG. If this is the case, you'll see an `Import Error` in the Airflow UI. 

![Import Error](/img/guides/import_error_2.png)

The message in the import error can help you troubleshoot and resolve the issue.

To view import errors in your terminal, run `astro dev run dags list-import-errors` with the Astro CLI, or run `airflow dags list-import-errors` with the Airflow CLI.

If you don't see an import error message but your DAGs still don't appear in the UI, try these debugging steps:

- Make sure all of your DAG files are located in the `dags` folder.
- Airflow scans the `dags` folder for new DAGs every [`dag_dir_list_interval`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval), which defaults to 5 minutes but can be modified. You might have to wait until this interval has passed before a new DAG appears in the Airflow UI or restart your Airflow environment. 
- Ensure that you have permission to see the DAGs, and that the permissions on the DAG file are correct.
- Run `astro dev run dags list` with the Astro CLI or `airflow dags list` with the Airflow CLI to make sure that Airflow has registered the DAG in the metadata database. If the DAG appears in the list but not in the UI, try restarting the Airflow webserver.
- Try restarting the Airflow scheduler with `astro dev restart`.
- If you see an error in the Airflow UI indicating that the scheduler is not running, check the scheduler logs to see if an error in a DAG file is causing the scheduler to crash. If you are using the Astro CLI, run `astro dev logs -s` and then try restarting.

    ![No Scheduler](/img/guides/scheduler_not_running_2.png)

At the code level, ensure that each DAG:

- Has a unique `dag_id`.
- Contains either the word `airflow` or the word `dag`. The scheduler only parses files fulfilling this condition.
- Is called when defined with the `@dag` decorator. See also [Introduction to Airflow decorators](airflow-decorators.md).

### Import errors due to dependency conflicts

A frequent cause of DAG import errors is not having the necessary packages installed in your Airflow environment. You might be missing [provider packages](https://registry.astronomer.io/providers) that are required for using specific operators or hooks, or you might be missing Python packages used in Airflow tasks.

In an Astro project, you can install OS-level packages by adding them to your `packages.txt` file. You can install Python-level packages, such as provider packages, by adding them to your `requirements.txt` file. If you need to install packages using a specific package manager, consider doing so by adding a bash command to your Dockerfile.

To prevent compatibility issues when new packages are released, Astronomer recommends pinning a package version to your project. For example, adding `astronomer-providers[all]==1.14.0` to your `requirements.txt` file ensures that no future releases of `astronomer-providers` causes compatibility issues. If no version is pinned, Airflow will always use the latest available version.

If you are using the Astro CLI, packages are installed in the scheduler Docker container. You can confirm that a package is installed correctly by running:

```sh
astro dev bash --scheduler "pip freeze | grep <package-name>"
```

If you have conflicting package versions or need to run multiple Python versions, you can run tasks in different environments using a few different operators:

- [KubernetesPodOperator](kubepod-operator.md): Runs a task in a separate Kubernetes Pod.
- [ExternalPythonOperator](external-python-operator): Runs a task in a predefined virtual environment.
- [PythonVirtualEnvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator): Runs a task in a temporary virtual environment.

If many Airflow tasks share a set of alternate package and version requirements a common pattern is to run them in two or more separate Airflow deployments. 

### DAGs are not running correctly

If your DAGs are either not running or running differently than you intended, consider checking the following common causes:

- DAGs need to be unpaused in order to run on their schedule. You can unpause a DAG by clicking the toggle on the left side of the Airflow UI or by using the [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause).

    ![Location of unpause toggle in the Airflow UI](/img/guides/paused_dag_2.png)

    If you want all DAGs unpaused by default, you can set [`dags_are_paused_at_creation=False`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval) in your Airflow config. If you do this, remember to set `catchup=False` in your DAGs to prevent automatic backfilling of DAG runs. In Airflow 2.2 and later, paused DAGs are unpaused automatically when you manually trigger them.

- Double check that each DAG has a unique `dag_id`. If two DAGs with the same id are present in one Airflow instance the scheduler will pick one at random every 30 seconds to display.
- Make sure your DAG has a `start_date` in the past. A DAG with a `start_date` in the future will result in a successful DAG run with no task runs. Do not use `datetime.now()` as a `start_date`.
- Test the DAG using `astro dev dags test <dag_id>`. With the Airflow CLI, run `airflow dags test <dag_id>`.
- If no DAGs are running, check the state of your scheduler 
using `astro dev logs -s`. 
- If too many runs of your DAG are being scheduled after you unpause it, you most likely need to set `catchup=False` in your DAG's parameters.

If your DAG is running but not on the schedule you expected, review the [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md) guide. If you are using a custom timetable, ensure that the data interval for your DAG run does not precede the DAG start date.

## Common task issues

This section covers common issues related to individual tasks you might encounter. If your entire DAG is not working, see the [DAGs are not running correctly](#dags-are-not-running-correctly) section above.

### Tasks are not running correctly

It is possible for a DAG to start but its tasks to be stuck in various states or to not run in the desired order. If your tasks are not running as intended, try the following debugging methods:

- Double check that your DAG's `start_date` is in the past. A future `start_date` will result in a successful DAG run even though no tasks ran.
- If your tasks stay in a `scheduled` or `queued` state, ensure your scheduler is running properly. If needed, restart the scheduler or increase scheduler resources in your Airflow infrastructure.
- If your tasks have the `depends_on_past` parameter set to `True`, those newly added tasks won't run until you set the state of prior task runs.
- When running many instances of a task or DAG, be mindful of scaling parameters and configurations. Airflow has default settings that limit the amount of concurrently running DAGs and tasks. See [Scaling Airflow to optimize performance](airflow-scaling-workers.md) to learn more.
- If you are using task decorators and your tasks are not showing up in the **Graph** and **Grid** view, make sure you are calling your tasks. See also [Introduction to Airflow decorators](airflow-decorators.md).
- Check your task dependencies and trigger rules. See [Manage DAG and task dependencies in Airflow](managing-dependencies.md). Consider recreating your DAG structure with [EmptyOperators](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/empty/index.html) to ensure that your dependencies are structured as expected.
- As of Airflow 2.6, the [`task_queued_timeout`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#task-queued-timeout) parameter controls how long tasks can be in queued state before they are either retried or marked as failed. The default is 600 seconds.
- If you are using the CeleryExecutor in an Airflow version earlier than 2.6 and tasks get stuck in the `queued` state, consider turning on [`stalled_task_timeout`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#stalled-task-timeout).

### Tasks are failing 
Most task failure issues fall into one of 3 categories:

- Issues with operator parameter inputs.
- Issues within the operator.
- Issues in an external system.

Failed tasks appear as red squares in the **Grid** view, where you can also directly access task logs.

![Grid View Task failure](/img/guides/grid_view_task_failure.png)

Task logs can also be accessed from the **Graph** view and have plenty of configuration options. See [Airflow Logging](logging.md).

![Get Logs](/img/guides/access_logs_grid_view.png)

The task logs provide information about the error that caused the failure. 

![Error Log](/img/guides/error_log_2.png)

To help identify and resolve task failures, you can set up error notifications. See [Error Notifications in Airflow](error-notifications-in-airflow.md).

Task failures in newly developed DAGs with error messages such as `Task exited with return code Negsignal.SIGKILL` or containing a `-9` error code are often caused by a lack of memory. Increase the resources for your scheduler, webserver, or pod, depending on whether you're running the Local, Celery, or Kubernetes executors respectively.

:::info

After resolving your issue you may want to rerun your DAGs or tasks, see [Rerunning DAGs](rerunning-dags.md). 

:::

### Issues with dynamically mapped tasks

[Dynamic task mapping](dynamic-tasks.md) is a powerful feature that was introduced in Airflow 2.3 to allow you to dynamically adjust the number of tasks at runtime based on changing input parameters. Starting with Airflow 2.5.0 you can also dynamically map over task groups.

Possible causes of issues when working with dynamically mapped tasks include:

- You did not provide a keyword argument to the `.expand()` function. 
- When using `.expand_kwargs()`, you did not provide mapped parameters in the form of a `List(Dict)`.
- You tried to map over an empty list, which causes the mapped task to be skipped.
- You exceeded the limit for how many mapped task instances you can create. This limit depends on the Airflow core config [`max_map_length`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#max-map-length) and is 1024 by default. 
- The number of mapped task instances of a specific task that can run in parallel across all runs of a given DAG depend on the task level parameter `max_active_tis_per_dag`.  
- Not all parameters are mappeable. If a parameter does not support mapping you will receive an Import Error like in the screenshot below.

    ![Unmappeable Error](/img/guides/error_unmappeable.png)

When creating complex patterns with dynamically mapped tasks, we recommend first creating your DAG structure using EmptyOperators or decorated Python operators. Once the structure works as intended, you can start adding your tasks. Refer to the [Create dynamic Airflow tasks](dynamic-tasks.md) guide for code examples.

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
- Ensure that your logs are retained until you need to access them. If you are an Astronomer customer see our documentation on how to [View logs](https://docs.astronomer.io/astro/view-logs).
- Check your scheduler and webserver logs for any errors that might indicate why your task logs aren't appearing.

## Troubleshooting connections

Typically, Airflow connections are needed to allow Airflow to communicate with external systems. Most hooks and operators expect a defined connection parameter. Because of this, improperly defined connections are one of the most common issues Airflow users have to debug when first working with their DAGs. 

While the specific error associated with a poorly defined connection can vary widely, you will typically see a message with "connection" in your task logs. If you haven't defined a connection, you'll see a message such as `'connection_abc' is not defined`. 

The following are some debugging steps you can try:

- Review [Manage connections in Apache Airflow](connections.md) to learn how connections work.
- Make sure you have the necessary provider packages installed to be able to use a specific connection type.
- Change the `<external tool>_default` connection to use your connection details or define a new connection with a different name and pass the new name to the hook or operator.
- Define connections using Airflow environment variables instead of adding them in the Airflow UI. Make sure you're not defining the same connection in multiple places. If you do, the environment variable takes precedence.
- Test if your credentials work when used in a direct API call to the external tool.
- Test your connections using the Airflow UI or the Airflow CLI. See [Testing connections](connections.md#testing-connections).

    ![Test Connections](/img/guides/test_connections_2.png)

:::note

Testing connections is disabled by default in Airflow 2.7+. You can enable connection testing by defining the environment variable `AIRFLOW__CORE__TEST_CONNECTION=Enabled` in your Airflow environment. Astronomer recommends not enabling this feature until you are sure that only highly trusted UI/API users have "edit connection" permissions.

:::

To find information about what parameters are required for a specific connection:

- Read provider documentation in the [Astronomer Registry](https://registry.astronomer.io/providers?page=1) to access the Apache Airflow documentation for the provider. Most commonly used providers will have documentation on each of their associated connection types. For example, you can find information on how to set up different connections to Azure in the Azure provider docs.
- Check the documentation of the external tool you are connecting to and see if it offers guidance on how to authenticate.
- View the source code of the hook that is being used by your operator.

You can also test connections from within your IDE by using the `dag.test()` method. See [Debug interactively with dag.test()](testing-airflow.md#use-variables-and-connections-in-dagtest) and [How to test and debug your Airflow connections](https://www.astronomer.io/events/webinars/how-to-test-and-debug-your-airflow-connections/).

## I need more help

The information provided here should help you resolve the most common issues. If your issue was not covered in this guide, try the following resources:

- If you are an Astronomer customer contact our [customer support](https://support.astronomer.io/).
- Post your question to [Stack Overflow](https://stackoverflow.com/), tagged with `airflow` and other relevant tools you are using. Using Stack Overflow is ideal when you are unsure which tool is causing the error, since experts for different tools will be able to see your question.
- Join the [Apache Airflow Slack](https://apache-airflow-slack.herokuapp.com/) and open a thread in `#newbie-questions` or `#troubleshooting`. The Airflow slack is the best place to get answers to more complex Airflow specific questions. 
- If you found a bug in Airflow or one of its core providers, please open an issue in the [Airflow GitHub repository](https://github.com/apache/airflow/issues). For bugs in Astronomer open source tools please open an issue in the relevant [Astronomer repository](https://github.com/astronomer).

To get more specific answers to your question, include the following information in your question or issue:

- Your method for running Airflow (Astro CLI, standalone, Docker, managed services).
- Your Airflow version and the version of relevant providers.
- The full error with the error trace if applicable. 
- The full code of the DAG causing the error if applicable.
- What you are trying to accomplish in as much detail as possible.
- What you changed in your environment when the problem started.
