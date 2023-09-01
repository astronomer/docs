---
sidebar_label: Write Python
title: Write Python in the Astro Cloud IDE
id: run-python
description: Learn how to run Python code by creating and configuring Python cells in the Astro Cloud IDE.
---

A Python cell contains a Python function that you can run in isolation or as a dependency in your pipeline. Create Python cells to execute Python as part of your data pipeline. 

## Prerequisites 

- An IDE project and pipeline. See [Step 2: Create a pipeline](/astro/cloud-ide/quickstart.md#step-2-create-a-pipeline).

## Create a Python cell

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. On the **Pipelines** page, click a pipeline name to open the pipeline editor.

4. Click **Add Cell** > **Python**.

5. Click the cell name and enter a name for the cell.

6. Add your Python code to the cell body.

## Run a Python cell

See [Run cells in the Astro Cloud IDE](run-cells.md).

## Create explicit dependencies for a Python cell

In a Python cell, click **Dependencies** and select a cell to make it an explicit upstream dependency of your Python cell. When you run your entire pipeline, the Python cell cannot begin running until the selected upstream cell finishes running.

To make a Python cell an upstream dependency for another cell, click **Dependencies** for the other cell and select the name of your Python cell. 

To create data dependencies between Python cells, see [Pass data between cells](pass-data-between-cells.md).

## View complete code for Python cells

To view your Python cell within the context of an Airflow DAG, click **Code**. The Airflow DAG includes your Python function as well as all of the code required to run it on Airflow.

All Python cells execute Python using `aql.dataframe`, which is a function available in the Astro SDK. See [Astro SDK documentation](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html).

## See also

- [Run cells in the Astro Cloud IDE](cloud-ide/run-cells.md).