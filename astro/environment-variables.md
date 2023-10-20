---
sidebar_label: 'Overview'
title: 'Environment variables'
id: environment-variables
description: Overview of environment variables on Astro
---

import {siteVariables} from '@site/src/versions';

On Astro, an _Environment Variable_ is a key-value configuration stored in a configuration file that applies to a specific Deployment. You can use environment variables to configure custom environment variables for your Deployment, customize core settings of Airflow and its pre-installed providers, or store Airflow connections and variables.

Some scenarios where you might use custom environment variables for your Deployment include:

- Adding a token or a URL that is required by your Airflow DAGs or tasks
- Integrating with Datadog or other third-party tooling to [export Deployment metrics](deployment-metrics.md#export-airflow-metrics-to-datadog)
- Customizing your DAG flows by identifiyng a production Deployment versus a development Deployment

Some examples of customizing core settings of Airflow or any of its pre-installed providers include:

- Changing the import timeout of DAGBag using `AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT`.
  See all [core settings of Airflow](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) that can be customized.
- Setting up an SMTP service to receive [Airflow alerts](airflow-email-notifications.md) by email.

You can also use environment variables to store [Airflow connections](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables) and [variables](https://docs.astronomer.io/learn/airflow-variables#using-environment-variables).

Some environment variables on Astro are set globally and cannot be overridden for individual Deployments, while others are used by Astro Runtime to enhance your Airflow experience. For more information on these, see [Global environment variables](platform-variables.md).

## Choose a strategy

Environment variables are fundamentally used to customize your Airflow environment on Astro to take advantage of different performance, behavior, and connection options available. In order to choose the right management and implementation strategy for your needs, you must understand the available management options, how Astro prioritizes environment variables, and how Astro stores them. 

### Management options

On Astro, you can manage environment variables on Astro in four different ways for your Deployment:

- Your Deployment's **Variable** tab [in the Cloud UI](env-vars-astro.md#using-the-cloud-ui)
- Your Astro project's [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) during the Astro build and deploy process
- Using the [Astro CLI](env-vars-astro.md#using-astro-cli)
  - Your Astro project's `.env` file
  - Using Astro CLI commands `astro deployment variable create` and `astro deployment variable update`

You can also override existing environment variables defined in your `Dockerfile` using the Cloud UI. Environment variables defined in the Cloud UI take precedence over the ones defined in your `Dockerfile`. When you use Astro CLI to upload environment variables, they are also stored in the Cloud UI.

For example, if you have set `AIRFLOW__CORE__PARALLELISM` in your `Dockerfile` but want to use a different value for testing, you can define the same in the Cloud UI to override the original value in your `Dockerfile`.

### Storing environment variables

Astro stores non-secret environment variables set in the Cloud UI in a database that is hosted and managed by Astronomer. However, the Cloud UI also allows you to mark your environment variables as secret. When you configure a secret environment variable in the Cloud UI, the following methodology is used:

1. Astro generates a manifest that defines a Kubernetes secret, named `env-secrets`, that contains your variable's key and value.
2. Astro applies this manifest to your Deployment's namespace.
3. After the manifest is applied, the key and value of your environment variable are stored in a managed [etcd cluster](https://etcd.io/) at rest within Astro.

This process occurs every time you update the environment variable's key or value. To use a secret environment variable value in a task running on the Kubernetes executor or the KubernetesPodOperator, you need to mount the value from the Astro Kubernetes secret to your Kubernetes Pod. See:

- [Mount secret environment variables to worker pods](kubernetes-executor.md#mount-secret-environment-variables-to-worker-pods)
- [Use secret environment variables with the KubernetesPodOperator](kubernetespodoperator.md#use-secret-environment-variables-with-the-kubernetespodoperator)

:::caution

Environment variables marked as secret are stored securely by Astronomer and are not shown in the Cloud UI. However, it's possible for a user in your organization to create or configure a DAG that exposes secret values in Airflow task logs. Airflow task logs are visible to all Workspace members in the Airflow UI and accessible in your Astro cluster's storage.

To avoid exposing secret values in task logs, instruct users to not log environment variables in DAG code.

:::

### Recommended methods

Astronomer recommends using the Cloud UI to store your environment variables because it provides you:

- Ease of use
- Security for your secret variables
- Visibility into your Airflow environment, without having to print environment variables in your task
- Ability to export using Astro CLI

However, there are scenarios based on your specific use case when you might want to use a mix of methods or strategies other than the Cloud UI. 

The following table describes recommended methods for different scenarios.

| Scenario                                                                                                                                                                                                                                                                     | Recommended method                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| You are a new Astro user. You just created a Deployment and want to integrate your Hashicorp Vault secrets backend to test DAGs.                                                                                                                                             | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use and visibilty.                                                                                                                                                                                   |
| Your team has dev/prod/staging environments and you use an `ENVIRONMENT_TYPE` environment variable in your DAGs to customize the file, bucket, or database schema names.                                                                                                     | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility.                                                                                                                                                                                                  |
| Your team has dev/prod/staging environments and you use various environment variables to customize your Airflow environment.                                                                                                                                                 | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to keep different environments in sync.                                                                                                                                                                   |
| You want to ensure all the environment variables defined in the Cloud UI are checked-in to the code repository and bundled in an Astro project before you promote your code from a lower environment (development) to a higher environment (staging or integration or prod). | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to version control your environment configuration.                                                                                                                                                        |
| Your are part of a production support team analyzing DAG failures and want to turn on Debug logging temporarily.                                                                                                                                                             | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use.                                                                                                                                                                                                 |
| You develop DAGs locally with a new source, and want to use a secret credential in these DAGs.                                                                                                                                                                               | [Use `.env` file](env-vars-astro.md#using-astro-cli). This allows you to avoid accidentally checking in credentials to the code repository because `.env` is part of `.gitignore`. This `.env` file can be easily applied to your Deployment using the Astro CLI. |
| You use environment variables to store your Airflow connections and variables, and have to configure these from one Deployment to another based on the environment type.                                                                                                     | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility.                                                                                                                                                                                                  |
| You want the features of the Cloud UI for environment variables, but you also keep track of the non-secret environment variables in your code repository.                                                                                                                    | Use [Astro CLI](env-vars-astro.md#in-your-astro-deployment) to write an automation script to add or update the non-secret environment variables in your Deployment from your code repository.                                                                     |

