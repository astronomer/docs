---
title: "Manage Airflow code"
sidebar_label: "Manage Airflow code"
id: managing-airflow-code
description: "Learn best practices for Airflow project organization, such as when to separate out DAGs into multiple projects and how to manage code used across different projects."
---

One of the tenets of Apache Airflow is that pipelines are defined as code. This allows you to treat your pipelines as you would any other piece of software and use best practices such as version control and CI/CD. As you scale the use of Airflow within your organization, it becomes important to manage your Airflow code in a way that is organized and sustainable.

In this guide, you'll learn how to organize your Airflow projects, when to separate your DAGs into multiple projects, how to manage code that is used in different projects, and review a typical development flow.

Throughout this guide, the term project is used to denote any set of DAGs and supporting files that are deployed to a single Airflow Deployment. For example, your organization might have a finance team and a data science team each with their own separate Airflow deployment, and they each have a separate Airflow project that contains all of their code.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: Local Development Environment](https://academy.astronomer.io/path/airflow-101/local-development-environment).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## Project structure

When working with Airflow, a consistent project structure helps keep all DAGs and supporting code organized and easy to understand, and it makes it easier to scale Airflow horizontally within your organization. 

The ideal setup is to keep one directory and repository for each project. This means that you can use a version control tool such as Github or Bitbucket to package everything together. 

Astronomer uses the following project structure:

```bash
.
├── dags                        # Folder where all your DAGs go
│   ├── example-dag.py
│   └── redshift_transforms.py
├── Dockerfile                  # For Astronomer's Docker image and runtime overrides
├── include                     # For any scripts that your DAGs might need to access
│   └── sql
│       └── transforms.sql
├── packages.txt                # For OS-level packages
├── plugins                     # For any custom or community Airflow plugins
│   └── example-plugin.py
└── requirements.txt            # For any Python packages
```

To create a project with this structure automatically, install the [Astro CLI](https://www.astronomer.io/docs/astro/install-cli) and initialize a project with `astro dev init`.

If you are not running Airflow with Docker or have different requirements for your organization, your project structure might look different. Choose a structure that works for your organization and keep it consistent so that anyone working with Airflow can easily transition between projects without having to re-learn a new structure.

## When to separate projects

The most common setup for Airflow projects is to keep all code for a given deployment in the same repository. However, there are some circumstances where it makes sense to separate DAGs into multiple projects. In these scenarios, it's best practice to have a separate Airflow deployment for each project. You might implement this project structure for the following reasons:

- Access control: Role-based access control (RBAC) should be managed at the Airflow Deployment level and not at the DAG level. If Team A and Team B should only have access to their own team's DAGs, it would make sense to split them up into two projects and deployments.
- Infrastructure considerations: If you have a set of DAGs that are well suited to the Kubernetes executor and another set that are well suited to the Celery executor, you may want to separate them into two different projects that feed Airflow deployments with different infrastructure. See [Configure Deployment resources](https://www.astronomer.io/docs/astro/configure-deployment).
- Dependency management: If DAGs have conflicting Python or OS dependencies, one way of managing this can be separating them into separate projects so they are isolated from one another.

Occasionally, some use cases require DAGs from multiple projects to be deployed to the same Airflow deployment. This is a less common pattern and is not recommended for project organization unless it is specifically required. In this case, deploying the files from different repositories together into one Airflow deployment should be managed by your CI/CD tool. If you are implementing this use case with Astronomer Software, you will need to use the [NFS](https://www.astronomer.io/docs/software/deploy-nfs) or [Git-Sync](https://www.astronomer.io/docs/software/deploy-git-sync) deployment methods.  

## Reusing code

Code, such as custom hooks, operators, or DAG templates that are reused between projects, should be stored in a repository that's separate from your individual project repositories. This ensures that any changes to the re-used code only need to be made once and are applied across all projects where that code is used. See [Sharing code across projects](https://www.astronomer.io/docs/learn/sharing-code-multiple-projects) for more on how to structure and set up a project for shared code.

You can pull code from separate repositories into your Airflow projects. If you are working with Astronomer, see [Install Python packages from private sources](https://www.astronomer.io/docs/astro/cli/private-python-packages) for Astro or [Customize your image on Astronomer Software](https://www.astronomer.io/docs/software/customize-image#build-from-a-private-repository) for Software. Depending on your repository setup, it may also be possible to manage this with your CI/CD tool.

## Development flow

You can extend the project structure to work for developing DAGs and promoting code through `dev`, `QA`, and `production` environments. The most common method for managing code promotion with this project structure is to use branching. You still maintain one project and repository, and create `dev` and `qa` branches for any code in development or testing. Your `main` branch should correspond to code that is deployed to production. You can then use your CI/CD tool to manage promotion between these three branches. For more on this, see [Configure CI/CD on Astronomer Software](https://www.astronomer.io/docs/software/ci-cd).

There are many ways of implementing a development flow for your Airflow code. For example, you might work with feature branches instead of a specific `dev` branch. How you choose to implement this will depend on the needs of your organization, but the method described here is a good place to start if you aren't currently using CI/CD with Airflow.
