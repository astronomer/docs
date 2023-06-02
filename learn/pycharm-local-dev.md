---
title: "Develop locally with PyCharm"
description: "Integrate the Astro CLI with PyCharm for local development."
id: pycharm-local-dev
sidebar_label: "PyCharm"
---

This example shows how to set up [PyCharm]((https://www.jetbrains.com/pycharm/)) for local development with Airflow and the [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Before you start

Before using this example, make sure you have:

- [PyCharm](https://www.jetbrains.com/pycharm/)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) installed and a project running locally

## Configure the Python interpreter

In your PyCharm preferences go to **Build, Execution, Deployment** >> **Docker** and set up the following:

![Docker settings](/img/examples/pycharm_local_dev_docker_settings.png)

Go to **Project: <your-project-name>** >> **Python Interpreter** and click the settings gear icon next to Python Interpreter, then click **Add**:

![Interpreter settings](/img/examples/pycharm_local_dev_interpreter.png)

In the window that appears, click on **Docker** in the left pane, and in the **Image name** field select the Docker image that your Airflow environment is running. Then click **OK**.

![Image settings](/img/examples/pycharm_local_dev_docker_image.png)

## Write Airflow code with PyCharm

Using PyCharm to write Airflow DAGs has multiple advantages like code autocompletion, identifying deprecated or unused imports, and error and warning syntax highlighting.

Here is an example of deprecated imports:

![Deprecated Imports](/img/examples/pycharm_local_dev_deprecated_import.png)

Here is an example of an unused import:

![Unused Imports](/img/examples/pycharm_local_dev_unused_import.png)

Here is an example error syntax highlighting:

![Syntax Highlighting](/img/examples/pycharm_local_dev_syntax_highlighting.png)

Here is an example of code autocompletion and built in definitions:

![Code Autocompletion](/img/examples/pycharm_local_dev_autocomplete.png)

## Manage Docker containers with PyCharm

With PyCharm configured to use the Python Interpreter from Docker, you can connect to your Docker containers directly from PyCharm using the ***Services*** pane. If you do not see this pane, try pressing `cmd+8`.

![Services](/img/examples/pycharm_local_dev_docker_services.png)

From the Services pane, start Docker by clicking the green play button and you’ll see the same containers appear as when you run `docker ps`:

![Containers](/img/examples/pycharm_local_dev_docker_containers.png)

You can view logs for the containers by clicking on `/scheduler`, `/triggerer`, `/webserver`, or `/airflow-dev_2cd823-postgres` (this may be a different string based on what the name of the parent directory for your project is):

![Logs](/img/examples/pycharm_local_dev_docker_logs.png)

You can run Airflow CLI commands by right clicking on `/scheduler` and selecting `Create Terminal` to bash into the container:

![CLI](/img/examples/pycharm_local_dev_docker_cli.png)
