---
title: 'Get started with Apache Airflow, Part 1: Write and run your first DAG'
sidebar_label: 'Part 1: Write your first DAG'
id: get-started-with-airflow
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

Getting started with Apache Airflow locally is easy with the Astro CLI.

This tutorial is for people who are new to Apache Airflow and want to run it locally with open source tools.

After you complete this tutorial, you'll be able to:

- Run a local Airflow environment using the Astro CLI.
- Manage the Astro project directory.
- Write a new DAG.
- Navigate the Airflow UI.
- Use code from the Astronomer Registry.

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Prerequisites

- A terminal that accepts bash commands. This is pre-installed on most operating systems.
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).
- An integrated development environment (IDE) for Python development, such as [VSCode](https://code.visualstudio.com/).
- Optional. A local installation of [Python 3](https://www.python.org/downloads/) to improve your Python developer experience.

## Step 1: Create an Astro project

To run data pipelines on Astro, you first need to create an Astro project, which contains the set of files necessary to run Airflow locally.

1. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

2. Open the directory:

    ```sh
    cd <your-astro-project-name>
    ```

3. Run the following Astro CLI command to initialize an Astro project in the directory:

    ```sh
    astro dev init
    ```

The Astro project is built to run Airflow with Docker. [Docker](https://docs.docker.com/) is a service to run software in virtualized containers within a machine. When you run Airflow on your machine with the Astro CLI, Docker creates a container for each Airflow component that is required to run DAGs. For this tutorial, you don't need an in-depth knowledge of Docker. All you need to know is that Airflow runs on the compute resources of your machine, and that all necessary files for running Airflow are included in your Astro project.

The default Astro project structure includes a collection of folders and files that you can use to run and customize Airflow. For this tutorial, you only need to know the following files and folders:

- `/dags`: A directory of DAG files. Each Astro project includes two example DAGs: `example-dag-basic` and `example-dag-advanced`. For more information on DAGs, see [Introduction to Airflow DAGs](dags.md).
- `Dockerfile`: This is where you specify your version of Astro Runtime, which is a runtime software based on Apache Airflow that is built and maintained by Astronomer. The CLI generates new Astro projects with the latest version of Runtime, which is equivalent to the latest version of Airflow. For advanced use cases, you can also configure this file with Docker-based commands to run locally at build time.

## Step 2: Start Airflow

Now that you have an Astro project ready, the next step is to actually start Airflow on your machine. In your terminal, open your Astro project directory and run the following command:

```sh
astro dev start
```

Starting Airflow for the first time can take 2 to 5 minutes. Once your local environment is ready, the CLI automatically opens a new tab or window in your default web browser to the Airflow UI at `https://localhost:8080`.

:::info

If port 8080 or 5432 are in use on your machine, Airflow won't be able to start. To run Airflow on alternative ports, run:

```sh
astro config set webserver.port <available-port>
astro config set postgres.port <available-port>
```

:::

## Step 3: Log in to the Airflow UI

The [Airflow UI](airflow-ui.md) is essential for managing Airflow. It contains information about your current DAG runs and is the best place to create and update Airflow connections to third-party data services.

To access the Airflow UI, open `http://localhost:8080/` in a browser and log in with `admin` for both your username and password.

The default page in the Airflow UI is the **DAGs** page, which shows an overview of all DAGs in your Airflow environment:

![View of starter DAGs in the Airflow UI](/img/tutorials/get-started-with-airflow_ui_with_starter_dags.png)

Each DAG is listed with a few of its properties, including tags, owner, previous runs, schedule, timestamp of the last and next run, and the states of recent tasks. Because you haven't run any DAGs yet, the **Runs** and **Recent Tasks** sections are empty. Let's fix that!

## Step 4: Trigger a DAG run

A **DAG run** is an instance of a DAG running on a specific date. Let's trigger a run of the `example-dag-basic` DAG that was generated with your Astro project.

To provide a basic demonstration of an ETL pipeline, this DAG creates an example JSON string, calculates a value based on the string, and prints the results of the calculation to the Airflow logs.

1. Before you can run any DAG in Airflow, you have to unpause it. To unpause `example-dag-basic`, click the slider button next to its name. Once you unpause it, the DAG starts to run on the schedule defined in its code.

    ![Unpause DAG slider in the Airflow UI](/img/tutorials/get-started-with-airflow_unpause_dag.png)

2. While all DAGs can run on a schedule defined in their code, you can manually trigger a DAG run at any time from the Airflow UI. Manually trigger `example-dag-basic` by clicking the play button under the **Actions** column. During development, running DAGs on demand can help you identify and resolve issues.

After you press **Play**, the **Runs** and **Recent Tasks** sections for the DAG start to populate with data.

![DAG running in the Airflow UI](/img/tutorials/get-started-with-airflow_dag_running.png)

These circles represent different [states](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) that your DAG and task runs can be in. However, these are only high-level summaries of your runs that won't make much sense until you learn more about how Airflow works. To get a better picture of how your DAG is running, let's explore some other views in Airflow.

## Step 5: Explore the Airflow UI

The navigation bar in the Airflow UI contains 5 tabs, each with different information about your Airflow environment. For more information about what you can find in each tab, see [The Airflow UI](airflow-ui.md).

Let's explore the available views in the **DAGs** page. To access different DAG views for `example-dag-basic`:

1. Click the name of the DAG.

    The default DAG view is the **Grid** view, which shows the state of completed and currently running tasks. Each column in the grid represents a complete DAG run, and each block in the column represents a specific task instance. This view is useful for seeing DAG runs over time and troubleshooting previously failed task instances.

    ![Grid view](/img/tutorials/get-started-with-airflow_grid_view.png)

    Click on a green square to display additional information about the related task instance on the right side of the Airflow UI. The task instance view includes tabs with additional information for the task instance, such as its logs and historic runs. This is one of many available views that show details about your DAG.

    ![Access task logs](/img/tutorials/get-started-with-airflow_access_task_instance.gif)

2. In the **Grid** view, click the **Graph** tab. This view shows task dependencies and relationships and can help you troubleshoot dependency issues. When you select a DAG run in the Grid view, the Graph tab shows the last state of each task instance in this DAG run.

    ![Graph view](/img/tutorials/get-started-with-airflow_graph_view_dagrun.gif)

3. In the **Grid** view, click the **Code** tab to display your DAG source code. Viewing code in the Airflow UI helps you confirm which version of your code is currently running on Airflow.

    ![Code view](/img/tutorials/get-started-with-airflow_code_view.png)

  :::info

  While you can view DAG code within the Airflow UI, code edits must be completed in the Python file within the `/dags` folder. The displayed code updates every 30 seconds.

  :::

## Step 6: Write a new DAG

Now that we can run DAGs and navigate the UI, let's write our own DAG and run it. In this step, you'll write a DAG that multiplies an input by 23. You'll copy most of the code, trigger the DAG, and then confirm the expected output is returned.

1. Create a new Python file in the `/dags` folder named `my-dag.py`.
2. Open `my-dag.py` in your IDE. Add the required imports for Python packages:

    ```python
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.bash import BashOperator

    from datetime import datetime, timedelta

    ```

    The first line imports the `DAG` class, the second and third lines import Airflow operators that are used in this example, and the last line imports two objects from the [datetime package](https://docs.python.org/3/library/datetime.html), which are required to define the schedule of a DAG.

3. In the same file, add two static variables and a simple Python function that multiplies an input by 23. The DAG will use an Airflow operator to call this code.

    ```python
    # constants
    MY_NAME = "MY_NAME"
    MY_NUMBER = 19

    def multiply_by_23(number):
        """Multiplies a number by 23 and prints the results to Airflow logs."""
        result = number * 23
        print(result)

    ```

4. Add a `dag` object, which is an instance of the `DAG` class:

    ```python
    with DAG(
        dag_id="my_first_dag",
        start_date=datetime(2022,7,28),
        schedule=timedelta(minutes=30),
        catchup=False,
        tags= ["tutorial"],
        default_args={
            "owner": MY_NAME,
            "retries": 2,
            "retry_delay": timedelta(minutes=5)
        }
    ) as dag:
    ```

    `with DAG(...) as dag:` instantiates a DAG context in which tasks can be defined and given dependencies. The instantiation includes several important arguments:

    - `dag_id` (Required): The name of the DAG that appears in the Airflow UI. Each DAG must have a unique name, and Astronomer recommends using the same name for the DAG file and the `dag_id`.
    - `start_date` (Required): The date and time when the DAG is scheduled to start running, given as a datetime object. In this example, the DAG is triggered on its schedule as long as the current time is 0:00 UTC on July 28th, 2022 or later.
    - `schedule`: The frequency the DAG runs. You can define this as a timedelta object, a [CRON expression](https://crontab.guru/), or as a macro such as "@daily". If you don't set this value, the DAG runs every 24 hours after the `start_date`.
    - `catchup`: Defines whether the DAG reruns all DAG runs that were scheduled before today's date. The default value is `True`, but it is recommended that you set this argument to `False` unless you are explicitly running your DAG to backfill runs.
    - `tags`: Defines the **Tags** that appear in the **DAGs** page of the Airflow UI. These can help you organize DAGs in more complex projects.
    - `default_args`: A list of configurations for the DAG's behavior. In this DAG, these arguments change the owner of the DAG, give the DAG a maximum of two retries in case of failure, and tell the DAG to wait five minutes before retrying. Many more arguments can be passed to a DAG at instantiation. See [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#tag/DAG) for a complete list.

4. Add a task to your DAG:

    ```python
    t1 = BashOperator(
        task_id="say_my_name",
        bash_command=f"echo {MY_NAME}"
    )

    ```

    An operator is a Python class containing the logic to define the work to be completed by a single task. The first task (`t1`) uses the [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator) to run a bash command that prints the `MY_NAME` variable to the terminal. The first parameter of the task (`task_id`) defines the name of the task that appears in the Airflow UI. Each task requires a unique `task_id`.

5. Add a second task to your DAG:

    ```python
    t2 = PythonOperator(
        task_id="multiply_my_number_by_23",
        python_callable=multiply_by_23,
        op_kwargs={"number": MY_NUMBER}
    )
    ```

    The [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator) can run any Python script that's accessible by our DAG. Our second task (`t2`) uses the PythonOperator to call the `multiply_by_23` function that we defined earlier. We can then pass arguments to the Python function by defining a dictionary of key value pairs in the `op_kwargs` parameter.

    This is one of the features that makes Airflow so powerful: Any action that can be defined in Python, no matter how complex, can be orchestrated using Airflow.

6. Define the dependencies between the two tasks using bitshift operators:

    ```python
    t1 >> t2
    ```

    This notation is unique to Airflow. It both defines and visualizes the dependencies between tasks. `t1` is **upstream** of `t2`. meaning that `t1` must finish before `t2` can start.

    There are multiple ways to define dependencies in Airflow, but this is one of the simplest. For more options on how to define task dependencies, see [Managing Dependencies in Apache Airflow](managing-dependencies.md).

7. Save your code.

## Step 7: Run the new DAG

To view your new DAG in the Airflow UI, enter `http://localhost:8080/` in your browser. As long as Airflow is running, it automatically picks up any new changes in your `/dags` directory. Existing files are parsed for changes every 30 seconds, while new files can be detected every 5 minutes.

When your new DAG appears in the Airflow UI, you can run it to test it.

1. Start the new DAG and trigger a run like you did in [Step 4](#step-4-trigger-a-dag-run).
2. Click the name of your new DAG and open the **Graph** view. After your DAG runs, there should be a dark green border around the tasks in the graph showing that your run was successful.

## Step 8: View task logs

When you tell Airflow to print something to the terminal, the output appears in Airflow task logs. Task logs are an important feature for unit testing or otherwise troubleshooting DAGs. If a task in your DAG fails, task logs are the best place to investigate why.

1. In the Airflow UI, open the **Grid** view.  
2. Click the `say_my_name` task to access details of the task instance.
3. Click the **Logs** tab.

In the log output, you should see the string you set for the `MY_NAME` constant:

```text
[2022-07-29, 15:17:19 UTC] {subprocess.py:74} INFO - Running command: ['bash', '-c', 'echo MY_NAME']
[2022-07-29, 15:17:19 UTC] {subprocess.py:85} INFO - Output:
[2022-07-29, 15:17:19 UTC] {subprocess.py:92} INFO - MY_NAME
[2022-07-29, 15:17:19 UTC] {subprocess.py:96} INFO - Command exited with return code 0
[2022-07-29, 15:17:19 UTC] {taskinstance.py:1415} INFO - Marking task as SUCCESS. dag_id=my_first_dag, task_id=say_my_name, execution_date=20220729T144715, start_date=20220729T151718, end_date=20220729T151719

```

Repeat steps 1-3 for the `multiply_my_number_by_23` task. The task logs should include the results of our multiplication operation.

```text
[2022-07-29, 15:17:22 UTC] {logging_mixin.py:115} INFO - 437
[2022-07-29, 15:17:22 UTC] {python.py:173} INFO - Done. Returned value was: None
[2022-07-29, 15:17:22 UTC] {taskinstance.py:1415} INFO - Marking task as SUCCESS. dag_id=my_first_dag, task_id=multiply_my_number_by_23, execution_date=20220729T144715, start_date=20220729T151721, end_date=20220729T151722
```

## Step 9: Use the Astronomer Registry

The example DAG you wrote used two different core Airflow operators, but there are many more operators available outside of core Airflow. The best place to explore and search for operators is the [Astronomer Registry](https://registry.astronomer.io/).

You can find [example DAGs](https://registry.astronomer.io/dags) in the Astronomer Registry that demonstrate more complex use cases and integrations. Now you'll add an example DAG to the Astro project:

1. Go to the [Astronomer Registry](https://registry.astronomer.io/).
2. In the search bar, search for `TaskFlow API`.
3. Go to the **DAGs** tab and open the **TaskFlow API ETL Example** DAG.
4. In the DAG's information page, click the **Code** tab and copy the contents of the DAG code.
5. Paste the code into a new `.py` in the `dags` folder of your Astro project.
6. Run the DAG from the Airflow UI.

This DAG demonstrates how you can define task dependencies using the TaskFlow API, which is a popular, more Pythonic method of writing DAGs. Instead of defining dependencies with bitshift operators, you can use direct calls to functions that have been decorated as tasks. In the example DAG, the following line:

```python
store_data(process_data(extract_bitcoin_price()))
```

has the same dependency structure as:

```
extract_bitcoin_price >> process_data >> store_data
```

If this style of DAG writing feels more intuitive to you, read more about it on the [Airflow Decorators concept page](airflow-decorators.md).

## Next steps

Astronomer offers a variety of resources like this tutorial to learn more about how to use Airflow.

- [Astronomer Webinars](https://www.astronomer.io/events/webinars/) cover concepts and use cases in-depth and offer the possibility to ask us questions live on air.
- [Astronomer Learn](https:/docs.astronomer.io/learn/) covers both entry and expert level concepts in Airflow.
- [Astronomer Academy](https://academy.astronomer.io/) offers many video tutorials and the option to purchase full length Airflow courses and to take exams to get certified.

Don't know where to start? For beginners, the next resources we recommend are:

- [Managing connections in Airflow](connections.md): Learn how to connect Airflow to third party products and services.
- [Develop a project](https://docs.astronomer.io/astro/develop-project): Learn about all of the ways you can configure your Astro project and local Airflow environment.
- [DAG Writing Best Practices](dag-best-practices.md): Learn how to write efficient, secure, and scalable DAGs.
