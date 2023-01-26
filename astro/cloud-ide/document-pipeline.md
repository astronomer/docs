---
sidebar_label: Document your pipeline
title: Add documentation to an Astro Cloud IDE pipeline
id: document-pipeline
description: Learn how to add documentation to your pipeline and individual cells in the Astro Cloud IDE. 
---

Use Markdown cells to document your pipeline and make it easier for team members to collaborate on the same code. Your Markdown cell appears as a top-level comment in the generated DAG for your data pipeline. It does not appear in the Airflow UI and is not related to the features described in [Create DAG documentation in Apache Airflow](https://docs.astronomer.io/learn/custom-airflow-ui-docs-tutorial).

## Prerequisites 

- An IDE project and pipeline. See [Step 2: Create a pipeline](cloud-ide.md/quickstart#step-2-create-a-pipeline).

## Create pipeline documentation

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. On the **Pipelines** page click a pipeline name to open the pipeline editor.

4. Click **Add Cell** > **Markdown**.

5. In the body of the cell, write your documentation in Markdown format. 

6. Optional. Click **Code** to view your documentation within the context of an Airflow DAG.