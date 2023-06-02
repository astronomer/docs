---
title: "Develop locally with VS Code"
description: "Integrate the Astro CLI with VS Code for local development."
id: vscode-local-dev
sidebar_label: "VS Code"
---

This example shows how to set up [VS Code](https://code.visualstudio.com/) for local development with Airflow and the [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Before you start

Before using this example, make sure you have:

- [VS Code](https://code.visualstudio.com/)
- The [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) VS Code extension
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) installed and a project running locally

## Write Airflow code with VS Code

Follow these steps to start writing your DAGs in VS Code, open the folder containing your Astro Project.

In the bottom left corner of your VS Code window, click the green containers icon and select `Open Folder in Container...`
    
![Open Folder](/img/examples/vscode_local_dev_open_folder.png)
    
The Finder/File Explorer will open prompting you to select the project folder. Ensure that your Astro project is selected and click `Open`.
    
![Finder](/img/examples/vscode_local_dev_finder.png)
    
You will be prompted with 3 options. Select `From 'Dockerfile'`.
    
![From Dockerfile](/img/examples/vscode_local_dev_from_dockerfile.png)
    
A new VS Code window will appear. Note in the lower left corner of the window that your IDE is now pointing to that running Docker container.
    
![Container](/img/examples/vscode_local_dev_container.png)
    
Install the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) to your new session of VS Code. Go to the `Extensions` nav bar option, search for ***Python***, and the first result should be the extension published by Microsoft. Install it by clicking the button `Install in Container <your container name>`.
    
![Extension](/img/examples/vscode_local_dev_extension.png)
    
Ensure the Python interpreter is configured properly by opening the `dags/example_dag_basic.py` file in your Astro project `dags/` folder and start writing some Python. In the example below, you can see that the Python interpreter is working properly and attempting to auto-complete the import line as it is being written.

![Code](/img/examples/vscode_local_dev_open_code.png)
