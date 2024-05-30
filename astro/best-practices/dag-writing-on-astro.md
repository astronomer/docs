---
title: 'How to optimize Airflow DAGs for Astro'
sidebar_label: 'DAG writing on Astro'
id: dag-writing-on-astro
---

You can run any valid Airflow DAG on Astro. 

However, following best practices in using Astro features will help you:

- Improve your development workflow.
- Organize your deployment and DAGs. 
- Optimize task execution efficiency.

While this best practice guide focuses on writing Airflow DAGs for Astro, all [general Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) also apply.

:::info New to Airflow?

If you are new to Airflow in general, we recommend starting with the following resources:

- Hands-on tutorial: [Get started with Apache Airflow](https://docs.astronomer.io/learn/get-started-with-airflow).
- Astronomer Academy: [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).
- Webinar: Airflow 101: How to get started writing data pipelines with Apache Airflow.

:::

## Feature overview

In this guide, you'll learn when to use the following Astro and Airflow features to optimize your DAGs for Astro:

- [Astro CLI](overview.md).
- [CI/CD on Astro](set-up-ci-cd.md).
- [Worker queues](configure-worker-queues.mdx).
- [Astro Cloud UI Environment Manager](manage-connections-variables.md).
- [Astro alerts](alerts.md).
- [Kubernetes Executor](executors-overview.md).
- [KubernetesPodOperator](kubernetespodoperator.md).

## Best practice guidance 

This section provides a list of best practices for writing Airflow DAGs on Astro.

### Use the Astro CLI for local development

The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) is Astronomer's OSS tool to develop Airflow DAGs locally in a controlled, containerized environment. 

After initializing a new project with the Astro CLI by running `astro dev init`, follow these guidelines to organize your project:

- Use the `dags` directory to store your DAGs. If you have multiple DAGs, consider organizing them into subdirectories.
- Modularize your code and store all supporting classes, files and functions in the `include` directory.
- Store all your [tests](#follow-devops-best-practices) in the `tests` directory.

:::tip

If you are unable to install the Astro CLI on your local machine, due to company policy or other reasons, you can use it in GitHub Codespaces by forking the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

:::

### Follow DevOps best practices

Airflow pipelines are Python code and all software engineering best practices apply: 

- Store your code in a version control system like [GitHub](https://github.com/).
- Create [dedicated branches for development, staging and production](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- Use a CI/CD pipeline to automate testing and deployment. See [Develop a CI/CD workflow for deploying code to Astro](https://docs.astronomer.io/astro/set-up-ci-cd).

![Airflow CI/CD pipeline showing a 3 branch structure with a dev branch corresponding to Local Development, a staging branch corresponding to a staging Deployment and a production branch corresponding to the Production deployment. CI/CD is present at all steps of the workflow.](/img/docs/airflow-cicd-3-branches.png)

Your Airflow pipelines should be tested and validated before deployment:

- Write **DAG validation tests** and store them in the `tests` directory to create rules for you DAGs, for example to enforce the use of specific operators, or restrict which schedules are allowed. See [Key DAG writing best practices for Astro](#key-dag-writing-best-practices-for-astro) for more information.
- Write **unit tests** for all your custom code and store them in the `tests` directory. You can use any Python testing framework you like, for example `pytest` or `unittest`.
- Consider writing **integration tests** for custom functions that connect to external tools and store them in the `tests` directory. You can use any Python testing framework you like, for example `pytest` or `unittest`.

You can run all tests stored in the `tests` directory with the `astro dev pytest` command and integrate this command into your CI/CD pipelines. For more information on testing Airflow DAGs see [Test Airflow DAGs](https://docs.astronomer.io/learn/testing-airflow).

### Key DAG writing best practices for Astro

When writing Airflow DAGs for Astro, it is recommended that all of your DAGs have the following characteristics:

- **Docstring up front**: Include a docstring at the top of your DAG file that describes the purpose of the DAG, the author, and any other relevant information. This will help other data practitioners understand the purpose of the DAG and how to use it. Convert the docstring to a [DAG Doc](https://docs.astronomer.io/learn/custom-airflow-ui-docs-tutorial) by setting `doc_md=__doc__` in the DAG definition.
- **Define an owner**: In the `default_args` dictionary, define the `owner` key with the name of the person responsible for the DAG. This will help other data practitioners know who to contact if they have questions about the DAG. Note that you can link the owner to any address by setting the DAG parameter `owner_links` to a dictionary with the owner name as the key and the desired link as the value.
- **Use tags**: Use tags to categorize your DAGs. The Astro UI allows you to filter DAGs by tags across all deployments in a workspace.
- **Set retries**: It is an important Airflow best practice to set the `retries` parameter in the `default_args` dictionary to a value greater than 0. This will allow your tasks to retry if they fail. If you do not want a specific task to retry, you can override the `retries` parameter in the task definition.

Writing Airflow tasks for Astro is similar to writing tasks for any Airflow deployment and general [Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) apply. When writing DAGs for Astro you can also leverage the following features:

- The [Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables) to manage your connections. This allows you to define connections once and use them in multiple deployments (with or without overrides for individual fields), as well in your local development environment. Connections in the Environment Manager are stored in the Astronomer managed secrets backend.
- [Deployment environment variables](environment-variables.md) to store environment variables. You can mark variables as secret to be stored in the Astronomer managed secrets backend. You can store [Airflow variables](https://docs.astronomer.io/learn/airflow-variables) as environment variables as well, by using the format `AIRFLOW_VAR_MYVARIABLENAME`.
- [Worker queues](https://docs.astronomer.io/astro/configure-worker-queues) to optimize task execution efficiency. Worker queues allow you to define sets of workers with specific resources that execute tasks in parallel. You can assign tasks to specific worker queues to optimize resource usage. This feature is an improvement over OSS Airflow pools, which only manage concurrency and not resources. You can use both worker queues and pools in combination.
- [Astro Alerts](alerts.md) to set up alerts for your DAGs. For more information, see [When to use Airflow or Astro alerts for your pipelines on Astro](airflow-vs-astro-alerts.md).

### Kubernetes and Astro

On Astro, Airflow runs on Kubernetes. To run Airflow tasks in dedicated Kubernetes pods you have two options:

- Use the **Kubernetes Executor**: On Astro you can switch to the Kubernetes Executor in the deployment settings. This will run all tasks running in a deployment in dedicated Kubernetes pods. See [Manage Airflow executors on Astro](executors-overview.md).
- Use the **KubernetesPodOperator**: If you are using the Celery Executor, you can use the KubernetesPodOperator to run specific tasks in dedicated Kubernetes pods. You can run your tasks on the same cluster as your Airflow deployment by using the `in_cluster` parameter, or on a different cluster by using the `cluster_context` parameter. See [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md).

## Example 

This example show a simple DAG that follows the best practices for writing Airflow DAGs for Astro.

### Prerequisites

- At least one [Astro Deployment](create-deployment.md) with at least one [worker queue](https://docs.astronomer.io/astro/configure-worker-queues) defined.
- An [Astro project](https://docs.astronomer.io/astro/cli/overview) initialized with the Astro CLI. If you do not have a project ready you can fork the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

### Implementation

1. Create a new DAG file in the `dags` directory of your Astro project.
2. Create a DAG definition with the following characteristics:

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

3. Add at least one task to your DAG definition. Set the `queue` parameter to assign the task to a specific worker queue. 
4. Configure the pre-existing DAG validation tests in the `tests/dags` directory for your needs. A common test is to enforce the `catchup` parameter is set to `False`:

    ```python
    @pytest.mark.parametrize(
        "dag_id,dag, fileloc", get_dags(), ids=[x[2] for x in get_dags()]
    )
    def test_dag_has_catchup_false(dag_id, dag, fileloc):
        """
        test if a DAG has catchup set to False
        """
        assert (
            dag.catchup == False
        ), f"{dag_id} in {fileloc} must have catchup set to False."
    ```

5. Add unit tests for your custom code and functions to the `tests` directory. See [Test Airflow DAGs](https://docs.astronomer.io/learn/testing-airflow) for more information and examples.
6. Use `astro dev pytest` to run all tests in the `tests` directory locally and integrate this command into your [CI/CD pipeline](set-up-ci-cd.md).
7. Add any connections needed in your DAG in the [Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables).
8. Add any environment variables needed in your DAG as [deployment environment variables](environment-variables.md).
9. Configure a **DAG Failure** alert for your DAG. Use the communication channel of your choice. See [Set up Astro alerts](https://docs.astronomer.io/astro/alerts).

## See also 

- Webinar: [Best practices for managing Airflow across teams](https://www.astronomer.io/events/webinars/best-practices-for-managing-airflow-across-teams-video/).
- Webinar: [DAG writing for data engineers and data scientists](https://www.astronomer.io/events/webinars/dag-writing-for-data-engineers-and-data-scientists-video/).
- OSS Learn guide: [DAG writing best practices in Apache Airflow](https://docs.astronomer.io/learn/dag-best-practices).