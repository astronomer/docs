---
sidebar_label: 'Overview'
title: 'Environment variables'
id: env-vars-overview
description: Overview of environment variables on Astro
---

import {siteVariables} from '@site/src/versions';

On Astro, an _Environment Variable_ is a key-value configuration stored in a configuration file that applies to a specific Deployment. You can use environment variables to configure custom environment variables for your Deployment, customize core settings of Airflow and its pre-installed providers, or store Airflow connections and variables.

To configure custom environment variables for your Deployment, some examples include:
- Identify a production Deployment versus a development Deployment allowing you to customize your DAG flow.
- Add a token or a URL that is required by your Airflow DAGs or tasks
- Integrate with Datadog or other third-party tooling to [export Deployment metrics](deployment-metrics.md#export-airflow-metrics-to-datadog).

To customize core settings of Airflow or any of its pre-installed providers, some examples are:
- Change the import timeout of DAGBag using `AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT`. See all [core settings of Airflow](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) that can be customized.
- Set up an SMTP service to receive [Airflow alerts](airflow-email-notifications.md) by email.

You can also use environment variables to store [Airflow connections](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables) and [variables](https://docs.astronomer.io/learn/airflow-variables#using-environment-variables).

Some environment variables on Astro are set globally and cannot be overridden for individual Deployments, while others are used by Astro Runtime to enhance your Airflow experience. For more information on these, see [Global environment variables](platform-variables.md).

## Choose how to manage environment variables

Environment variables are fundamentally used to customize your Airflow environment on Astro to take advantage of different performance, behavior, and connection options available. In order to choose the right management and implementation strategy for your needs, you must understand the available management options, how Astro prioritizes environment variables, and how Astro stores them. 

### Ways to manage environment variables on Astro

On Astro, you can manage environment variable in four different ways for your Deployment:

- [Your Deployment's **Variable** tab in the Cloud UI](env-vars-astro.md#using-the-cloud-ui)
- [Your Astro project's `Dockerfile`](env-vars-astro.md#using-your-dockerfile) during the Astro build and deploy process
- [Using Astro CLI](env-vars-astro.md#using-astro-cli)
    - Your Astro project's `.env` file
    - Using Astro CLI commands `astro deployment variable create` and `astro deployment variable update`

### How Astro prioritizes environment variables

On Astro, environment variables are applied and overridden in the following order:

- [Cloud UI](env-vars-astro.md#using-the-cloud-ui)
- [.env (local development only)](env-vars-astro.md#in-your-local-airflow-environment)
- [Dockerfile](env-vars-astro.md#using-your-dockerfile)

For example, if you set `AIRFLOW__CORE__PARALLELISM` with one value in the Cloud UI and you set the same environment variable with another value in your `Dockerfile`, the value set in the Cloud UI takes precedence.

### How Astro stores your environment variables 

The Cloud UI allows you to mark your environment variables as secret. Astro stores non-secret environment variables set in the Cloud UI in a database that is hosted and managed by Astronomer. When you configure a secret environment variable in the Cloud UI, the following methodology is used:

1. Astro generates a manifest that defines a Kubernetes secret, named `env-secrets`, that contains your variable's key and value.
2. Astro applies this manifest to your Deployment's namespace.
3. After the manifest is applied, the key and value of your environment variable are stored in a managed [etcd cluster](https://etcd.io/) at rest within Astro.

This process occurs every time you update the environment variable's key or value. To use a secret environment variable value in a task running on the Kubernetes executor or the KubernetesPodOperator, you need to mount the value from the Astro kubernetes secret to your Kubernetes Pod. See:

- [Mount secret environment variables to worker pods](kubernetes-executor.md#mount-secret-environment-variables-to-worker-pods)
- [Use secret environment variables with the KubernetesPodOperator](kubernetespodoperator.md#use-secret-environment-variables-with-the-kubernetespodoperator)

:::caution

Environment variables marked as secret are stored securely by Astronomer and are not shown in the Cloud UI. However, it's possible for a user in your organization to create or configure a DAG that exposes secret values in Airflow task logs. Airflow task logs are visible to all Workspace members in the Airflow UI and accessible in your Astro cluster's storage.

To avoid exposing secret values in task logs, instruct users to not log environment variables in DAG code.

:::


### Choose the strategy to manage environment variables

Astronomer recommends using the Cloud UI to store your environment variables because it provides you:

- Ease of use
- Security for your secret variables
- Visibility into your Airflow environment, without having to print environment variables in your task
- Ability to export using Astro CLI

There are scenarios based on your specific use case when you might want to follow a different strategy or a mix of strategies. The following table describes recommended methods for particular scenarios.

| Scenario | Recommended method | 
|----------|--------------------|
| You are a new Astro user, have just created a Deployment and want to integrate your Vault secrets backend to test few DAGs. | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use and visibilty. | 
| Your team has dev/prod/staging environments and you use an `ENVIRONMENT_TYPE` environment variable in your DAGs to customize the file, bucket, or database schema names. | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility. |
| Your team has dev/prod/staging environments and you use various environment variables to customize your Airflow environment. | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to keep different environments in sync. |
| You want to ensure all the environment variables defined in the Cloud UI are checked-in to the code repository and bundled in an Astro project before you promote your code from a lower environment (development) to a higher environment (staging or integration or prod) | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to version control your environment configuration. | 
| Your are part of the production support team analyzing the DAG failures and want to turn on Debug logging temporarily | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use. | 
| You locally develop a couple of DAGs with a new source and want to use a secret or credential in these DAGs. | [Use `.env` file](env-vars-astro.md#using-astro-cli). This allows you to avoid accidentally checking in credentials to the code repository because `.env` is part of `.gitignore`. This `.env` file can be easily applied to your Deployment using Astro CLI | 
| You use environment variables to store your Airflow connections and variables, and have to configure these from one Deployment to another based on the environment type | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility. | 
| You want the features of the Cloud UI for environment variables, and you also keep track of the non-secret environment variables in your code repository. | Use [Astro CLI](env-vars-astro.md#in-your-astro-deployment) to write an automation script to add or update the environment variables. | 