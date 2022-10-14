---
title: "Orchestrate Azure Container Instances with Airflow"
sidebar_label: "Azure Container Instances"
description: "How to orchestrate containers with Azure Container Instances with your Airflow DAGs."
id: airflow-azure-container-instances
tags: ["Integrations", "Azure", "DAGs"]
---

[Azure Container Instances](https://azure.microsoft.com/en-us/services/container-instances/) (ACI) is one service that Azure users can leverage for working with containers. In this guide, you'll learn how to orchestrate ACI using Airflow and walk through an example DAG.

> **Note:** All code in this guide can be found on [the Astronomer Registry](https://registry.astronomer.io/dags/azure-container-instance).

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of ACI. See [Getting started with Azure Container Instances](https://azure.microsoft.com/en-us/products/container-instances/#getting-started).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## The ACI Operator

The easiest way to orchestrate ACI with Airflow is to use the [AzureContainerInstancesOperator](https://registry.astronomer.io/providers/microsoft-azure/modules/azurecontainerinstancesoperator). This operator starts a container on ACI, runs the container, and terminates the container when all processes are completed.

The only prerequisites for using this operator are:

- An Azure account with a [resource group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal) created
- An [Azure Service Principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals) that has write permissions over that resource group
- A Docker image to use for the container (either publicly or privately available)

This operator can also be used to run existing container instances and make certain updates, including the docker image, environment variables, or commands. Some updates to existing container groups are not possible with the operator, including CPU, memory, and GPU; those updates require deleting the existing container group and recreating it, which can be accomplished using the [AzureContainerInstanceHook](https://registry.astronomer.io/providers/microsoft-azure/modules/azurecontainerinstancehook).

## When to use ACI

There are multiple ways to manage containers with Airflow on Azure. The most flexible and scalable method is to use the [KubernetesPodOperator](https://registry.astronomer.io/providers/kubernetes/modules/kubernetespodoperator). This lets you run any container as a Kubernetes pod, which means you can pass in resource requests and other native Kubernetes parameters. Using this operator requires an [AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/) cluster (or a hand-rolled Kubernetes cluster).

If you are not running on [AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/), ACI can be a great choice:

- It's easy to use and requires little setup
- You can run containers in different regions
- It's typically the cheapest; since no virtual machines or higher-level services are required, **you only pay for the memory and CPU used by your container group while it is active**
- Unlike the [DockerOperator](https://registry.astronomer.io/providers/docker/modules/dockeroperator), it does not require running a container on the host machine

With these points in mind, Astronomer recommends using ACI with the `AzureContainerInstancesOperator` for testing or lightweight tasks that don't require scaling. For heavy production workloads, you should use AKS and the `KubernetesPodOperator`.

## Example

Using Airflow to create and run ACI is straightforward: You first identify the Azure resource group you want to create the Azure Container Instance in (or create a new one), then ensure your Azure instance has a service principal with write access over that resource group. For more information, see [Use the portal to create an Azure AD application and service principal that can access resources](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal).

> **Note**: In Airflow 2.0, provider packages are separate from the core of Airflow. If you are running 2.0 with Astronomer, the [Microsoft Provider](https://registry.astronomer.io/providers/microsoft-azure) package is already included in our Astronomer Certified Image; if you are not using Astronomer you may need to install this package separately to use the hooks, operators, and connections described here. To learn more, read [Airflow Docs on Provider Packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html).

Next, create an Airflow connection with the type ACI. Specify your Client ID in the **Login** field, Client Secret in the **Password** field, and Tenant and Subscription IDs in the **Extras** field as json. It should look something like this:

![ACI Connection](/img/guides/aci_connection.png)

Lastly, define a DAG using the `AzureContainerInstancesOperator`:

```python
from airflow import DAG
from airflow.providers.microsoft.azure.operators.azure_container_instances import AzureContainerInstancesOperator
from datetime import datetime, timedelta

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG('azure_container_instances',
         start_date=datetime(2020, 12, 1),
         max_active_runs=1,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:

    opr_run_container = AzureContainerInstancesOperator(
        task_id='run_container',
        ci_conn_id='azure_container_conn_id',
        registry_conn_id=None,
        resource_group='adf-tutorial',
        name='azure-tutorial-container',
        image='hello-world:latest',
        region='East US',
        cpu=1,
        memory_in_gb=1.5,
        fail_if_exists=False

    )
```

The parameters for the operator are:

- **ci\_conn\_id:** The connection ID for the Airflow connection we created above
- **registry\_conn\_id:** The connection ID to connect to a registry. In this case we use DockerHub, which is public and does not require credentials, so we pass in `None`
- **resource\_group:** Our Azure resource group
- **name:** The name we want to give our ACI. Note that this must be unique within the resource group
- **image:** The Docker image we want to use for the container. In this case we use a simple Hello World example from Docker
- **region:** The Azure region we want our ACI deployed to
- **CPU:** The number of CPUs to allocate to the container. In this example we use the default minimum. For more information on allocating CPUs and memory, refer to the [Azure documentation](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-faq).
- **memory\_in\_gb**: The amount of memory to allocate to the container. In example we use the default minimum.
- **fail\_if\_exists:** Whether we want the operator to raise an exception if the container group already exists (default value is `True`). If it's set to False and the container group name already exists within the given resource group, the operator will attempt to update the container group based on the other parameters before running and terminating upon completion

You can also provide the operator with other parameters such as environment variables, volumes, and a command as needed to run the container.

If we run this DAG, an ACI will spin up, run the container with the Hello World image, and spin down. If we look at the Airflow task log, we see the printout from the container has propagated to the logs:

![ACI Task Log](/img/guides/aci_task_log.png)

From here we can build out our DAG as needed with any other dependent or independent tasks.