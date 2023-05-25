---
sidebar_label: Use Airflow operators
title: Use Airflow operators in the Astro Cloud IDE
id: use-airflow-operators
description: Learn how to run Airflow operators by creating and configuring operator cells in the Astro Cloud IDE.
---

You can import any Airflow operator available on the Astronomer Registry and run it as part of your Cloud IDE pipeline. In most cases, the Cloud IDE can parse parameters and provides you with a detailed form for configuring the operator. 

## Create an operator cell

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. On the **Pipelines** page, click a pipeline name to open the pipeline editor.

4. Click **Add Cell** and search for the name of the operator you want to use. When you find it, click its entry in the search box. The cell is added to your pipeline.

  :::caution

  You can add sensors and async operators to your pipeline, but these will not work when testing your pipeline from the Cloud IDE. To test a pipeline with these operators, export your project as a DAG and run it locally or on an Astro Deployment.

  :::

5. Fill out the parameters in the operator cell body. For each parameter, use the switch to the right of the parameter to configure whether your input is treated as a **Literal value** or a **Python expression**.

:::info Literal expressions and Python expressions

The Astro Cloud IDE is often able to detect the required format for an operator's parameter values. When it does detect the required format, choose **Literal value** to let the Cloud IDE format and check your parameter values.

Conversely, choose a **Python expression** if you want to define a parameter value without the IDE formatting or checking it. If the IDE cannot detect the required format for a parameter value, you can only define it as a Python expression. You can also use Python expressions to pass values from other cells as data dependencies.

For example, the S3toSnowflakeOperator has a parameter called `autocommit` that takes a boolean value. Because the IDE detects the required value format, it shows a toggle when you select **Literal value**. 

[Image]

If you click the toggle on and then select **Python expression**, you see that the IDE converts the toggle into a raw Python expression.

[Image]

:::

## Run an operator cell

See [Run cells in the Astro Cloud IDE](run-cells.md).
