---
title: "Develop Airflow locally with PyCharm"
description: "Integrate the Astro CLI with PyCharm for local development."
id: pycharm-local-dev
sidebar_label: "Develop with PyCharm"
---

This example shows how to set up [PyCharm]((https://www.jetbrains.com/pycharm/)) for local development with Airflow and the [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Before you start

Before trying this example, make sure you have:

- [PyCharm](https://www.jetbrains.com/pycharm/)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
- An Astro project running locally on your computer. See [Getting started with the Astro CLI](https://docs.astronomer.io/astro/cli/get-started-cli)

## Configure the Python interpreter

1. In your PyCharm preferences go to **Build, Execution, Deployment** >> **Docker** and set up the following:

    - **Name**: Docker
    - **Connect to Docker Daemon with**: Docker for Mac
    - **Path mappings**: Enter `/Users` for both **Virtual machine path** and **Local path**.
    
    ![Docker settings](/img/examples/pycharm_local_dev_docker_settings.png)

2. Go to **Project: <your-project-name>** >> **Python Interpreter**. Click the settings gear icon next to **Python Interpreter**, then click **Add**:

    ![Interpreter settings](/img/examples/pycharm_local_dev_interpreter.png)

3. In the window that appears, click **Docker** in the left pane. In the **Image name** field, select the Docker image that your Airflow environment is running, then click **OK**.

    ![Image settings](/img/examples/pycharm_local_dev_docker_image.png)

## Write Airflow code with PyCharm

Using PyCharm to write Airflow DAGs has multiple advantages like code autocompletion, identifying deprecated or unused imports, and error and warning syntax highlighting.

PyCharm will show you when there's deprecated imports in your project:

![Deprecated Imports](/img/examples/pycharm_local_dev_deprecated_import.png)

It can also alert you when an import is unused:

![Unused Imports](/img/examples/pycharm_local_dev_unused_import.png)

Like with other Python projects, PyCharm will highlight syntax errors in your Airflow code:

![Syntax Highlighting](/img/examples/pycharm_local_dev_syntax_highlighting.png)

Lastly, here is an example of PyCharm autocompleting code and showing built-in definitions:

![Code Autocompletion](/img/examples/pycharm_local_dev_autocomplete.png)

## Manage Docker containers with PyCharm

With PyCharm configured to use the Python interpreter from Docker, you can connect to your Docker containers directly from PyCharm using the ***Services*** pane. If you do not see this pane, try pressing `cmd+8`.

![Services](/img/examples/pycharm_local_dev_docker_services.png)

From the **Services** pane, start Docker by clicking the green play button. You’ll see the same containers appear as when you run `docker ps` after starting your Astro project locally:

![Containers](/img/examples/pycharm_local_dev_containers.png)

View logs for the containers by clicking on `/scheduler`, `/triggerer`, `/webserver`, or `/airflow-dev_2cd823-postgres`. Note that these strings might differ based on where the parent directory for your project is located:

![Logs](/img/examples/pycharm_local_dev_logs.png)

Run Airflow CLI commands by right clicking on `/scheduler` and selecting **Create Terminal** to bash into the container:

![CLI](/img/examples/pycharm_local_dev_cli.png)

## See also

- [Develop with VS Code](vscode-local-dev.md)
