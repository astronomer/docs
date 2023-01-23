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
- Basic knowledge of Airflow DAGs. See [Introduction to Airflow DAGs](dags.md)

## General Airflow debugging approach

With Airflow being a multifunctional tool at the heart of the data engineering stack it is impossible to list all issues that can arise. These questions will give you a starting point when troubleshooting.

- Is the problem with Airflow or with another system Airflow connects to? Test if the action can be performed in the external system from its UI, a script or the command-line.
- What is the state of your [Airflow components](airflow-components.md)? Inspect the logs of each component and restart your Airflow environment.
- Does Airflow have access to all relevant files? This is especially relevant when running Airflow in Docker, like with the Astro CLI.
- Are the [Airflow connections](connections.md) set correctly with correct credentials?
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
- Issues caused by custom commands in the Dockerfile, conflicts or dependencies in the packages located in `packages.txt` and `requirements.txt`. 
- The components are in a crash-loop because of errors in custom code in features like plugins or a custom XCom backend. Check out the scheduler logs with `astro dev logs -s` to troubleshoot.

:::info

To troubleshoot infrastructure issues when running Airflow in other forms like on Kubernetes using the [Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html) or managed services please refer to the relevant documentation.

:::

## Common DAG issues

In this section we will go over common issues related to DAGs you might encounter when developping locally.

### DAGs don't appear in the Airflow UI

If a DAG isn't appearing in the Airflow UI, it's typically because Airflow is unable to parse the DAG. If this is the case, you'll see an `Import Error` in the Airflow UI. 

![Import Error](/img/guides/import_error_2.png)

This error message should help you troubleshoot and resolve the issue. In the example above a task is missing the mandatory `task_id` parameter.

If you don't see an import error message, here are some debugging steps you can try:

- Make sure your DAG file is located in the `dags` folder.
- Airflow scans the `dags` folder for new DAGs every [`dag_dir_list_interval`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-dir-list-interval), which defaults to 5 minutes but can be modified. You might have to wait until this interval has passed before a new DAG appears in the Airflow UI or restart your Airflow environment. 
- Ensure that you have permission to see the DAGs, and that the permissions on the DAG file are correct.
- Run `airflow dags list` with the [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/usage-cli.html) to make sure that Airflow has registered the DAG in the metastore. If the DAG appears in the list, try restarting the webserver.
- Try restarting the scheduler with `astro dev restart`.
- If you see an error similar to the following image indicating that the scheduler is not running, check the scheduler logs to see if something in the DAG file is causing the scheduler to crash. If you are using the Astro CLI, run `astro dev logs -s` and then try restarting.

    ![No Scheduler](/img/guides/scheduler_not_running_2.png)

At the code level ensure that:

- Each DAG has a unique `dag_id`.
- Each DAG contains either the word `airflow` or `dag` (the scheduler will only parse files fulfilling this condition).
- Each DAG defined with the `@dag` decorator is called. See also [Introduction to Airflow decorators](airflow-decorators.md).

### Import Errors due to dependency conflicts

A frequent cause of DAG import errors is not having the necessary packages installed in your Airflow environment. For example additional [provider packages](https://registry.astronomer.io/providers) from which you are using operators or hooks or packages used in Airflow tasks.

Install OS level packages by adding their name to the `packages.txt` file. Python packages which are needed by Airflow tasks can be installed by adding them to the `requirements.txt` file. 

To prevent compatibility issues when new packages are released it is best practice to pin the version you want to work with like this: `astronomer-providers[all]==1.14.0`. If no version is pinned Airflow will always use the latest version available.

If you are using the Astro CLI packages will be installed in the scheduler container. You can confirm that a package is installed correctly by running:

```
astro dev bash --scheduler "pip freeze | grep <package-name>"
```

If you need conflicting package versions or a different Python version for different Airflow tasks you have a variety of options:

- [KubernetesPodOperator](kubepod-operator.md): to run a task in a separate Kubernetes Pod.
- [ExternalPythonOperator](external-python-operator): to run a task in a predefined virtual environment.
- [PythonVirtualEnvOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonvirtualenvoperator): to run a task in a temporary virtual environment. 

### DAGs are not running correctly

If your DAGs are either not running or running different than you intended consider checking the following common causes.

- DAGs need to be unpaused in order to run according to their schedule. You can unpause a DAG by clicking the toggle on the lefthand side of the Airflow UI or via the [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause).
- Double check that each DAG has a unique `dag_id`. If two DAGs with the same id are present in one Airflow instance the scheduler will pick one at random every 30 seconds to display.
- Make sure your DAG has a `start_date` in the past.
- Test the DAG using `astro dev dags test <dag_id>`.
- If no DAGs are running, check the state of your scheduler 
using `astro dev logs -s`. 

If your DAG is running but not at the schedule you intended take a look at the [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md) guide.



## Tasks aren't running

Your DAG is visible in the Airflow UI, but your tasks don't run when you trigger the DAG. This is a common issue and the cause can be very simple or complex. The following are some debugging steps you can try:

- Make sure your DAG is unpaused. If your DAG is paused when you trigger it, the tasks will not run. 

    ![Paused DAG](/img/guides/paused_dag.png)

    DAGs are paused by default, but you can change this behavior by setting `dags_are_paused_at_creation=False` in your Airflow config. If you do this, be aware of the `catchup` parameter in your DAGs.

    In Airflow 2.2 and later, paused DAGs are unpaused automatically when you manually trigger them.

- Ensure your DAG has a start date that is in the past. If your start date is in the future, triggering the DAG results in a successful DAG run even though no tasks ran.
- A DAG run is automatically triggered when you unpause the DAG if the start date and end of the data interval are both in the past, and `catchup=True`. For more details on data intervals and DAG scheduling, see [Scheduling and Timetables in Airflow](scheduling-in-airflow.md).
- If you are using a [custom timetable](scheduling-in-airflow.md), ensure that the data interval for your DAG run does not precede the DAG start date.
- If your tasks stay in a `scheduled` or `queued` state, ensure your scheduler is running properly. If needed, restart the scheduler or increase scheduler resources in your Airflow infrastructure.
- If you added tasks to an existing DAG that has `depends_on_past=True`, those newly added tasks won't run until their state is set for prior task runs.

## Tasks have a failure status

To view task run failure information, go to the **Tree View** or the **Graph View** in the Airflow UI. Failed task runs appear as red squares.

![Tree View Task Failure](/img/guides/tree_view_task_failure.png)

Task logs are your best resource to determine the cause of failures. To access the logs, click the failed task in the **Tree View** or the **Graph View** and click the **Log**. 

![Get Logs](/img/guides/access_logs.png)

The task logs provide information about the error that caused the failure. 

![Error Log](/img/guides/error_log.png)

To help identify and resolve task failures, you can set up error notifications. See [Error Notifications in Airflow](error-notifications-in-airflow.md).

Task failures in newly developed DAGs with error messages such as `Task exited with return code Negsignal.SIGKILL` or containing a `-9` error code are often caused by a lack of memory. Increase the resources for your scheduler, webserver, or pod, depending on whether you're running the Local, Celery, or Kubernetes executors respectively.

## Logs aren't appearing

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

- Review [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) to learn how connections work.
- Change the `default` connection to use your connection details or define a new connection with a different name and pass that to the hook or operator.
- Upgrade to Airflow 2.2 or later to use the test connections feature in the Airflow UI or API.

    ![Test Connections](/img/guides/test_connections.png)

- Every hook and operator has its own way of using a connection, and it can be difficult determining what parameters are required. Go to the [Astronomer Registry](https://registry.astronomer.io/) to determine what connections are required for hooks and operators.
- Define connections using Airflow environment variables instead of adding them in the Airflow UI. Make sure you're not defining the same connection in multiple places. If you do, the environment variable takes precedence.

## Recover from failures

If you've made any changes to your code, make sure to redeploy and use the code view in the Airflow UI to make sure that your changes have been captured by Airflow.

To rerun your DAG or a specific task after you've made changes, see [Rerunning Tasks](rerunning-dags.md#rerun-tasks). 

The information provided here should help you resolve the most common issues. For help with more complex issues, consider joining the [Apache Airflow Slack](https://airflow.apache.org/community/) or [contact Astronomer support](https://www.astronomer.io/get-astronomer/).
