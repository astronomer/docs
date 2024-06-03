---
title: 'Optimize Airflow DAGs for Astro'
sidebar_label: 'DAG writing on Astro'
id: dag-writing-on-astro
---

You can run any valid Airflow DAG on Astro. 

That said, following best practices and taking full advantage of Astro features will help you:

- Produce DAGs more efficiently.
- Improve your development workflow.
- Better organize your deployment and DAGs. 
- Optimize resource usage and task execution efficiency.

While this best practice guide focuses on writing Airflow DAGs for Astro, all [general Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) are also recommended.

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
- [CI/CD on Astro](set-up-ci-cd.md). A recommended architecture for testing and deployment supported by pre-built templates.
- [Worker queues](configure-worker-queues.mdx). A feature of Astro that enables resource optimization beyond what is possible using OSS Airflow.
- [Astro Cloud UI Environment Manager](manage-connections-variables.md). A tool for managing connections across multiple deployments locally and on Astro.
- [Astro alerts](alerts.md). No-code alerting on Astro configurable for various trigger types and communication channels.
- [Kubernetes Executor](executors-overview.md). Supports running Airflow on dedicated Kubernetes pods on Astro.
- [KubernetesPodOperator](kubernetespodoperator.md). Supports running specific tasks in dedicated Kubernetes pods on Astro.

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

If you are unable to install the Astro CLI on your local machine, due to company policy or other reasons, you can use it in GitHub Codespaces by forking the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

:::

Learn more and get started by following the guidance in [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).

### Follow DevOps best practices

Airflow pipelines are code, so all software engineering best practices apply: 

- Store your code in a version control system like [GitHub](https://github.com/).
- Create [dedicated branches for development, staging and production](https://docs.astronomer.io/astro/set-up-ci-cd#multiple-environments).
- Use a CI/CD pipeline to automate testing and deployment. See [Develop a CI/CD workflow for deploying code to Astro](https://docs.astronomer.io/astro/set-up-ci-cd).

![Airflow CI/CD pipeline showing a 3-branch structure with a dev branch corresponding to Local Development, a staging branch corresponding to a staging Deployment and a production branch corresponding to the Production deployment. CI/CD is present at all steps of the workflow.](/img/docs/airflow-cicd-3-branches.png)

Test and validate your Airflow pipelines prior to deployment:

- Write **DAG validation tests** to create rules to, for example, enforce the use of specific operators or allow only certain schedules. Store all validation tests in the `tests` directory.
- Write **unit tests** for all your custom code using your preferred Python testing framework. Popular options include `pytest` and `unittest`. Store all unit tests in the `tests` directory.
- Consider writing **integration tests** for custom functions that connect to external tools and store them in the `tests` directory, as well. A Python testing framework can also be used for this purpose.

You can run all tests stored in the `tests` directory with the `astro dev pytest` command and integrate this command into your CI/CD pipelines. For more information about testing Airflow DAGs, see [Test Airflow DAGs](https://docs.astronomer.io/learn/testing-airflow).

### Follow DAG-writing best practices

We recommend that all your DAGs for Astro have the following characteristics:

- **Docstring up front**: Include a docstring at the top of your DAG file that describes the purpose of the DAG, the author, and any other relevant information. This will help other data practitioners understand the purpose of the DAG and how to use it. Convert the docstring to a [DAG Doc](https://docs.astronomer.io/learn/custom-airflow-ui-docs-tutorial) by setting `doc_md=__doc__` in the DAG definition.
- **Defined owner**: In the `default_args` dictionary, define the `owner` key with the name of the person responsible for the DAG. This will help other data practitioners know whom to contact if they have questions about the DAG. Note that you can link the owner to any address by setting the DAG parameter `owner_links` to a dictionary with the owner name as the key and the desired link as the value.
- **Tags**: Use tags to categorize your DAGs. The Astro UI allows you to filter DAGs by tags across all deployments in a workspace.
- **Retries set**: It is an important Airflow best practice to set the `retries` parameter in the `default_args` dictionary to a value greater than 0. This will allow your tasks to retry if they fail. If you do not want a specific task to retry, you can override the `retries` parameter in the task definition.

### Leverage Astro resources for improved Airflow management

We recommend taking advantage of the following features for easy management of your DAGs:

- **[Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables)** for managing connections. Allows you to define connections once and use them in multiple deployments (with or without overrides for individual fields), as well in your local development environment. Connections in the Environment Manager are stored in the Astronomer managed secrets backend.
- **[Deployment environment variables](environment-variables.md)** for storing environment variables. You can mark variables as secret for storage in the Astronomer managed secrets backend. You can store [Airflow variables](https://docs.astronomer.io/learn/airflow-variables) as environment variables as well by using the format `AIRFLOW_VAR_MYVARIABLENAME`.
- **[Worker queues](https://docs.astronomer.io/astro/configure-worker-queues)** for optimizing task execution efficiency. Worker queues allow you to define sets of workers with specific resources that execute tasks in parallel. You can assign tasks to specific worker queues to optimize resource usage. This feature is an improvement over OSS Airflow pools, which only manage concurrency and not resources. You can use both worker queues and pools in combination.
- **[Astro Alerts](alerts.md)** for setting up alerts for your DAGs. For more information, see [When to use Airflow or Astro alerts for your pipelines on Astro](airflow-vs-astro-alerts.md).

### Kubernetes and Astro

On Astro, Airflow runs on Kubernetes. To run Airflow tasks in dedicated Kubernetes pods you have two options:

- **Kubernetes Executor**: on Astro you can switch to the Kubernetes Executor in the deployment settings. This will run all tasks running in a deployment in dedicated Kubernetes pods. See [Manage Airflow executors on Astro](executors-overview.md).
- **KubernetesPodOperator**: if you are using the Celery Executor, you can use the KubernetesPodOperator to run specific tasks in dedicated Kubernetes pods. You can run your tasks on the same cluster as your Airflow deployment by using the `in_cluster` parameter, or on a different cluster by using the `cluster_context` parameter. See [Run the KubernetesPodOperator on Astro](kubernetespodoperator.md).

## Astro DAG Example 

Create a simple DAG that follows best practices for writing Airflow DAGs for Astro.

### Prerequisites

- At least one [Astro Deployment](create-deployment.md) with at least one [worker queue](https://docs.astronomer.io/astro/configure-worker-queues) defined.
- An [Astro project](https://docs.astronomer.io/astro/cli/overview) initialized with the Astro CLI or a fork of the [Astro CLI Codespaces](https://github.com/astronomer/astro-cli-codespaces) repository.

### Implementation

1. Create a new DAG file in the `dags` directory.
2. Create an empty DAG definition using the Airflow `dag` decorator and the following arguments:

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
