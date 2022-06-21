---
title: 'Test and Troubleshoot the KubernetesPodOperator Locally'
sidebar_label: 'Run the KubernetesPodOperator Locally'
id: kubepodoperator-local
description: Test and troubleshoot the KubernetesPodOperator locally.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

The `KubernetesPodOperator` completes work within Kubernetes Pods in a Kubernetes cluster. Test the `KubernetesPodOperator` locally before running it in a production Kubernetes cluster. 

## Set up Kubernetes
<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

The latest versions of Docker for Windows and Mac both support running a single-node Kubernetes cluster locally. 

If you're using a Windows computer and want to make sure your environment is ready for Kubernetes, see [Setting Up Docker for Windows and WSL to Work Flawlessly](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). 

If you're using a Mac cpmputer and want to make sure your environment is ready for Kubernetes, see [Docker Desktop for Mac user manual](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). 

It isn't necessary to install docker-compose.

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

## Update the kubeconfig File
<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

1. Go to the `$HOME/.kube` directory that was created when you enabled Kubernetes in Docker and copy the `config` file into the `/include/.kube/` folder in your Astro project. The `config` file contains all the information the KubePodOperator uses to connect to your cluster. For example:
    ```apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: <cert-authority-data>
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
        client-certificate-data: CERT_CLIENT_DATA
        client-key-data: CERT_KEY_DATA
    ```
    The `clusters.cluster.name` should be searchable as `docker-desktop` in your local `$HOME/.kube``config` file.

2. Update the `CERT_AUTHORITY_DATA`, `CERT_CLIENT_DATA`, and `CERT_KEY_DATA` values in the `config` file with the values for your organization.
3. Under cluster, change `server: https://localhost:6445` to `server: https://kubernetes.docker.internal:6443` to identify the localhost running Kubernetes Pods. If this doesn't work, try `server: https://host.docker.internal:6445`.
4. Optional. Add the `.kube` folder to `.gitignore` if your project is configureed as a GitHub repository and you want to prevent the file from being tracked by your version control tool.
5. Optional. Add the `.kube` folder to `.dockerignore` to exclude it from the Docker image.

</TabItem>

<TabItem value="linux">

In a `.kube` folder in your Astro project, create a default `config` file with:

```bash
microk8s config > /include/.kube/config
```
</TabItem>
</Tabs>

## Run Your Container

The `config_file` points to the `/include/.kube/config` file you just edited. 

You can use the following example DAG to test your configurations. This DAG runs the `hello-world` Docker image in a different cluster based on whether you're running the DAG locally or on Astro. 

If you are using Linux, you need to change the value for `cluster_context` in this DAG to `microk8s`.

Run `astro dev start` to build this config into your image.

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

namespace = conf.get('kubernetes', 'NAMESPACE')

# This detects the default namespace locally and reads the
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
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster,  # when set to True, it looks in the cluster, when set to False, it looks for a file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        get_logs=True,
    )

```
## View Kubernetes Logs
<Tabs
    defaultValue="windows and mac"
    values={[
        {label: 'Windows and Mac', value: 'windows and mac'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="windows and mac">

Run `kubectl get pods -n <your-namespace>` or `kubectl logs {pod_name} -n <your-namespace>` to examine the logs for the pod that just ran. By default, `docker-for-desktop` and `microk8s` run pods in the `default` namespace.

</TabItem>

<TabItem value="linux">

Run `microk8s.kubectl get pods -n <your-namespace>` or `microk8s.kubectl logs {pod_name} -n <your-namespace>` to examine the logs for the pod that just ran. By default, `docker-for-desktop` and `microk8s` run pods in the `default` namespace.

</TabItem>
</Tabs>

## Test the KubernetesPodOperator Locally

Testing DAGs with the [KubernetesPodOperator](kubernetespodoperator.md) locally requires a local Kubernetes environment.

### Step 1: Prepare Your Environment

1. Set up Kubernetes in Docker. See [Set up Kubernetes](#set-up-kubernetes).
2. Update the kubeconfig file. See [Update the kubeconfig File](#update-the-kubeconfig-file).

### Step 2: Add a KubernetesPodOperator Task

To add the KubernetesPodOperator task in a DAG, update your DAG file to include the following code:

```python
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import configuration as conf
# ...

namespace = conf.get('kubernetes', 'NAMESPACE')

# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = '/usr/local/airflow/include/.kube/config'
    in_cluster=False
else:
    in_cluster=True
    config_file=None

with dag:
    k = KubernetesPodOperator(
        namespace=namespace,
        image="my-image",
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster, # if set to true, will look in the cluster for configuration. if false, looks for file
        cluster_context='docker-desktop', # is ignored when in_cluster is set to True
        config_file=config_file,
        get_logs=True)
```

Specifically, your operator must have `cluster_context='docker-desktop` and `config_file=config_file`.

### Step 3: Run and Monitor the KubernetesPodOperator

1. Run `astro dev restart` in the Astro CLI to rebuild your image and run your project in a local Airflow environment.
2. Optional. Review the logs for any pods that were created by the operator for issues. See [View Kubernetes Logs](#view-kubernetes-logs).


## Next Steps ##

- [Run the KubernetesPodOperator on Astro](kubepodoperator.md)
