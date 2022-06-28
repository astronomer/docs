---
title: 'How to Run the KubernetesPodOperator Locally'
sidebar_label: 'Local KubernetesPodOperator'
id: kubepodoperator-local
description: Test the KubernetesPodOperator on your local machine.
---
You use the `KubernetesPodOperator` to create and run Kubernetes pods on a  Kubernetes cluster in a local Kubernetes environment. Using the `KubernetesPodOperator` locally allows you to create, test, and modify your code before you move to production.

## Step 1: Set up Kubernetes

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

## Step 2: Update the kubeconfig File

### Windows and Mac

1. Go to the `$HOME/.kube` directory that was created when you enabled Kubernetes in Docker and copy the `config` file into the `/include/.kube/` folder in your Astro project. The `config` file contains all the information the KubePodOperator uses to connect to your cluster. For example:
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

2. Update the `<certificate-authority-data>`, `<certificate-authority-data>`, and `<certificate-authority-data>` values in the `config` file with the values for your organization. 
3. Under cluster, change `server: https://localhost:6445` to `server: https://kubernetes.docker.internal:6443` to identify the localhost running Kubernetes Pods. If this doesn't work, try `server: https://host.docker.internal:6445`.
4. Optional. Add the `.kube` folder to `.gitignore` if  your project is configureed as a GitHub repository and you want to prevent the file from being tracked by your version control tool. 
5. Optional. Add the `.kube` folder to `.dockerignore` to exclude it from the Docker image.  

### Linux

In a `.kube` folder in your Astro project, create a config file with:

```bash
microk8s.config > /include/.kube/config
```

## Step 3: Run your Container

To use the KubernetesPodOperator, you must define the configuration for your pod, including its namespace and runtime image, when you create an instance of the operator. This sample syntax runs the `hello-world` Docker image in a different namespace based on whether you're running the DAG locally or on Astro. If you are using Linux, the `cluster_context` is `microk8s`. The `config_file` points to the edited `/include/.kube/config` file.

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
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
    )

```

## Step 4: View Kubernetes Logs

Optional. Review the logs for any pods that were created by the operator for issues.

### Windows and Mac

Run `kubectl get pods -n $namespace` or `kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran. By default, `docker-for-desktop` runs pods in the `default` namespace.

### Linux

Run `microk8s.kubectl get pods -n $namespace` or `microk8s.kubectl logs {pod_name} -n $namespace` to examine the logs for the pod that just ran. By default, `microk8s` runs pods in the `default` namespace.

## Next Steps ##

- [Run the KubernetesPodOperator on Astronomer Software](kubepodoperator.md)