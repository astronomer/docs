---
title: 'Test and Troubleshoot the KubernetesPodOperator Locally'
sidebar_label: 'Test the KubernetesPodOperator locally'
id: kubepodoperator-local
description: Test and troubleshoot the KubernetesPodOperator locally.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


The `KubernetesPodOperator` is an Airflow operator that completes tasks in Kubernetes Pods. The `KubernetesPodOperator` provides an isolated, containerized execution environment for each task and lets you run custom Docker images and Python versions, set task-level resource requests, and more.

The Kubernetes infrastructure required to run the `KubernetesPodOperator` is built in. To test the `KubernetesPodOperator` operator locally, you need a local Kubernetes environment.

## Step 1: Set up Kubernetes
<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

The latest versions of Docker for Windows and Mac let you run a single node Kubernetes cluster locally. If you are using Windows, see [Setting Up Docker for Windows and WSL to Work Flawlessly](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). If you are using Mac, see [Docker Desktop for Mac user manual](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). It isn't nevessary to install Docker Compose.

1. Open Docker and go to **Settings** > **Kubernetes**.

2. Select the `Enable Kubernetes` checkbox.

3. Click **Apply and Restart**.

4. Click **Install** in the **Kubernetes Cluster Installation** dialog.

    Docker restarts and the status indicator changes to green to indicate Kubernetes is running.

</TabItem>
<TabItem value="linux">

1. Install Microk8s. See [Microk8s](https://microk8s.io/).

2. Run `microk8s.start` to start Kubernetes.

</TabItem>
</Tabs>

## Step 2: Update the kubeconfig file

<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

1. Go to the `$HOME/.kube` directory that was created when you enabled Kubernetes in Docker and copy the `config` file into the `/include/.kube/` folder in your project. The `config` file contains all the information the KubernetesPodOperator uses to connect to your cluster. For example:
    ```apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: <certificate-authority-data>
        server: https://kubernetes.docker.internal:6443/
    name: docker-desktop
    contexts:
    - context:
        cluster: docker-desktop
        user: docker-desktop
    name: docker-desktop
    current-context: docker-desktop
    kind: Config
    preferences: {}
    users:
    - name: docker-desktop
    user:
        client-certificate-data: <client-certificate-data>
        client-key-data: <client-key-data>
    ```
    The cluster `name` should be searchable as `docker-desktop` in your local `$HOME/.kube``config` file. Do not add any additional data to the `config` file.

2. Update the `<certificate-authority-data>`, `<client-authority-data>`, and `<client-key-data>` values in the `config` file with the values for your organization.
3. Under cluster, change `server: https://localhost:6445` to `server: https://kubernetes.docker.internal:6443` to identify the localhost running Kubernetes Pods. If this doesn't work, try `server: https://host.docker.internal:6445`.
4. Optional. Add the `.kube` folder to `.gitignore` if your project is hosted in a GitHub repository and you want to prevent the file from being tracked by your version control tool.
5. Optional. Add the `.kube` folder to `.dockerignore` to exclude it from the Docker image.

</TabItem>
<TabItem value="linux">

In a `.kube` folder in your project, create a config file with:

```bash
microk8s.config > /include/.kube/config
```
</TabItem>
</Tabs>

## Step 3: Run your container

To use the KubernetesPodOperator, you must define the configuration of each task and the Kubernetes Pod in which it runs, including its namespace and Docker image.

This example DAG runs a `hello-world` Docker image. The namespace is determined dynamically based on whether you're running the DAG in your local environment. If you are using Linux, the `cluster_context` is `microk8s`. The `config_file` points to the edited `/include/.kube/config` file.
Run `astro dev start` to build this config into your image.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get('kubernetes', 'NAMESPACE')

# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = '/usr/local/airflow/include/.kube/config'
    in_cluster = False
else:
    in_cluster = True
    config_file = None

dag = DAG('example_kubernetes_pod', schedule_interval='@once', default_args=default_args)


with dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="hello-world",
        labels={"<pod-label>": "<label-name>"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
    )

```
## Step 4: View Kubernetes logs

Optional. Use the `kubectl` command line tool to review the logs for any pods that were created by the operator for issues. If you haven't installed the `kubectl` command line tool, see [Install Tools](https://kubernetes.io/docs/tasks/tools/#kubectl).

<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

Run `kubectl get pods -n $namespace` or `kubectl logs {pod_name} -n $namespace` to examine the logs for the Pod that just ran. By default, `docker-for-desktop` runs Pods in the `default` namespace.

</TabItem>
<TabItem value="linux">

Run `microk8s.kubectl get pods -n $namespace` or `microk8s.kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran. By default, `microk8s` runs pods in the `default` namespace.

</TabItem>
</Tabs>

## Next Steps

- [Run the KubernetesPodOperator on Astronomer Software](kubepodoperator.md)