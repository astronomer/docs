---
title: 'DAG writing on Astro'
sidebar_label: 'DAG writing on Astro'
id: dag-writing-on-astro
---

You can run any valid Airflow DAG on Astro. 

That said, following best practices and taking full advantage of Astro features will help you:

- Produce DAGs more efficiently.
- Improve your development workflow.
- Better organize your deployment and DAGs. 
- Optimize resource usage and task execution efficiency.

This guide describes best practices for taking advantage of Astro features when writing DAGs. While this focuses on writing Airflow DAGs for Astro, all [general Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) are also recommended.

:::info New to Airflow?

If you are new to Airflow, we advise starting with the following resources:

- Hands-on tutorial: [Get started with Apache Airflow](https://docs.astronomer.io/learn/get-started-with-airflow).
- Astronomer Academy: [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).
- Webinar: [Airflow 101: How to get started writing data pipelines with Apache Airflow](https://www.astronomer.io/events/webinars/airflow-101-how-to-get-started-writing-data-pipelines-with-apache-airflow-video/).

:::

## Feature overview

In this guide, you'll learn about a number of Astro and Airflow features for optimizing your DAGs for Astro:

- [Astro Cloud IDE](https://docs.astronomer.io/astro/cloud-ide). A low-code, notebook-inspired IDE for writing and testing pipelines on Astro.
- [Astro CLI](overview.md). An OSS tool for developing DAGs and deploying projects tailor-made for Astro.
- [Worker queues](configure-worker-queues.mdx). A feature of Astro that enables resource optimization beyond what is possible using OSS Airflow.
- [Astro Cloud UI Environment Manager](manage-connections-variables.md). A tool for managing connections across multiple deployments locally and on Astro.
- [Astro alerts](alerts.md). No-code alerting on Astro configurable for various trigger types and communication channels.

## Best practice guidance

### Use the Astro Cloud IDE for secure, low-code development in the cloud

One of the highest barriers to using Airflow is writing boilerplate code for basic actions such as creating dependencies, passing data between tasks, and connecting to external services. If a low-code option is preferred by your team, the Cloud IDE is convenient because it enables you to set up these actions with the Astro UI and create pipelines by writing a minimal amount of Python or SQL code rather than entire DAGs.

To get the most out of the Astro Cloud IDE:

- Connect a Git repository for deployment of your pipelines using the [Astro GitHub integration](https://www.astronomer.io/docs/astro/deploy-github-integration). Deployment using the Astro CLI is also supported, but the GitHub integration offers advantages such as easy enforcement of software development best practices without custom CI/CD scripts, faster iteration on DAG code for teams, and greater visibility into the status and logs of individual deploys. For detailed guidance on deploying Cloud IDE pipelines, see [Deploy a project from the Cloud IDE to Astro](https://www.astronomer.io/docs/astro/cloud-ide/deploy-project).
- Locally test any DAGs employing async operators and task sensors prior to deployment after [exporting them](https://www.astronomer.io/docs/astro/cloud-ide/deploy-project#export-your-pipelines-to-a-local-astro-project). Although supported, async operators and task sensors cannot currently be tested in the Cloud IDE.

Learn more and get started by following the guidance in [Cloud IDE](https://www.astronomer.io/docs/astro/cloud-ide).

### Use the Astro CLI for local development

When writing DAGs intended for Astro Deployments, use the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) for containerized local development. The Astro CLI is an open-source interface you can use to:
- test Airflow DAGs locally
- deploy code to Astro
- automate key actions as part of a CI/CD process. 

To get the most out of the Astro CLI: 

- Use the `dags` directory to store your DAGs. If you have multiple DAGs, you can use subdirectories to keep your environment organized.
- Modularize your code and store all supporting classes, files and functions in the `include` directory.
- Store all your [tests](#follow-devops-best-practices) in the `tests` directory.

:::tip

If you are unable to install the Astro CLI on your local machine, due to company policy or for other reasons, you can use it in GitHub Codespaces by forking the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

:::

Learn more and get started by following the guidance in [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).

### Leverage Astro resources for improved Airflow management

We recommend taking advantage of the following features for easy management of your DAGs:

- **[Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables)** for managing connections. Allows you to define connections once and use them in multiple deployments (with or without overrides for individual fields), as well in your local development environment. Connections in the Environment Manager are stored in the Astronomer managed secrets backend.
- **[Deployment environment variables](environment-variables.md)** for storing environment variables. You can mark variables as secret for storage in the Astronomer managed secrets backend. You can store [Airflow variables](https://docs.astronomer.io/learn/airflow-variables) as environment variables as well by using the format `AIRFLOW_VAR_MYVARIABLENAME`.
- **[Worker queues](https://docs.astronomer.io/astro/configure-worker-queues)** for optimizing task execution efficiency. Worker queues allow you to define sets of workers with specific resources that execute tasks in parallel. You can assign tasks to specific worker queues to optimize resource usage. This feature is an improvement over OSS Airflow pools, which only manage concurrency and not resources. You can use both worker queues and pools in combination.
- **[Astro Alerts](alerts.md)** for setting up alerts for your DAGs. For more information, see [When to use Airflow or Astro alerts for your pipelines on Astro](airflow-vs-astro-alerts.md).

## Astro DAG Example 

Create a simple DAG that follows best practices for writing Airflow DAGs for Astro.

### Prerequisites

- At least one [Astro Deployment](create-deployment.md) with at least one [worker queue](https://docs.astronomer.io/astro/configure-worker-queues) defined.
- An [Astro project](https://docs.astronomer.io/astro/cli/overview) initialized with the Astro CLI or a fork of the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

### Implementation

1. Create a new DAG file in the `dags` directory.
2. Create a DAG with a docstring that will be converted to a DAG doc, a specified DAG owner, and an empty DAG definition:

    ```python
    """
    ## My DAG title

    My DAG description.
    """

    from airflow.decorators import dag
    from pendulum import datetime

    @dag(
        start_date=datetime(2024, 1, 1),
        schedule="@daily",
        catchup=False,
        doc_md=__doc__,  # Convert the docstring to a DAG Doc
        default_args={
            "retries": 3,  # Set retries to > 0
            "owner": "Astro"  # Define an owner
        },
        owner_links={
            "Astro": "mailto:my_email@my_company.com"  # Define a link for the owner
        },
        tags=["example", "best-practices"],  # Use tags to categorize your DAGs
    )
    def my_dag():
        
        # your tasks

    my_dag()
    ```

3. Add at least one task to your DAG definition. Optional: set the `queue` parameter to assign the task to a specific worker queue. 
4. Add a custom test to the DAG validation tests in the `tests/dags` directory. A commonly added test is one for enforcing that the `catchup` parameter is set to `False`:

    ```python
    @pytest.mark.parametrize(
        "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
    )
    def test_dag_has_catchup_false(dag_id, dag, fileloc):
        """
        test if a DAG has catchup set to False
        """
        assert (
            dag.catchup == False
        ), f"{dag_id} in {fileloc} must have catchup set to False."
    ```

5. Optional: add unit tests for your custom code and functions to the `tests` directory. See [Test Airflow DAGs](https://docs.astronomer.io/learn/testing-airflow) for more information and examples.
6. Use `astro dev pytest` to run all tests in the `tests` directory locally. Optional: integrate this command into a [CI/CD pipeline](set-up-ci-cd.md).
7. Add any connections required by your DAG to the [Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables).
8. Add any environment variables required by your DAG as [deployment environment variables](environment-variables.md).
9. Configure a **DAG Failure** alert for your DAG. Use the communication channel of your choice. See [Set up Astro alerts](https://docs.astronomer.io/astro/alerts).
10. [Deploy your project to Astro](https://www.astronomer.io/docs/astro/deploy-dags) and click on **Run** to run it.

Congratulations! You've followed best practices in writing a DAG optimized for Astro and successfully deployed it!

## See also

- Webinar: [Best practices for managing Airflow across teams](https://www.astronomer.io/events/webinars/best-practices-for-managing-airflow-across-teams-video/).
- Webinar: [DAG writing for data engineers and data scientists](https://www.astronomer.io/events/webinars/dag-writing-for-data-engineers-and-data-scientists-video/).
- OSS Learn guide: [DAG writing best practices in Apache Airflow](https://docs.astronomer.io/learn/dag-best-practices).
