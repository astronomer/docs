---
title: "Run Azure Data Factory pipelines with Airflow"
sidebar_label: "Tutorial"
description: "Learn how to orchestrate remote jobs in Azure Data Factory with your Apache Airflow DAGs."
id: airflow-azure-data-factory-integration
sidebar_custom_props: { icon: 'img/integrations/azure-data-factory.png' }
---

Azure Data Factory (ADF) is a commonly used service for constructing data pipelines and jobs. With a little preparation, it can be used in combination with Airflow to leverage the best of both tools. In this tutorial, you'll learn why you might want to use these two tools together and how to run your ADF pipeline from your Airflow DAG.

:::info

All code in this tutorial can be found on [the Astronomer Registry](https://registry.astronomer.io/dags/azure-data-factory-dag).

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Azure Data Factory. See [Introduction to Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/introduction).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

To complete this tutorial, you need:

- Two ADF pipelines. If you do not currently have an ADF pipeline in your Azure account and are new to ADF, check out the [ADF quick start docs](https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal) for help getting started.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

## Step 1: Make your ADF pipelines runnable

Before you can orchestrate your ADF pipelines with Airflow, you have to make the pipelines runnable by an external service. There are multiple ways to do this depending on how you manage authentication within your Azure account. This tutorial shows how to register an App with Azure Active Directory to get a **Client ID** and **Client Secret** (API Key) for your Data Factory.

1. Go to Azure Active Directory and click **App registrations** to see a list of registered apps. If you created a Resource group, you should already have an app registered with the same name. Otherwise you can create a new one.

    ![ADF App Registration](/img/integrations/airflow_azure_data_factory_integration_app_registration.png)

    Click the app associated with your resource group, and note the **Application (client) Id**. You'll need this to connect Airflow to ADF.

2. Go to **Certificates & Secrets** -> **New client secret** and create a **Client Secret** which will be used to connect Data Factory in Airflow.

3. Connect your **Client Secret** API key to your Data Factory instance. Go back to the overview of your Data Factory and click **Access Control** -> **Add role assignments** and add your **Application** as a contributor to the Data Factory.

    ![ADF Access Control](/img/integrations/airflow_azure_data_factory_integration_add_role_assignment.png)

4. Add a role assignment with the following settings:

    - Role: Data Factory Contributor
    - Assign access to: User, group, or service principal

    Search for your app, add it to 'Selected members' and click save.

:::info

Additional detail on requirements for interacting with Azure Data Factory using the REST API can be found [here](https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-rest-api). You can also see [this link](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#register-an-application-with-azure-ad-and-create-a-service-principal) for more information on creating a registered application in Azure Active Directory.

:::

## Step 2: Configure your Astro project

Now that you have your Azure resources configured, you can move on to setting up Airflow.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-adf-tutorial && cd astro-adf-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    apache-airflow-providers-microsoft-azure
    ```

    This installs the Azure provider package that contains all of the relevant ADF modules.

3. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 3: Create an Airflow connection to ADF

Add a connection that Airflow will use to connect to ADF. In the Airflow UI, go to **Admin** -> **Connections**.

Create a new connection named `azure_data_factory` and choose the `Azure Data Factory` connection type. Enter the following information:

- **Login:** Your Azure **Client ID** from Step 1
- **Password:** Your Azure **Client secret** from Step 1
- **Extras:** `{"tenantId":"Your Tenant ID", "subscriptionId":"Your Subscription ID"}`

## Step 4: Create your DAG

In your Astro project `dags/` folder, create a new file called `adf-pipeline.py`. Paste the following code into the file:

```python
from datetime import datetime, timedelta

from airflow.models import DAG, BaseOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
from airflow.providers.microsoft.azure.sensors.data_factory import AzureDataFactoryPipelineRunStatusSensor
from airflow.utils.edgemodifier import Label

with DAG(
    dag_id="example_adf_run_pipeline",
    start_date=datetime(2021, 8, 13),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
        "azure_data_factory_conn_id": "azure_data_factory",
        "factory_name": "my-data-factory",  # This can also be specified in the ADF connection.
        "resource_group_name": "my-resource-group",  # This can also be specified in the ADF connection.
    },
    default_view="graph",
) as dag:
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    # [START howto_operator_adf_run_pipeline]
    run_pipeline1: BaseOperator = AzureDataFactoryRunPipelineOperator(
        task_id="run_pipeline1",
        pipeline_name="pipeline1",
        parameters={"myParam": "value"},
    )
    # [END howto_operator_adf_run_pipeline]

    # [START howto_operator_adf_run_pipeline_async]
    run_pipeline2: BaseOperator = AzureDataFactoryRunPipelineOperator(
        task_id="run_pipeline2",
        pipeline_name="pipeline2",
        wait_for_termination=False,
    )

    pipeline_run_sensor: BaseOperator = AzureDataFactoryPipelineRunStatusSensor(
        task_id="pipeline_run_sensor",
        run_id=run_pipeline2.output["run_id"],
    )
    # [END howto_operator_adf_run_pipeline_async]

    begin >> Label("No async wait") >> run_pipeline1
    begin >> Label("Do async wait with sensor") >> run_pipeline2
    [run_pipeline1, pipeline_run_sensor] >> end
```

Update the following parameters in the DAG code:

- `pipeline_name` in the `run_pipeline1` and `run_pipeline2` tasks to the names of your two ADF pipelines.
- `factory_name` in the `default_args` to your factory name.
- `resource_group_name` in the `default_args` to your resource group name from Step 1.

The DAG graph should look similar to this:

![Graph View](/img/guides/multiple_adf_pipeline_graph.png)

## Step 5: Run your DAG to execute your ADF pipelines

Go to the Airflow UI, unpause your `example_adf_run_pipeline` DAG, and trigger it to run the your ADF pipelines.
The DAG will execute both ADF pipelines in parallel (tasks `run_pipeline1` and `run_pipeline2`), and then will use an `AzureDataFactoryPipelineRunStatusSensor` to wait until `pipeline2` has completed before finishing the DAG.

To learn more about all of the ADF modules in the Microsoft Azure provider, check out the [Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure).

## Why use Airflow with ADF

ADF is an easy to learn tool that allows you to quickly create jobs without writing code. It integrates seamlessly with on-premises data sources and other Azure services. However, it has some disadvantages when used alone - namely:

- Building and integrating custom tools can be difficult
- Integrations with services outside of Azure are limited
- Orchestration capabilities are limited
- Custom packages and dependencies can be complex to manage

That's where Airflow comes in. ADF jobs can be run using an Airflow DAG, giving the full capabilities of Airflow orchestration beyond using ADF alone. This allows users that are comfortable with ADF to write their job there, while Airflow acts as the control plane for orchestration.

For a more complex example of orchestrating dependent ADF pipelines with Airflow, see [Orchestrating Multiple Azure Data Factory Pipelines in Airflow](https://registry.astronomer.io/dags/airflow-azure-data-factory).
