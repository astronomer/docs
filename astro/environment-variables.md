---
sidebar_label: 'Overview'
title: 'Environment variables'
id: environment-variables
description: Overview of environment variables on Astro
---

import {siteVariables} from '@site/src/versions';

On Astro, an _Environment Variable_ is a key-value configuration stored in a configuration file that applies to a specific Deployment. You can use environment variables to configure custom environment variables for your Deployment, customize core settings of Airflow and its pre-installed providers, or store Airflow connections and variables.

Some scenarios where you might use environment variables in your Deployment include:

- Adding a token or a URL that is required by your Airflow DAGs or tasks.
- Integrating with Datadog or other third-party tooling to [export Deployment metrics](deployment-metrics.md#export-airflow-metrics-to-datadog).
- Specifying a tag that's added to all resources created by the Deployment and indicates whether a resource is for development or production.

Some examples of customizing core settings of Airflow or any of its pre-installed providers include:

- Changing the import timeout of DAGBag using `AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT`.
- Setting up an SMTP service to receive [Airflow alerts](airflow-email-notifications.md) by email.

You can also use environment variables to store [Airflow connections](https://docs.astronomer.io/learn/connections#define-connections-with-environment-variables) and [variables](https://docs.astronomer.io/learn/airflow-variables#using-environment-variables).

Some environment variables on Astro are set globally and cannot be overridden for individual Deployments, while others are used by Astro Runtime to enhance your Airflow experience. For more information on these, see [Global environment variables](platform-variables.md).

## Choose a strategy

Environment variables can be used in many different contexts on Airflow. To choose the right management and implementation strategy for your specific use case, it's helpful to know how Astro prioritizes and stores environment variables for each available management option.

### Management options

On Astro, you can manage environment variables from two different locations:

- Your Deployment's **Variables** tab in the Cloud UI. This is the fastest and easiest way to set an environment variable. See [Using the Cloud UI](env-vars-astro.md#using-the-cloud-ui) for setup steps.
- Your Astro project `Dockerfile`. Storing environment variables in your Dockerfile allows you to manage them as code in a version control tool like GitHub. However, environment variables stored in the Dockerfile do not appear in the Cloud UI and might be harder to reference from DAG code.  Using the Dockerfile is recommended for more complex production use cases, such as implementing a secrets backend. See [Using your Dockerfile](env-vars-astro.md#using-your-dockerfile) for setup steps. 

At the local development level, you can use your Astro project `.env` file to set and test environment variables. When you're ready to push these environment variables to a Deployment, you can use the Astro CLI to export and store them in the Cloud UI for your Deployment. 


### How environment variables are stored in the Cloud UI

When you set a non-secret environment variable in the Cloud UI, Astronomer stores the variable in a database that is hosted and managed by Astronomer. 

When set a secret environment variable in the Cloud UI, the following happens:

1. Astro generates a manifest that defines a Kubernetes secret, named `env-secrets`, that contains your variable's key and value.
2. Astro applies this manifest to your Deployment's namespace.
3. After the manifest is applied, the key and value of your environment variable are stored in a managed [etcd cluster](https://etcd.io/) at rest within Astro.

This process occurs every time you update the environment variable's key or value.

:::caution

Environment variables marked as secret are stored securely by Astronomer and are not shown in the Cloud UI. However, it's possible for a user in your organization to create or configure a DAG that exposes secret values in Airflow task logs. Airflow task logs are visible to all Workspace members in the Airflow UI and accessible in your Astro cluster's storage.

To avoid exposing secret values in task logs, instruct users to not log environment variables in DAG code.

:::

### Environment variable priority

On Astro, environment variables set in the Cloud UI take precedence over environment variables set in your Dockerfile.

For example, if you set `AIRFLOW__CORE__PARALLELISM` with one value in the Cloud UI and you set the same environment variable with another value in your `Dockerfile`, the value set in the Cloud UI takes precedence. 

Similarly, in local development, environment variables set in your `.env` file take precedence over environment variables set in your Dockerfile.

### Example use cases

For most use cases, Astronomer recommends using the Cloud UI to store your environment variables for the following reasons:

- It's easy to use.
- It has built-in security for secret environment variables.
- You can import and export environment variables using the Astro CLI.

There are some scenarios when you might want to use a mix of methods or strategies other than the Cloud UI. The following table prescribes specific methods for various common use cases.

| Scenario                                                                                                                                                                                                                                                                     | Recommended method                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| You are a new Astro user. You just created a Deployment and want to integrate your Hashicorp Vault secrets backend to test DAGs.                                                                                                                                             | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use and visibilty.                                                                                                                                                                                   |
| Your team has multiple environment types and you use an `ENVIRONMENT_TYPE` environment variable in your DAGs to customize the file, bucket, or database schema names.                                                                                                     | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility.                                                                                                                                                                                                  |
| You want to standardize a core set of Airflow environment configurations across multiple environments.                                                                                                                                                | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to have a file that serves as a source of truth and starting point for all environments.                                                                                                                                                                |
| You want to use version control to manage your environment variables from a code repository. | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to version control your environment configuration.                                                                                                                                                        |
| You want to carry over environment variables when you promote code from a development environment to a production environment. | [`Dockerfile`](env-vars-astro.md#using-your-dockerfile) to deploy environment variables from project code using CI/CD.                                                                                                                                                        |
| You are part of a production support team analyzing DAG failures and want to turn on debugging-related environment variables temporarily.                                                                                                                                                             | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for ease of use.                                                                                                                                                                                                 |
| You're developing locally, and you want to use a secret credential in your DAGs.                                                                                                                                                                               | [Use the `.env` file](env-vars-astro.md#using-astro-cli) locally. This allows you to avoid accidentally sending credentials to your code repository because `.env` is part of `.gitignore`. You can then export the `.env` file to your Deployment using the Astro CLI. |
| You use environment variables to store your Airflow connections and variables, and you have to reconfigure these between Deployments based on the environment type.                                                                                                     | [Cloud UI](env-vars-astro.md#using-the-cloud-ui) for visibility.                                                                                                                                                                                                  |
| You want the features of the Cloud UI for environment variables, but you also keep track of the non-secret environment variables in your code repository.                                                                                                                    | Use the [Astro CLI](env-vars-astro.md#in-your-astro-deployment) and an automation script to add or update the non-secret environment variables in your Deployment from your code repository.                                                                     |

