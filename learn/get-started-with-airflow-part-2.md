---
title: "Get started with Apache Airflow, Part 2: Providers, connections, and variables"
sidebar_label: "Part 2: Providers, connections, and variables"
description: "Learn the core Apache Airflow concepts of using providers and connections."
id: get-started-with-airflow-part-2
---

Learn core Apache Airflow concepts in this hands-on tutorial using the Astro CLI.

Use this tutorial after completing [Part 1: Write your first DAG](get-started-with-airflow.md) to learn about how to connect Airflow to external systems.

After you complete this tutorial, you'll be able to:

- Add an Airflow provider to your Airflow environment.
- Create and use an [Airflow connection](connections.md).
- Create and use an [Airflow variable](airflow-variables.md).

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To complete this tutorial, you'll need to know:

- How to write DAGs and run Airflow. See [Part 1: Write your first DAG](get-started-with-airflow.md).
- The basics of git. See the [tutorial on Git’s official webpage](https://git-scm.com/docs/gittutorial).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).
- A GitHub account with a personal access token and at least one repository. If you don’t have a GitHub repository you can follow the [steps in the GitHub documentation](https://docs.github.com/en/get-started/quickstart/create-a-repo) on how to create one.

:::info

If you do not have a GitHub account, you can create one for free on the [GitHub website](https://github.com/signup). To create a personal access token, see the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

:::

## Step 1: Create your Astro project

To run Airflow data pipelines locally and on Astro, you first need to create an Astro project, which contains the set of files necessary to run Airflow locally. For more information on the Astro project, see [Part 1: Write your first DAG](get-started-with-airflow.md).

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

4. Run the following Astro CLI command to start Airflow:

    ```bash
    astro dev start
    ```

    Once your local environment is ready, the CLI automatically opens a new tab or window in your default web browser to the Airflow UI at `https://localhost:8080`.

5. Log in to the Airflow UI with `admin` for both your username and password.

## Step 2: Create your DAG

1. Create a new Python file in the `dags` directory of your Astro project called `my_second_dag.py`.
2. Open the Astronomer Registry page for [`my_second_dag`](https://registry.astronomer.io/dags/my_second_dag/versions/latest). Click `</>` and copy the DAG code that appears.

    ![Copy Code from the registry](/img/tutorials/get-started-with-airflow-part-2_registry_code_copy.png)

3. Paste the code into `my_second_dag.py`.

## Step 3: Add a provider package

1. Open the Airflow UI to confirm that your DAG was pushed to your environment. On the **DAGs** page, you should see a "DAG Import Error" like the one shown here:

    ![Import Error](/img/tutorials/get-started-with-airflow-part-2_ImportError.png)

This error is due to a missing provider package. Provider packages are Python packages maintained separately from core Airflow that contain hooks and operators for interacting with external services. You can browse all available providers in the [Astronomer Registry](https://registry.astronomer.io/).

Your DAG uses operators from two Airflow provider packages: the [HTTP provider](https://registry.astronomer.io/providers/http) and the [GitHub provider](https://registry.astronomer.io/providers/github). While the HTTP provider is pre-installed in the Astro Runtime image, the GitHub provider is not, which causes the DAG import error.

2. Open the [GitHub provider page](https://registry.astronomer.io/providers/apache-airflow-providers-github/versions/latest) in the Astronomer Registry.

    ![GitHub Provider](/img/tutorials/get-started-with-airflow-part-2_GitHubProvider.png)

3. Copy the provider name and version by clicking **Use Provider** in the top right corner.
4. Paste the provider name and version into the `requirements.txt` file of your Astro project. Make sure to only add `apache-airflow-providers-github=<version>` without `pip install`.
5. Restart your Airflow environment by running `astro dev restart`. Unlike DAG code changes, package dependency changes require a complete restart of Airflow.

## Step 4: Add an Airflow variable

After restarting your Airflow instance, you should not see the DAG import error from Step 2. Next, you will need to add an Airflow variable to be used in the GithubTagSensor.

[Airflow variables](airflow-variables.md) are key value pairs that can be accessed from any DAG in your Airflow environment. Because the variable `my_github_repo` is used in the DAG code with a default of `apache/airflow`, you'll need to create the variable and give it a value in the Airflow UI to wait for a tag in your own repository.

1. Go to **Admin** > **Variables** to open the list of Airflow variables. It will be empty.

    ![Admin Variables](/img/tutorials/get-started-with-airflow-part-2_AdminVariables.png)

2. Click on the **+** sign to open the form for adding a new variable. Set the **Key** for the variable as `my_github_repo` and set the **Val** as a GitHub repository you have administrator access to. Make sure the **Val** is in the format `github_account_name/repository_name` (for example `apache/airflow`). The repository can be private.

3. Click **Save**.

## Step 5: Create a GitHub connection

An [Airflow connection](connections.md) is a set of configurations for connecting with an external tool in the data ecosystem. If you use a hook or operator that connects to an external system, it likely needs a connection.

In your example DAG, you used two operators that interact with two external systems, which means you need to define two different connections.

1. In the Airflow UI, go to **Admin** > **Connections**.

    ![Admin Connections](/img/tutorials/get-started-with-airflow-part-2_AdminConnections.png)

2. Click **+** to open the form for adding a new Airflow connection.
3. Name the connection `my_github_connection` and set its **Connection Type** to `GitHub`. Note that you can only select connection types that are available from either core Airflow or an installed provider package. If you are missing the connection type `GitHub`, double check that you installed the `GitHub` provider correctly in [Step 3](#step-3-add-a-provider-package).
4. Enter your **GitHub Access Token** in the GitHub Access Token field. If you need to create a token, you can follow the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
5. Save the connection by clicking the **Save** button.

Note that the option to test connections is only available for selected connection types and disabled by default in Airflow 2.7+, see [Test a connection](connections.md#test-a-connection).

## Step 6: Create an HTTP connection

1. In the **Connections** view, click **+** to create a new connection.
2. Name the connection `my_http_connection` and select a **Connection Type** of `HTTP`.
3. Enter the host URL for the API you want to query in the **Host** field. For this tutorial we use the Catfact API, which returns a random fact about cats for every `GET` request. The host for this API is `http://catfact.ninja/fact`.
4. Click **Save**.

You should now have two connections as shown in the following screenshot:
    
![Connection List](/img/tutorials/get-started-with-airflow-part-2_TwoConnections.png)

## Step 7: Test your DAG

1. Go to the DAGs view and unpause the `my_second_dag` DAG by clicking on the toggle to the left of the DAG name. The last scheduled DAG run automatically starts, and the `tag_sensor` task starts waiting for the `my_awesome_tag` tag to be added to your GitHub repository. You will see two light green circles in the **DAGs** view which indicates that the DAG run is in progress and the `tag_sensor` task is running.

    ![DAG running](/img/tutorials/get-started-with-airflow-part-2_GraphView.png)

2. Add the tag `my_awesome_tag` to your GitHub repository by [configuring it in the GitHub UI](https://docs.github.com/en/repositories/releasing-projects-on-github/viewing-your-repositorys-releases-and-tags) or running `git tag my_awesome_tag && git push --tags` in your local repository clone.
3. Watch for the `tag_sensor` task to finish successfully. The `query_api` task should now start.
4. In the **Grid** view, click on the green box representing the successful task run for `query_api`. Check the **Log** page of the task for a brand new cat fact!

```
[2023-07-09, 16:34:04 UTC] {base.py:68} INFO - Using connection ID 'my_http_connection' for task execution.
[2023-07-09, 16:34:04 UTC] {http.py:148} INFO - Sending 'GET' to url: http://catfact.ninja/fact
[2023-07-09, 16:34:05 UTC] {http.py:125} INFO - {"fact":"Cats sleep 16 to 18 hours per day. When cats are asleep, they are still alert to incoming stimuli. If you poke the tail of a sleeping cat, it will respond accordingly.","length":167}
```

## Step 8: View your DAG code

Now that your Airflow environment is configured correctly, look at the DAG code you copied from the repository to see how your new configurations are used at the code level.

At the top of the file, all necessary packages are imported. Notice how both the `SimpleHttpOperator` as well as the `GithubTagSensor` are part of the provider packages you installed.

```python
from airflow.decorators import dag
from airflow.models import Variable
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.github.sensors.github import GithubTagSensor
from pendulum import datetime
```

Next, the DAG context is instantiated using the [`@dag` decorator](airflow-decorators.md). The DAG has the ID `my_second_dag`, and it starts running on July 1st, 2023. After its start date, the DAG runs every day at 9:00 AM as defined in a [cron](https://crontab.guru/) string. `catchup` is set to `False` in order to prevent the DAG runs from between the `start_date` and today from being scheduled automatically.

```python
@dag(
    start_date=datetime(2023, 7, 1),
    schedule="0 9 * * *",
    catchup=False,
    tags=["connections"],
)
def my_second_dag():
```

The DAG itself has two tasks. The first task uses the GithubTagSensor to check whether a tag named `my_awesome_tag` has been added to your GitHub repository. It utilizes the Airflow variable (`my_github_repo`) and connection (`my_github_connection`) to access the correct repository with the appropriate credentials. The `Variable.get()` method uses `apache/airflow` as the default value if it has not been defined by the user. The sensor checks for the tag every 30 seconds and will time out after one day. It is best practice to always set a `timeout` because the default value is quite long at 7 days, which can impact performance if left unchanged in DAGs that run on a higher frequency.

```python
    tag_sensor = GithubTagSensor(
        task_id="tag_sensor",
        github_conn_id="my_github_connection",
        tag_name="my_awesome_tag",
        repository_name=Variable.get("my_github_repo", "apache/airflow"),
        timeout=60*60*24,
        poke_interval=30
    )
```

The second task uses the SimpleHttpOperator to send a `GET` request to the cat fact API. The response is logged to the Airflow task logs using `log_response=True`.

```python
    query_API = SimpleHttpOperator(
        task_id="query_API",
        http_conn_id="my_http_connection",
        method="GET",
        log_response=True
    )
```

Lastly, the dependency between the two tasks is set so that the API is only queried after the `tag_sensor` task is successful and the DAG function is called.

```python
    tag_sensor >> query_API

my_second_dag()
```

## Conclusion

Congratulations on finishing this tutorial! You now know how to:

- Browse the [Astronomer Registry](https://registry.astronomer.io/) for providers.
- Add a provider to your Airflow environment.
- Configure [Airflow connections](connections.md).
- Add [Airflow variables](airflow-variables.md).
- Use the [GithubTagSensor](https://registry.astronomer.io/providers/apache-airflow-providers-github/versions/latest/modules/GithubTagSensor) and the [SimpleHTTPOperator](https://registry.astronomer.io/providers/apache-airflow-providers-http/versions/latest/modules/SimpleHttpOperator).
- Get a near infinite supply of cat facts.
