---
sidebar_label: Use Airflow operators
title: Use Airflow operators in the Astro Cloud IDE
id: use-airflow-operators
description: Learn how to run Airflow operators by creating and configuring operator cells in the Astro Cloud IDE.
---

You can import any Airflow operator available on the Astronomer Registry and run it as part of your Cloud IDE pipeline. In most cases, the Cloud IDE can parse parameters and provides you with a detailed form for configuring the operator. 

## Create an operator cell

1. In the Cloud UI, select **Cloud IDE**.

2. Select a project.

3. On the **Pipelines** page, click a pipeline name to open the pipeline editor.

4. Click **Add Cell** and search for the name of the operator you want to use. When you find it, click its entry in the search box. The cell is added to your pipeline.

  :::caution

  You can add sensors and async operators to your pipeline, but these will not work when testing your pipeline from the Cloud IDE. To test a pipeline with these operators, export your project as a DAG and run it locally or on an Astro Deployment.

  :::

5. Fill out the parameters in the operator cell body. For each parameter, use the switch to the right of the parameter to configure whether your input is treated as a **Literal value** or a **Python expression**.

:::info Literal values and Python expressions

The Astro Cloud IDE is often able to detect the required format for an operator's parameter values. When it does detect the required format, choose **Literal value** to let the Cloud IDE format and check your parameter values.

Conversely, choose a **Python expression** if you want to define a parameter value without the IDE formatting or checking it. If the IDE cannot detect the required format for a parameter value, you can only define it as a Python expression. You can also use Python expressions to pass values from other cells as data dependencies.

For example, the S3toSnowflakeOperator has a parameter called `autocommit` that takes a boolean value. Because the IDE detects the required value format, it shows a toggle when you select **Literal value**. 

![A boolean formatted as a literal value](/img/docs/cloud-ide/literal-value.png)

If you click the toggle on and then select **Python expression**, you see that the IDE converts the toggle into a raw Python expression.

![A boolean formatted as a Python expression](/img/docs/cloud-ide/python-expression.png)

:::

## Create custom operator cells

To import a custom operator that your team uses into the Astro Cloud IDE, create a custom cell type in your project configuration.

1. If you're using a custom cell type to call custom operator code, [commit your IDE project to a Git repository](deploy-project.md#commit-your-project-to-a-git-repository) and add your custom operator code to the `include` folder of your repository.
   
2. In the Cloud UI, select **Cloud IDE**.

3. Select a project.

4. Click **Custom Cells**, then click **+ Cell Type**

5. Enter a **Custom Cell Type Name**. This is the name that appears in the cell body and when you search for the cell type in your pipeline editor. 

6. Enter a **Definition** for the cell type. A definition is a JSON configuration that defines how a user interacts with the cell type, as well as how the cell type can access your custom operator code. For a complete reference for possible JSON values, see [Custom cell type reference](custom-cell-reference.md).

7. Click **Validate** to check that your JSON configuration is valid. After it's validated, click **Add**.

8. Add the cell type to your pipeline as you would for a standard operator cell. See [Create an operator cell](#create-an-operator-cell).

## Run an operator cell

See [Run cells in the Astro Cloud IDE](run-cells.md).
