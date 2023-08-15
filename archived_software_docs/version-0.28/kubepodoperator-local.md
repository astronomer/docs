---
title: 'How to Run the KubernetesPodOperator Locally'
sidebar_label: 'Local KubernetesPodOperator'
id: kubepodoperator-local
description: Test the KubernetesPodOperator on your local machine.
---

## Setup Kubernetes

### Windows and Mac

The latest version of Docker for Windows and Mac comes with the ability to run a single node Kubernetes cluster on your local machine. If you are on Windows, follow [this guide](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly) for setting up Docker for Windows 10 and WSL (you don’t need to install docker compose if you don’t want to).

Go into Docker>Settings>Kubernetes to check the `Enable Kubernetes` checkbox and change the default orchestrator to Kubernetes. Once these changes are applied, the docker service will restart and the green dot in the bottom left hand corner will indicate Kubernetes is running. [Docker's docs](https://docs.docker.com/docker-for-mac/#kubernetes)

### Linux

Install [microk8s](https://microk8s.io/) and run `microk8s.start` to spin up Kubernetes.

## Get your Kube Config

### Windows and Mac

Navigate to the `$HOME/.kube` that was created when you enabled Kubernetes in Docker and copy the `config` into `/include/.kube/` folder of in your Astro project. This file contains all the information the KubePodOperator uses to connect to your cluster. Under cluster, you should see `server: https://localhost:6445`. Change this to `server: https://kubernetes.docker.internal:6443` (If this does not work, try `server: https://host.docker.internal:6445`) to tell the docker container running Airflow knows to look at your machine’s localhost to run Kubernetes Pods.

### Linux

In a `.kube` folder in your Astronomer project, create a config file with:

```bash
microk8s.config > /include/.kube/config
```

## Run your Container

The `config_file` is pointing to the `/include/.kube/config` file you just edited. Run `astro dev start` to build this config into your image.

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
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
    )

```

This example simply runs the docker `hello-world` image and reads environment variables to determine where it is run.

If you are on Linux, the `cluster_context` will be `microk8s`

## View Kubernetes Logs

### Windows and Mac

You can use `kubectl get pods -n $namespace` and `kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran. By default, `docker-for-desktop` and `microk8s` will run pods in the `default` namespace.

### Linux

Run the same commands as above prefixed with microk8s:
```
microk8s.kubectl get pods -n $namespace
```

When you are ready to deploy this up into Astronomer, follow the [KubernetesPodOperator doc](kubepodoperator.md) to find a list of the necessary changes that will need to be made.
