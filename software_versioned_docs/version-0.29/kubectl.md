---
sidebar_label: 'kubectl'
title: 'Use kubectl to administer Astronomer Software'
id: kubectl
description: Deploy Astronomer Software Airflow instances with kubectl and Helm.
---

### Kubectl and Helm

[Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [helm](https://helm.sh/docs/using_helm/) are the two primary ways DevOps users will interact/administer the Astronomer Platform.

### Setup
Both these tools are needed to deploy Astronomer onto a Kubernetes cluster. We also recommend using [`kubectx`](https://github.com/ahmetb/kubectx) to simplify commands (the rest of this guide will use `kubectx`).

### Base namespace and release

The initial `helm install` command to deploy Astronomer requires a namespace to deploy the base platform pods into.

```
helm install -f config.yaml . datarouter
```
This deploys a randomly named [release](https://helm.sh/docs/glossary/#release) of our helm charts into the `datarouter` [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).

All [pods](https://kubernetes.io/docs/concepts/workloads/pods/) can be listed in the namespace with kubectl.

```bash
root@orbiter: datarouter
Context "gke_astronomer-dev-190903_us-east4-a_astronomer-dev-lybjumoigv" modified.
Active namespace is "datarouter".

root@orbiter: kubectl get pods
NAME                                                   READY   STATUS    RESTARTS   AGE
cautious-seal-postgresql-0                             1/1     Running   0          2d
singed-chimp-alertmanager-0                            1/1     Running   0          1h
singed-chimp-cli-install-9f97f8b-m6l7t                 1/1     Running   0          1h
singed-chimp-commander-68b95959c5-xb9ht                1/1     Running   0          1h
singed-chimp-elasticsearch-client-84d85f87fb-lmbsf     1/1     Running   0          1h
singed-chimp-elasticsearch-client-84d85f87fb-wjpwc     1/1     Running   0          1h
singed-chimp-elasticsearch-data-0                      1/1     Running   0          1h
singed-chimp-elasticsearch-data-1                      1/1     Running   0          1h
singed-chimp-elasticsearch-exporter-5fc97b847f-52qsq   1/1     Running   0          1h
singed-chimp-elasticsearch-master-0                    1/1     Running   0          1h
singed-chimp-elasticsearch-master-1                    1/1     Running   0          1h
singed-chimp-elasticsearch-master-2                    1/1     Running   0          1h
singed-chimp-elasticsearch-nginx-9c4bc78-f5zzz         1/1     Running   0          1h
singed-chimp-fluentd-ztb6k                             1/1     Running   0          1h
singed-chimp-grafana-6df6859854-btdc6                  1/1     Running   0          1h
singed-chimp-houston-86556ffd74-dkbr8                  1/1     Running   0          1h
singed-chimp-kibana-5ccc7b98d4-gk7vb                   1/1     Running   0          1h
singed-chimp-kube-state-78bd89bf47-m7nrm               1/1     Running   0          1h
singed-chimp-kubed-5699fc79b4-9dz28                    1/1     Running   0          1h
singed-chimp-nginx-5cbdf7967f-2q4dr                    1/1     Running   0          1h
singed-chimp-nginx-default-backend-55788c586-2s9nl     1/1     Running   0          1h
singed-chimp-astro-ui-748dfd5748-77v66                 1/1     Running   0          1h
singed-chimp-prisma-6ddf8f6784-lfnfr                   1/1     Running   0          1h
singed-chimp-prometheus-0                              1/1     Running   0          1h
singed-chimp-registry-0                                1/1     Running   0          1h
```

Run `helm ls` to list all releases:

```bash
root@orbiter: helm ls
NAME                             	REVISION	UPDATED                 	STATUS  	CHART                   	NAMESPACE                             
cautious-seal                    	1       	Mon May  6 14:37:34 2019	DEPLOYED	postgresql-0.18.1       	datarouter                            
singed-chimp                     	3       	Thu May  9 12:08:36 2019	DEPLOYED	astronomer-0.8.2        	datarouter                         
```
There is a release for Astronomer (`single-chimp`) and postgres (`cautious-seal`) in the `datarouter` namespace.

### Creating new Airflow deployments

If you navigate to the Software UI and create a new deployment, it will create a new helm release in a new namespace.

```bash
root@orbiter helm ls
NAME                             	REVISION	UPDATED                 	STATUS  	CHART                   	NAMESPACE
accurate-bolide-9914             	2       	Thu May  9 12:06:06 2019	DEPLOYED	airflow-0.8.2           	datarouter-accurate-bolide-9914                              
cautious-seal                    	1       	Mon May  6 14:37:34 2019	DEPLOYED	postgresql-0.18.1       	datarouter                            
singed-chimp                     	3       	Thu May  9 12:08:36 2019	DEPLOYED	astronomer-0.8.2        	datarouter                         
```

The `accurate-bolide-9914` helm release now lives in the a namespace generated by Astronomer named `$basenamespace-release_name` (datarouter-accurate-bolide-9914) and lives on the URL `$release-name-airflow-BASEDOMAIN`.

Switching into the `datarouter-accurate-bolide-9914` namespace reveals the Airflow pods.

```bash
root@orbiter: kubectl get namespaces
NAME                                     STATUS   AGE
datarouter                               Active   2d
datarouter-accurate-bolide-9914          Active   1h
default                                  Active   222d

root@orbiter: kubens datarouter-accurate-bolide-9914
root@orbiter: kubectl get pods

NAME                                                        READY   STATUS    RESTARTS   AGE
accurate-bolide-9914-pgbouncer-57b46d67bb-b4tpw             2/2     Running   0          1h
accurate-bolide-9914-scheduler-7d4f5596b5-r457d             2/2     Running   0          1h
accurate-bolide-9914-statsd-84d76854fb-wz45c                1/1     Running   0          1h
accurate-bolide-9914-webserver-86bcbc48b-5xcwr              1/1     Running   0          1h
accurate-bolide-9914-worker-0                               1/1     Running   0          1m
accurate-bolide-9914-redis-0                                1/1     Running   0          1m
accurate-bolide-9914-flower-84f7d67fbd-q5sd7                1/1     Running   0          1m
```

Since this deployment is running the Celery executor with 1 worker, there are pods for Redis and Flower.

### Managing Pods

Airflow logs can be fetched directly from the underlying pods:

```bash
root@orbiter: kubectl logs accurate-bolide-9914-scheduler-7d4f5596b5-r457d

Waiting for host: accurate-bolide-9914-pgbouncer 6543
Initializing airflow database...
[2019-05-09 17:53:22,865] {settings.py:182} INFO - settings.configure_orm(): Using pool settings. pool_size=5, pool_recycle=1800, pid=18
[2019-05-09 17:53:24,345] {__init__.py:51} INFO - Using executor KubernetesExecutor
DB: postgresql://accurate_bolide_9914_airflow:***@accurate-bolide-9914-pgbouncer:6543/accurate-bolide-9914-metadata
[2019-05-09 17:53:24,969] {db.py:350} INFO - Creating tables
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Done.
[2019-05-09 17:53:28,159] {settings.py:182} INFO - settings.configure_orm(): Using pool settings. pool_size=5, pool_recycle=1800, pid=8
[2019-05-09 17:53:29,663] {__init__.py:51} INFO - Using executor KubernetesExecutor
  ____________       _____________
 ____    |__( )_________  __/__  /________      __
____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /
___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /
 _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/
[2019-05-09 17:53:30,338] {jobs.py:1500} INFO - Starting the scheduler
[2019-05-09 17:53:30,339] {jobs.py:1508} INFO - Running execute loop for -1 seconds
[2019-05-09 17:53:30,340] {jobs.py:1509} INFO - Processing each file at most -1 times
[2019-05-09 17:53:30,340] {jobs.py:1512} INFO - Searching for files in /usr/local/airflow/dags
[2019-05-09 17:53:30,341] {jobs.py:1514} INFO - There are 2 files in /usr/local/airflow/dags
[2019-05-09 17:53:30,343] {kubernetes_executor.py:691} INFO - Start Kubernetes executor
```

A full description of a pods status, resource request, and other data can be found with the `describe` command

```bash
root@orbiter: kubectl describe po/accurate-bolide-9914-scheduler-7d4f5596b5-g72pg
Name:               accurate-bolide-9914-scheduler-7d4f5596b5-g72pg
Namespace:          datarouter-accurate-bolide-9914
Priority:           0
PriorityClassName:  <none>
Node:               gke-astronomer-dev-l-astronomer-dev-n-1c6fc689-s8pg/10.150.0.77
Start Time:         Thu, 09 May 2019 13:53:20 -0400
Labels:             component=scheduler
                    platform=singed-chimp
                    pod-template-hash=3809115261
                    release=accurate-bolide-9914
                    tier=airflow
                    workspace=cjvgu6b2d00110b785tfxyqp0

```

Pods can also be deleted as a way to restart any Airflow component.

```
root@orbiter: kubectl delete po/accurate-bolide-9914-scheduler-7d4f5596b5-r457d
```

This will delete that copy of the pod and spin up a new one. All pods in an Airflow deployment are meant to be stateless, so deleting one and letting it recreate should not cause any


### Other Resources

For additional `kubectl` commands, check out this [Kubernetes Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).
