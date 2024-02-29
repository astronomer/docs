---
title: "Get started with Apache Airflow, Part 2: Providers, connections, and variables"
sidebar_label: "Part 2: Providers, connections, and variables"
description: "Learn the core Apache Airflow concepts of using providers and connections."
id: get-started-with-airflow-part-2
---

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

- The Astro project created by completing [Part 1: Write your first DAG](get-started-with-airflow.md).
- A GitHub account with a personal access token and at least one repository. If you don’t have a GitHub repository you can follow the [steps in the GitHub documentation](https://docs.github.com/en/get-started/quickstart/create-a-repo) on how to create one.

:::info

If you do not have a GitHub account, you can create one for free on the [GitHub website](https://github.com/signup). To create a personal access token, see the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

:::

## Step 1: Create your DAG

In this second part of the Get Started with Airflow tutorial, you will add a third DAG to your Astro project. The new DAG interacts with GitHub and two external APIs to print the location of the International Space Station (ISS) to your task logs after a specific commit message is pushed to your GitHub repository.

1. Create a new Python file in the `dags` directory of your Astro project called `find_the_iss.py`.
2. Open the Astronomer Registry page for the [`find_the_iss`](https://registry.astronomer.io/dags/object_storage_use_case/versions/latest) example DAG. Click `</>` and copy the DAG code that appears.

    ![Screenshot of the Astronomer Registry showing the DAG code](/img/tutorials/get-started-with-airflow-part-2_registry_code_copy.png)

3. Paste the code into `find_the_iss.py`.

## Step 2: Add a provider package

1. Open the Airflow UI to confirm that your DAG was pushed to your environment. On the **DAGs** page, you should see a "DAG Import Error" like the one shown here:

    ![Screenshot of the Airflow UI Showing an Import Error saying: ModuleNotFoundError: No module named 'airflow.providers.github'](/img/tutorials/get-started-with-airflow-part-2_ImportError.png)

This error is due to a missing provider package. Provider packages are Python packages maintained separately from core Airflow that contain hooks and operators for interacting with external services. You can browse all available providers in the [Astronomer Registry](https://registry.astronomer.io/).

Your DAG uses operators from two Airflow provider packages: the [HTTP provider](https://registry.astronomer.io/providers/http/versions/latest) and the [GitHub provider](https://registry.astronomer.io/providers/github/versions/latest). While the HTTP provider is pre-installed in the Astro Runtime image, the GitHub provider is not, which causes the DAG import error.

2. Open the [GitHub provider page](https://registry.astronomer.io/providers/apache-airflow-providers-github/versions/latest) in the Astronomer Registry.

    ![GitHub Provider](/img/tutorials/get-started-with-airflow-part-2_GitHubProvider.png)

3. Copy the provider name and version by clicking **Use Provider** in the top right corner.
4. Paste the provider name and version into the `requirements.txt` file of your Astro project. Make sure to only add `apache-airflow-providers-github=<version>` without `pip install`.
5. Restart your Airflow environment by running `astro dev restart`. Unlike DAG code changes, package dependency changes require a complete restart of Airflow.

## Step 3: Add an Airflow variable

After restarting your Airflow instance, you should not see the DAG import error from [Step 2](#step-2-add-a-provider-package). Next, you will need to add an Airflow variable to be used in the [GithubSensor](https://registry.astronomer.io/providers/apache-airflow-providers-github/versions/latest/modules/GithubSensor).

[Airflow variables](airflow-variables.md) are key value pairs that can be accessed from any DAG in your Airflow environment. Because the variable `my_github_repo` is used in the DAG code with a default of `apache/airflow`, you'll need to create the variable and give it a value in the Airflow UI to wait for a commit in your own repository.

1. Go to **Admin** > **Variables** to open the list of Airflow variables. It will be empty.

    ![Screenshot of the Airflow UI with the Admin tab menu expanded to show the Variables option.](/img/tutorials/get-started-with-airflow-part-2_AdminVariables.png)

2. Click on the **+** sign to open the form for adding a new variable. Set the **Key** for the variable as `my_github_repo` and set the **Val** as a GitHub repository you have administrator access to. Make sure the **Val** is in the format `github_account_name/repository_name` (for example `apache/airflow`). The repository can be private.

3. Click **Save**.

## Step 4: Create a GitHub connection

An [Airflow connection](connections.md) is a set of configurations for connecting with an external tool in the data ecosystem. If you use a hook or operator that connects to an external system, it likely needs a connection.

In your example DAG, you used two operators that interact with two external systems, which means you need to define two different connections.

1. In the Airflow UI, go to **Admin** > **Connections**.
2. Click **+** to open the form for adding a new Airflow connection.
3. Name the connection `my_github_conn` and set its **Connection Type** to `GitHub`. Note that you can only select connection types that are available from either core Airflow or an installed provider package. If you are missing the connection type `GitHub`, double check that you installed the `GitHub` provider correctly in [Step 2](#step-2-add-a-provider-package).
4. Enter your **GitHub Access Token** in the GitHub Access Token field. If you need to create a token, you can follow the [official GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
5. Save the connection by clicking the **Save** button.

Note that the option to test connections is only available for selected connection types and disabled by default in Airflow 2.7+, see [Test a connection](connections.md#test-a-connection).

## Step 5: Create an HTTP connection

1. In the **Connections** view, click **+** to create a new connection.
2. Name the connection `open_notify_api_conn` and select a **Connection Type** of `HTTP`.
3. Enter the host URL for the API you want to query in the **Host** field. For this tutorial we use the [Open Notify API](http://open-notify.org/Open-Notify-API/), which has an endpoint returning the current location of the ISS. The host for this API is `http://api.open-notify.org`.
4. Click **Save**.

You should now have two connections as shown in the following screenshot:
    
![Connection List](/img/tutorials/get-started-with-airflow-part-2_TwoConnections.png)

## Step 6: Review the DAG code

Now that your Airflow environment is configured correctly, look at the DAG code you copied from the repository to see how your new variable and connections are used at the code level.

At the top of the file, the DAG is described in a docstring. It is an Airflow best practice to always describe your DAGs up front and include any additional connections or variables that are required for the DAG to work.

```python
"""
## Find the International Space Station

This DAG waits for a specific commit message to appear in a GitHub repository, 
and then will pull the current location of the International Space Station from an API
and print it to the logs.

This DAG needs a GitHub connection with the name `my_github_conn` and 
an HTTP connection with the name `open_notify_api_conn`
and the host `https://api.open-notify.org/` to work.

Additionally you will need to set an Airflow variable with 
the name `open_notify_api_endpoint` and the value `iss-now.json`.
"""
```

After the docstring, all necessary packages are imported. Notice how both the HttpOperator as well as the GithubSensor are part of provider packages.

```python
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.github.sensors.github import GithubSensor
from airflow.exceptions import AirflowException
from airflow.models import Variable
from pendulum import datetime
from typing import Any
import logging
```

Next, the Airflow task logger is instantiated and two top-level variables are defined. The variable `YOUR_GITHUB_REPO_NAME` is set to the value of the Airflow variable `my_github_repo` you defined in [Step 3](#step-3-add-an-airflow-variable) and the variable `YOUR_COMMIT_MESSAGE` is set to the commit message that triggers the DAG to run.

```python
task_logger = logging.getLogger("airflow.task")

YOUR_GITHUB_REPO_NAME = Variable.get(
    "my_github_repo", "apache/airflow"
)  # This is the variable you created in the Airflow UI
YOUR_COMMIT_MESSAGE = "Where is the ISS right now?"  # Replace with your commit message
```

Below, a function is defined to be used in the GithubSensor. This function will process the repository object returned by the [`get_repo` method](https://pygithub.readthedocs.io/en/latest/examples/Repository.html) of the [PyGitHub](https://pygithub.readthedocs.io/en/latest/index.html) package, using `.get_commits()` to retrieve the last 10 commits to the repository and compare them to the commit message defined in `YOUR_COMMIT_MESSAGE`. If the message is found, the function returns `True`, otherwise `False`. Note that the function is defined at the top level of the DAG file for convenience but could also be defined in a separate module, located in the `include` directory and reused across multiple DAGs.

```python
def commit_message_checker(repo: Any, trigger_message: str) -> bool | None:
    """Check the last 10 commits to a repository for a specific message.
    Args:
        repo (Any): The GitHub repository object.
        trigger_message (str): The commit message to look for.
    """

    task_logger.info(
        f"Checking for commit message: {trigger_message} in 10 latest commits to the repository {repo}."
    )

    result = None
    try:
        if repo is not None and trigger_message is not None:
            commits = repo.get_commits().get_page(0)[:10]
            for commit in commits:
                if trigger_message in commit.commit.message:
                    result = True
                    break
            else:
                result = False

    except Exception as e:
        raise AirflowException(f"GitHub operator error: {e}")
    return result
```

Next, the DAG context is instantiated using the [`@dag` decorator](airflow-decorators.md) with the following parameters:

- `dag_id` is not set explicitly, so it defaults to the name of the Python function, `find_the_iss`.
- `start_date` is set to January 1st, 2024, which means the DAG starts to be scheduled after this date.
- `schedule` is set to `@daily`, which means the DAG runs every day at 0:00 UTC. You can use any [CRON](https://crontab.guru/) string or shorthand for time-based schedules. 
- `catchup` is set to `False` to prevent DAG runs from between the `start_date` and today from being backfilled automatically.
- `doc_md` is set to the docstring of the DAG file to create [DAG Docs](custom-airflow-ui-docs-tutorial.md) you can view in the Airflow UI.
- `default_args` is set to a dictionary with the key `owner` set to `airflow` and the key `retries` set to `3`. The latter setting gives each task in this DAG 3 retries before failing, which is a common best practice to protect against transient failures.
- `tags` adds the `Connections` tag to the DAG in the Airflow UI.

```python
@dag(
    start_date=datetime(2024, 6, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "airflow", "retries": 3},
    tags=["Connections"],
)
def find_the_iss():
```

The DAG itself has three tasks. 

The first task uses the [GithubSensor](https://registry.astronomer.io/providers/apache-airflow-providers-github/versions/latest/modules/GithubSensor) to check whether the commit message `Where is the ISS right now?` has been added to your GitHub repository with the help of the `commit_message_checker` function described previously. 

This task utilizes the Airflow variable (`my_github_repo`) and the Airflow connection (`my_github_connection`) to access the correct repository with the appropriate credentials. The [sensor](what-is-a-sensor.md) checks for the tag every 5 seconds (`poke_interval`) and will time out after one hour (`timeout`). It is best practice to always set a `timeout` because the default value is 7 days, which can impact performance if left unchanged in DAGs that run on a higher frequency.

```python
    github_sensor = GithubSensor(
        task_id="github_sensor",
        github_conn_id="my_github_conn",
        method_name="get_repo",
        method_params={"full_name_or_id": YOUR_GITHUB_REPO_NAME},
        result_processor=lambda repo: commit_message_checker(repo, YOUR_COMMIT_MESSAGE),
        timeout=60 * 60,
        poke_interval=5,
    )
```

The second task uses the HttpOperator to send a `GET` request to the `/iss-now.json` endpoint of the [Open Notify API](http://open-notify.org/Open-Notify-API/) to retrieve the current location of the ISS. The response is logged to the Airflow task logs and pushed to the [XCom](airflow-passing-data-between-tasks.md) table in the Airflow metadata database to be retrieved by downstream tasks.

```python
    get_iss_coordinates = HttpOperator(
        task_id="get_iss_coordinates",
        http_conn_id="open_notify_api_conn",
        endpoint="/iss-now.json",
        method="GET",
        log_response=True,
    )
```

The third task uses the [TaskFlow API's](airflow-decorators.md) `@task` decorator to run a regular Python function processing the coordinates returned by the `get_iss_coordinates` task and printing the city and country of the ISS location to the task logs. The coordinates are passed to the function as an argument using `get_iss_coordinates.output`, which accesses the value returned by the `get_iss_coordinates` task from the XCom table.

This is an example of how you can use a traditional operator (HttpOperator) and a TaskFlow API task to perform similar operations, in this case querying an API. Which way of task writing you choose depends on your use case and often comes down to personal preference.

```python
    @task
    def log_iss_location(location: str) -> dict:
        """
        This task prints the current location of the International Space Station to the logs.
        Args:
            location (str): The JSON response from the API call to the Open Notify API.
        Returns:
            dict: The JSON response from the API call to the Reverse Geocode API.
        """
        import requests
        import json

        location_dict = json.loads(location)

        lat = location_dict["iss_position"]["latitude"]
        lon = location_dict["iss_position"]["longitude"]

        r = requests.get(
            f"https://api.bigdatacloud.net/data/reverse-geocode-client?{lat}?{lon}"
        ).json()

        country = r["countryName"]
        city = r["locality"]

        task_logger.info(
            f"The International Space Station is currently over {city} in {country}."
        )

        return r

    # calling the @task decorated task with the output of the get_iss_coordinates task
    log_iss_location_obj = log_iss_location(get_iss_coordinates.output)
```

Lastly, the dependency between the three tasks is set so that the `get_iss_coordinates` task only runs after the `github_sensor` task is successful and the `log_iss_location` task only runs after the `get_iss_coordinates` task is successful. This is done using the `chain` method. You can learn more about setting dependencies between tasks in the [Manage task and task group dependencies in Airflow](managing-dependencies.md) guide.

The last line of the DAG file calls the `find_the_iss` function to create the DAG.

```python
    chain(github_sensor, get_iss_coordinates, log_iss_location_obj)

find_the_iss()
```

## Step 7: Test your DAG

1. Go to the DAGs view and unpause the `find_the_iss` DAG by clicking on the toggle to the left of the DAG name. The last scheduled DAG run automatically starts, and the `github_sensor` task starts waiting for the commit message `"Where is the ISS right now?"` to be pushed to your GitHub repository. You will see two light green circles in the **DAGs** view which indicates that the DAG run is in progress and the `github_sensor` task is running.

    ![DAG running](/img/tutorials/get-started-with-airflow-part-2_GraphView.png)

2. Create a new commit in your GitHub repository by changing any file then running:

    ```bash
    git add <file>
    git commit -m "Where is the ISS right now?"
    git push
    ```

3. Watch for the `github_sensor` task to finish successfully. The `get_iss_coordinates` task should start right after, and after it completes successfully the `log_iss_location` task will run.
4. In the **Grid** view, click on the green box representing the successful task run for `log_iss_location`. Check the **Log** tab of the task instance to learn where the ISS is right now!

```
[2024-02-28, 15:28:20 UTC] {find_the_iss.py:113} INFO - The International Space Station is currently over Sian Ka'an in Mexico.
```

## See also

- The [Astronomer Registry](https://registry.astronomer.io/) to find information on all providers.
- The [Airflow connections](connections.md) guide to learn more about Airflow connections.
- The [Airflow variables](airflow-variables.md) guide to learn more about Airflow variables.
