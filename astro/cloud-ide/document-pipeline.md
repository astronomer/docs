---
sidebar_label: Document your pipeline
title: Add Markdown cells to your Astro Cloud IDE pipeline
id: document-pipeline
description: Learn how to add documentation to your pipeline and individual cells in the Astro Cloud IDE. 
---

Use Markdown cells to add comments to your code and make it easier for Workspace users to collaborate on shared code. The content of a Markdown cell appears as rendered Markdown in your pipeline editor, as well as a top-level comment in your pipeline DAG. It does not appear in the Airflow UI and is not related to the features described in [Create DAG documentation in Apache Airflow](https://docs.astronomer.io/learn/custom-airflow-ui-docs-tutorial).

## Prerequisites 

- An IDE project and pipeline. See [Step 2: Create a pipeline](/astro/cloud-ide/quickstart.md#step-2-create-a-pipeline).

## Create pipeline documentation

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. On the **Pipelines** page click a pipeline name to open the pipeline editor.

4. Click **Add Cell** > **Markdown**.

5. In the body of the cell, write your documentation in Markdown format. 
   
6. Click out of the cell to save your changes and view the rendered Markdown in your pipeline editor. To view your cell as raw Markdown in your DAG, click **Code**.

![Rendered Markdown cell in the Cloud IDE](/img/cloud-ide/markdown-cell.png)