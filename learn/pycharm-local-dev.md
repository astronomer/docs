---
title: "Develop Airflow DAGs locally with PyCharm"
description: "Integrate the Astro CLI with PyCharm for local development."
id: pycharm-local-dev
sidebar_label: "Develop with PyCharm"
sidebar_custom_props: { icon: 'img/examples/pycharm_logo.png' }
---

This example shows how to set up [PyCharm](https://www.jetbrains.com/pycharm/) for local development with Airflow and the [Astro CLI](https://docs.astronomer.io/astro/cli/overview). Setting up a local development environment allows you to iterate more quickly when developing DAGs by taking advantage of IDE features.

## Before you start

Before trying this example, make sure you have:

- [PyCharm](https://www.jetbrains.com/pycharm/)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)
- An Astro project running locally on your computer. See [Getting started with the Astro CLI](https://docs.astronomer.io/astro/cli/get-started-cli)

## Configure the Python interpreter

To develop Airflow DAGs in PyCharm, you need to configure at least one Python interpreter. In this example you configure an interpreter using Docker, which allows you to write Python code and interact with running DAGs from within PyCharm.

1. In your PyCharm preferences go to **Build, Execution, Deployment** >> **Docker** and specify how to connect to the Docker daemon. For more, see [Connect to Docker](https://www.jetbrains.com/help/pycharm/docker.html#connect_to_docker).

2. Go to **Project: \<your-project-name\>** >> **Python Interpreter**. Click the **Add Interpreter** button on the right, and then click **On Docker**:

    ![Interpreter settings](/img/examples/pycharm_local_dev_interpreter_docker.png)

3. In the window that appears, select **Pull or use existing** for the **Image** option. In the **Image tag** field, select the Docker image that your Airflow environment is running, then click **Next**.

    ![Image settings](/img/examples/pycharm_local_dev_docker_target.png)

4. Wait for PyCharm to finish pulling the Docker image and then click **Next**.

    ![Image settings](/img/examples/pycharm_local_dev_docker_image_pull.png)

5. Ensure the **System Interpreter** is set to Python 3. By default this path will point to the location of Python 3 on the machine and should not need to be changed. Then, click **Create**.

    ![Image settings](/img/examples/pycharm_local_dev_system_interpreter.png)

6. On the original **Python Interpreter** setup screen, ensure the Python interpreter is set to the docker image and click **Apply**, followed by **OK**.

    ![Image settings](/img/examples/pycharm_local_dev_complete_setup.png)

## Write Airflow code with PyCharm

After you configure PyCharm to use the correct interpreter for Airflow, you get multiple advantages like code autocompletion, identifying deprecated or unused imports, and error syntax highlighting.

PyCharm will show you when there are deprecated imports in your project:

![Deprecated Imports](/img/examples/pycharm_local_dev_deprecated_import.png)

It can also alert you when an import is unused:

![Unused Imports](/img/examples/pycharm_local_dev_unused_import.png)

Like with other Python projects, PyCharm will highlight syntax errors in your Airflow code:

![Syntax Highlighting](/img/examples/pycharm_local_dev_syntax_highlighting.png)

Lastly, here is an example of PyCharm autocompleting code and showing built-in definitions:

![Code Autocompletion](/img/examples/pycharm_local_dev_autocomplete.png)

## Manage Airflow Docker containers with PyCharm

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
- [Debug interactively with dag.test()](https://docs.astronomer.io/learn/testing-airflow#debug-interactively-with-dagtest)
