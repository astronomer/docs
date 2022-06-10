---
title: 'Test and Troubleshoot the KubernetesPodOperator Locally'
sidebar_label: 'Local KubernetesPodOperator'
id: kubepodoperator-local
description: Test and troubleshoot the KubernetesPodOperator locally.
---

You use the `KubernetesPodOperator` to create and run Kubernetes pods on a  Kubernetes cluster in a local Kubernetes environment. Using the `KubernetesPodOperator` locally allows you to create, test, and modify your code before you move to production.

## Setup Kubernetes

### Windows and Mac

The latest versions of Docker for Windows and Mac let you run a single node Kubernetes cluster locally. If you are using Windows, see [Setting Up Docker for Windows and WSL to Work Flawlessly](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). If you are using Mac, see [Docker Desktop for Mac user manual](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly). It isn't nevessary to install docker-compose.

1. Open Docker and go to **Settings** > **Kubernetes**.

2. Select the `Enable Kubernetes` checkbox. 

3. Click **Apply and Restart**.

4. Click **Install** in the **Kubernetes Cluster Installation** dialog.

    Docker restarts and the status indicator changes to green to indicate Kubernetes is running.

### Linux

1. Install Microk8s. See [Microk8s](https://microk8s.io/).

2. Run `microk8s.start` to start Kubernetes.

## Update the kubeconfig File

### Windows and Mac

Go to the `$HOME/.kube` directory that was created when you enabled Kubernetes in Docker and copy the `config` into the `/include/.kube/` folder in your Astro project. This file contains all the information the KubePodOperator uses to connect to your cluster. Under cluster, you should see `server: https://localhost:6445`. Change this to `server: https://kubernetes.docker.internal:6443` to identify the localhost running Kubernetes Pods. If this doesn't work, try `server: https://host.docker.internal:6445`.

### Linux

In a `.kube` folder in your Astro project, create a config file with:

```bash
microk8s.config > /include/.kube/config
```

## Run Your Container

The `config_file` is pointing to the `/include/.kube/config` file you just edited. This example runs the docker `hello-world` image and reads environment variables to determine where it is run. If you are using Linux, the `cluster_context` is `microk8s`.

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
        labels={"foo": "bar"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster,  # when set to True, it looks in the cluster, if False, it looks for a file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
    )

```
## View Kubernetes Logs

### Windows and Mac

You can use `kubectl get pods -n $namespace` and `kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran. By default, `docker-for-desktop` and `microk8s` run pods in the `default` namespace.

### Linux

Run the same commands prefixed with microk8s. For example:
```
microk8s.kubectl get pods -n $namespace
```
## Next Steps ##

- [Run the KubernetesPodOperator on Astronomer Software](kubepodoperator.md)