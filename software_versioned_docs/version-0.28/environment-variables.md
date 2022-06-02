---
sidebar_label: 'Environment Variables'
title: 'Set Environment Variables on Astronomer Software'
id: environment-variables
description: Manage environment variables on Astronomer Software.
---

## Overview

Environment Variables on Astronomer can be used to set both Airflow configurations ([reference here](https://airflow.apache.org/docs/stable/configurations-ref.html)) or custom values, which are then applied to your Airflow Deployment either locally or on Astronomer.

Environment Variables can be used to set any of the following (and much more):

- SMTP to enable email alerts
- Airflow Parallelism and DAG Concurrency
- [A Secret Backend](secrets-backend.md) to manage your Airflow Connections and Variables
- Store Airflow Connections and Variables
- Customize your default DAG view in the Airflow UI (Tree, Graph, Gantt etc.)

This guide will cover the following:

- How to set Environment Variables on Astronomer
- How Environment Variables are stored on Astronomer
- How to store Airflow Connections and Variables as Environment Variables

## Set Environment Variables on Astronomer

On Astronomer, there are 3 ways to set Environment Variables:

- via your `.env` file (_Local Only_)
- via your `Dockerfile`
- via the Software UI

Read below for instructions on how to configure them via all 3 methods.

> **Note:** While Environment Variables on Astronomer are the equivalent of updating your `airflow.cfg`, you are NOT able to bring your own `airflow.cfg` file on Astronomer and configure it directly.

### via `.env` (_Local Only_)

The [Astronomer CLI](cli-quickstart.md) comes with the ability to bring in Environment Variables from a specified `.env` file, which was automatically generated when you initialized an Airflow project on Astronomer via `$ astro dev init`.

To add Environment Variables locally,

1. Find your `.env` file in your Airflow project directory
2. Add your Environment Variables of choice to that `.env` file
3. Rebuild your image to apply those changes by running `$ astro dev start --env .env`

In your `.env` file, insert the value and key, ensuring all-caps for all characters. For example:

```
AIRFLOW__CORE__DAG_CONCURRENCY=5
```

> **Note:** If your Environment Variables contain secrets you don't want to expose in plain-text, you may want to add your `.env` file to `.gitignore` if and when you deploy these changes to your version control tool.

#### Confirm your Environment Variables were Applied

By default, Airflow environment variables are hidden in the Airflow UI for local environments. To confirm your environment variables in the Airflow UI for a local environment, set `AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True` in either your Dockerfile or `.env` file (local only).

Alternatively, you can run:

```
docker ps
```

This will output 3 Docker containers that were provisioned to run Airflow's 3 primary components on your machine: The Airflow Scheduler, Webserver and Postgres Metadata Database.

Now, create a [Bash session](https://docs.docker.com/engine/reference/commandline/exec/#examples) in your scheduler container by running:

```
docker exec -it <scheduler-container-name> /bin/bash
```

If you run `ls -1` following this command, you'll see a list of running files:

```
bash-5.0$ ls -1
Dockerfile             airflow.cfg            airflow_settings.yaml  dags                   include                logs                   packages.txt           plugins                requirements.txt       unittests.cfg
```

Now, run:

```
env
```

This should output all Environment Variables that are running locally, some of which are set by you and some of which are set by Astronomer by default.

> **Note:** You can also run `cat airflow.cfg` to output _all_ contents in that file.

#### Multiple .env Files

The CLI will look for `.env` by default, but if you want to specify multiple files, make `.env` a top-level directory and create sub-files within that folder.

In other words,your project might look like the following:

```
my_project
  ├── Dockerfile
  └──  dags
    └── my_dag
  ├── plugins
    └── my_plugin
  ├── airflow_settings.yaml
  ├── .env
    └── dev.env
    └── prod.env
```

### via your `Dockerfile`

If you're working on an Airflow project locally but intend to deploy to Astronomer and want to commit your Environment Variables to your source control tool, you can set them in your `Dockerfile`. This file was automatically created when you first initialized your Airflow project on Astronomer (via `$ astro dev init`).

> **Note:** Given that this file will be committed upstream, we strongly recommend witholding Environment Variables containing sensitive credentials from your `Dockerfile` and instead inserting them via your `.env` file locally (while adding the file to your `.gitignore`) or setting them as 'secret' via the Software UI, as described in a dedicated section below.

To add Environment Variables, insert the value and key in your `Dockerfile` beginning with `ENV`, ensuring all-caps for all characters. With your Airflow image commonly referenced as a "FROM" statement at the top, your Dockerfile might look like this:

```dockerfile
FROM quay.io/astronomer/ap-airflow:1.10.7-buster-onbuild
ENV AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=1
ENV AIRFLOW__CORE__DAG_CONCURRENCY=5
ENV AIRFLOW__CORE__PARALLELISM=25
```

Once your Environment Variables are added,

1. Run `$ astro dev stop` and `$ astro dev start` to rebuild your image and apply your changes locally OR
2. Run `$ astro deploy` to apply your changes to your running Airflow Deployment on Astronomer

> **Note:** Environment Variables injected via the `Dockerfile` are mounted at build time and can be referenced in any other processes run during the docker build process that immediately follows `$ astro deploy` or `$ astro dev start`.
>
> Environment Variables applied via the Software UI only become available once the docker build process has been completed.

### via the Software UI

The last way to add Environment Variables on Astronomer is to add them via the Software UI. For Environment Variables that you _only_ need on Astronomer and not locally, we'd recommend using this method.

To set them,

1. Navigate to the Software UI
2. Go to "Deployment" > "Variables"
3. Add your Environment Variables

![Astro UI Env Vars Config](https://assets2.astronomer.io/main/docs/astronomer-ui/v0.16-Astro-UI-EnvVars.png)

> **Note:** Input for all configurations officially supported by Airflow are pre-templated, but you're free to specify your own values.

#### Mark Environment Variables as "Secret"

On Astronomer, users have the ability to mark any Environment Variable as "secret" via the UI. For those who have Environment Variables containing potentially sensitive information (e.g. SMTP password, S3 bucket, etc.), we'd recommend leveraging this feature.

To do so from the "Variables" tab,

1. Enter a Key
2. Enter a Value
3. Check the "Secret?" box
4. Click "Add"
5. Press "Deploy Changes"

Once changes are deployed, Environment Variables marked as "secret" will NOT be available in plain-text to any user in the Workspace.

A few additional notes:

- Workspace Editors and Admins are free to set an existing non-secret Env Var to "secret" any time
- To convert a "secret" Env Var to a "non-secret" Env Var, you'll be prompted to enter a new value
- If you export Environment Variables via JSON, "secret" values will NOT render in plain-text
- Users cannot add a new variable that has the same key as an existing variable

Read below for more detail on how Environment Variables are encrypted on Astronomer.

> **Note:** As noted above, Workspace roles and permissions apply to actions in the "Variables" tab. For a full breakdown of permissions for each role, reference Astronomer's ["Roles and Permissions" doc](workspace-permissions.md).

### Precedence amongst 3 Methods

Given the ability to set Environment Variables across 3 different methods potentially simultaneously, it's worth noting the precedence each take.

On Astronomer, Environment Variables will be applied and overridden in the following order:

1. Software UI
2. .env (_Local Only_)
3. Dockerfile
4. Default Airflow Values (`airflow.cfg`)

In other words, if you set `AIRFLOW__CORE__PARALLELISM` with one value via the Software UI and you set the same Environment Variable with another value in your `Dockerfile`, the value set in the Software UI will take precedence.

### How Environment Variables are Stored on Astronomer

All values for Environment Variables that are added via the Software UI are stored as a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/), which is encrypted at rest and mounted to your Deployment's Airflow pods (Scheduler, Webserver, Worker(s)) as soon as they're set or changed.

Environment Variables are _not_ stored in Airflow's Metadata Database and are _not_ stored in Astronomer's platform database. Unlike other components, the Astronomer Houston API fetches them from the Kubernetes Secret instead of the platform's database to render them in the Software UI.

For information on how Airflow Connections and Variables are encrypted on Astronomer, refer to [this forum post](https://forum.astronomer.io/t/how-are-connections-variables-and-env-vars-encrypted-on-astronomer/173).

## Adding Airflow Connections and Variables via Environment Variables

For users who regularly leverage Airflow Connections and Variables, we'd recommend storing and fetching them via Environment Variables.

As mentioned above, Airflow Connections and Variables are stored in Airflow's Metadata Database. Adding them _outside_ of task definitions and operators requires an additional connection to Airflow's Postgres Database, which is called every time the Scheduler parses a DAG (as defined by `processor_poll_interval`, which is set to 1 second by default). By adding Connections and Variables as Environment Variables, you can refer to them more easily in your code and lower the amount of open connections, thus preventing a strain on your Database and resources.

Read below for instructions on both.

### Airflow Connections

The Environment Variable naming convention for Airflow Connections is:

```
ENV AIRFLOW_CONN_<CONN_ID>=<connection-uri>
```

For example, consider the following Airflow Connection:

- Connection ID: `MY_PROD_DB`
- Connection URI: `my-conn-type://login:password@host:5432/schema`

Here, the full Environment Variable would read:

```
ENV AIRFLOW_CONN_MY_PROD_DB=my-conn-type://login:password@host:5432/schema
```

You're free to set this Environment Variable via an `.env` file locally, via your Dockerfile or via the Software UI as explained above. For more information on how to generate your Connection URI, refer to [Airflow's documentation](https://airflow.apache.org/docs/stable/howto/connection/index.html#generating-connection-uri).

### Airflow Variables

The Environment Variable naming convention for Airflow Variables is:

```
ENV AIRFLOW_VAR_<VAR_NAME>=Value
```

For example, consider the following Airflow Variable:

- Variable Name: `My_Var`
- Value: `2`

Here, the Environment Variable would read:

```
ENV AIRFLOW_VAR_MY_VAR=2
```

> **Note:** The ability to store and fetch Airflow Variables was [introduced in Airflow 1.10.10](https://github.com/apache/airflow/pull/7923) and is not available in earlier versions.
