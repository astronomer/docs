---
sidebar_label: 'Get started'
title: 'Get started with the Astro CLI'
id: get-started
description: Install the Astro CLI, the best way to run Apache Airflow and test data pipelines on your local machine.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

The Astro CLI is an open source command line for modern data orchestration. It is the easiest way to run Apache Airflow on your machine. By the end of this quickstart, you'll have an Airflow environment running locally with just a few commands. From there, you can start building your project with your own DAGs, dependencies, and tests.

## Step 1: Install the Astro CLI

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

#### Prerequisites

To use the Astro CLI on Mac, you must have:

- [Homebrew](https://brew.sh/)
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

#### Installation

To install the latest version of the Astro CLI, run the following command:

```sh
brew install astro
```

</TabItem>

<TabItem value="windows">

#### Prerequisites

To use the Astro CLI on Windows, you must have:

- [Docker Desktop](https://docs.docker.com/desktop/windows/install/) for Windows.
- [Docker Engine](https://docs.docker.com/engine/install/) (v0.18.9 or higher).
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) enabled on your local machine.
-  Windows 10 or Windows 11.

#### Installation

1. Go to the [**Releases** page of the Astro CLI GitHub repository](https://github.com/astronomer/astro-cli/releases). Based on your desired CLI version and the CPU architecture of your machine, download one of the `.zip` files available on this page.

    For example, to install v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, download `astro_1.0.0-converged_windows_amd64.zip`.

2. If the `.zip` file does not automatically unzip, run the following command to unzip the executable:

    ```sh
    tar -xvzf .\astrocli.tar.gz
    ```

3. Add the filepath for the directory containing `astro.exe` as a PATH environment variable. For example, if `astro.exe` was stored in `C:\Users\username\astro.exe`, you would add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [Java documentation](https://www.java.com/en/download/help/path.html).

4. Restart your machine.

</TabItem>

<TabItem value="linux">

#### Prerequisites

To use the Astro CLI on Linux, you must have:

- [Docker Engine](https://docs.docker.com/engine/install/) (v0.18.9 or higher).

#### Installation

Run the following command to install the latest version of the Astro CLI directly to `PATH`:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

</TabItem>

</Tabs>

## Step 2: Confirm the install

To confirm the CLI was installed properly, run the following CLI command:

```sh
astro version
```

If the installation was successful, you should see the following output:

<pre><code parentName="pre">{`% astro version
Astro CLI Version: ${siteVariables.cliVersion}`}</code></pre>

## Step 3: Create an Astro project

To start developing locally, you first need to create an Astro project, which contains all of the files you need to run Apache Airflow locally.

To create a new Astro project:

1. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

2. Open the directory:

    ```sh
    cd <your-astro-project-name>
    ```

3. Initialize an Astro project in the directory:

    ```sh
    astro dev init
    ```

    This Astro CLI command generates all of the necessary files to run Airflow locally in your new directory. This includes dedicated folders for your DAG files, plugins, and dependencies.

## Step 4: Run Airflow locally

To confirm that you successfully initialized an Astro project, run the following command from your project directory:

```sh
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with [deferrable operators](deferrable-operators.md)

## Step 5: Access the Airflow UI

Once your project builds successfully, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password.

After logging in, you should see two example DAGs in the Airflow UI that correspond to two files in the `dags` directory of your Astro project. These example DAGs are maintained by Astronomer and showcase Airflow features and best practices.

<div class="text--center">
<img src="/img/docs/sample-dag.png" alt="Example DAG in the Airflow UI" />
</div>

That's all it takes to run Airflow locally using the Astro CLI! From here, you can add new DAGs to your Astro project and start developing.

## Next steps

Once you install the CLI and have an Astro project running locally, there are a few different paths you can take:

- To write and test your own DAGs locally and configure your local Airflow environment, see [Develop Project](develop-project.md).
- To view logs, set up unit tests for your DAGs, or troubleshoot your local Airflow environment, see [Test and troubleshoot locally](test-and-troubleshoot-locally.md).
- To deploy DAGs to an environment managed by Astronomer, see [Deploy code](deploy-code.md). If you're not a customer but might be interested in Astro, [reach out to us](https://www.astronomer.io/get-started).
- To learn more about the available commands in the CLI, see the [CLI command reference](cli/reference.md) or run `astro help`.
