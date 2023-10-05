---
sidebar_label: 'Overview'
title: 'Environment variables'
id: environment-variables
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

On Astro, you can manage environment variables on Astro in four different ways for your Deployment:

- [Your Deployment's **Variable** tab in the Cloud UI](env-vars-astro.md#using-the-cloud-ui)
- [Your Astro project's `Dockerfile`](env-vars-astro.md#using-your-dockerfile) during the Astro build and deploy process
- [Using Astro CLI](env-vars-astro.md#using-astro-cli)
    - Your Astro project's `.env` file
    - Using Astro CLI commands `astro deployment variable create` and `astro deployment variable update`

You can also override existing environment variables defined in your `Dockerfile` using the Cloud UI. Environment variables defined in the Cloud UI take precedence over the ones defined in your `Dockerfile`. When you use Astro CLI to upload environment variables, they are also stored in the Cloud UI.

For example, if you have set `AIRFLOW__CORE__PARALLELISM` in your `Dockerfile` but want to use a different value for testing, you can define the same in the Cloud UI to override the original value in your `Dockerfile`.

### How Astro stores your environment variables 

Non-secret environment variables set in the Cloud UI are stored in a Hashicorp Vault secrets manager hosted in Astro control plane. These environment variables are available to your Astro Deployment’s Kubernetes namespace as a Kubernetes secret.

To use these environment variables in an Astro Deployment:
- In a regular PythonOperator or Python code, you can use `os.environ` method.
- If you can’t use Python or are using a pre-defined code that expects specific keys for environment variables, you need to mount the secret environment variables using BaseOperator’s `executor_config` by providing a `pod_override`. See [Use secret environment variables in worker Pods](kubernetes-executor.md#mount-secret-environment-variables-to-worker-pods).
- If you need to use these secret environment variables in a KubernetesPodOperator, see [Use secret environment variables with KubernetesPodOperator](kubernetespodoperator.md#use-secret-environment-variables-with-the-kubernetespodoperator).

:::caution

Environment variables marked as secret are stored securely by Astronomer and are not shown in the Cloud UI. However, it's possible for a user in your organization to create or configure a DAG that exposes secret values in Airflow task logs. Airflow task logs are visible to all Workspace members in the Airflow UI and accessible in your Astro cluster's storage.

To avoid exposing secret values in task logs, instruct users to not log environment variables in DAG code.

:::


### Choose a method or methods to manage environment variables

The Cloud UI provides you the following benefits to manage your environment variables:

- Ease of use
- Security for your secret variables
- Visibility into your Airflow environment, without having to print environment variables in your task
- Ability to export using Astro CLI

However, there are scenarios based on your specific use case when you might want to follow a different method or a mix of strategies. The following table describes some of the common scenarios and the recommended methods:

| Scenario | Recommended method | 
|----------|--------------------|
| You are a new Astro user, have just created a Deployment and want to integrate your Vault secrets backend to test few DAGs. | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use and visibilty. | 
| Your team has production and non-production environments and you use an `ENVIRONMENT_TYPE` environment variable in your DAGs to customize the file, bucket, or database schema names. | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility. |
| Your team uses different Airflow configurations to customize your production Deployment and non-production Deployment. For example, different parallelism and max_active_runs_per_dag settings across teams for production and staging. | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to keep the settings in code repository for easy reference and sync. |
| You want to ensure all the environment variables defined in the Cloud UI of your development environment should be committed to the code repository and bundled in an Astro project before you promote your code to a higher environment (staging or integration or production) | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to version control your environment configuration. | 
| Your are part of the production support team analyzing the DAG failures and want to temporarily turn on Debug logging. | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use. | 
| You locally develop a couple of DAGs with a new source system and want to use a secret or credential in these DAGs. | [Use `.env` file](env-vars-astro.md#using-astro-cli). This will allow you to avoid accidentally checking in credentials to the code repository because `.env` is part of `.gitignore`. This `.env` file can be easily applied to your Deployment using Astro CLI.  | 
| You use environment variables to store your Airflow connections and variables, and have to configure these from one Deployment to another based on the environment type | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility. | 
| You want the visibility and ability to edit environment variables from the Cloud UI, and you also want to keep track of the non-secret environment variables in your code repository. | Use [Astro CLI](env-vars-astro.md#in-your-astro-deployment) to write an automation script to add or update the environment variables. | 