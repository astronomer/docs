---
sidebar_label: 'Configure platform resources'
title: 'Astronomer Software platform resources'
id: configure-platform-resources
description: A summary of how platform and Airflow deployment resources are created in the context of Astronomer Software.
---

## Configuring platform resources

By default, Astronomer needs around 10 CPUs and 44Gi of memory:

| Pod                              | Request CPU | Request Mem | Limit CPU | Limit Mem | Storage |
| -------------------------------- | ----------- | ----------- | --------- | --------- | ------- |
| `astro-ui`                       | 100m        | 256Mi       | 500m      | 1024Mi    | NA      |
| `houston`                        | 250m        | 512Mi       | 800m      | 1024Mi    | NA      |
| `prisma`                         | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| `commander`                      | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| `registry`                       | 250m        | 512Mi       | 500m      | 1024Mi    | 100Gi   |
| `install`                        | 100m        | 256Mi       | 500m      | 1024Mi    | NA      |
| `nginx`                          | 500m        | 1024Mi      | 1         | 2048Mi    | NA      |
| `grafana`                        | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| `prometheus`                     | 1000m       | 4Gi         | 1000m     | 4Gi       | 100Gi   |
| `elasticsearch client replica-1` | 1           | 2Gi         | 2         | 4Gi       | NA      |
| `elasticsearch client replica-2` | 1           | 2Gi         | 2         | 4Gi       | NA      |
| `elasticsearch data replica-1`   | 1           | 2Gi         | 2         | 4Gi       | 100Gi   |
| `elasticsearch data replica-2`   | 1           | 2Gi         | 2         | 4Gi       | 100Gi   |
| `elasticsearch master replica-1` | 1           | 2Gi         | 2         | 4Gi       | 20Gi    |
| `elasticsearch master replica-2` | 1           | 2Gi         | 2         | 4Gi       | 20Gi    |
| `elasticsearch master replica-3` | 1           | 2Gi         | 2         | 4Gi       | 20Gi    |
| `kibana`                         | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| `fluentd`                        | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| `kubeState`                      | 250m        | 512Mi       | 500m      | 1024Mi    | NA      |
| Total                            | 10.7        | 23.5Gi      | 21.3      | 44Gi      | 460Gi   |

### Changing values

You can change the request and limit of any of the components above in your `config.yaml` or in `values.yaml` (`config.yaml` will overwrite `values.yaml`).

To change something like the resources allocated to `astro-ui`, add the following fields to your `config.yaml`:

```yaml
#####
#Changing Software UI CPU
####

astronomer:
  astroUI:
    resources:
      requests:
        cpu: "200m"
        memory: "256Mi"
      limits:
        cpu: "700m"
        memory: "1024Mi"
```

Once all the changes are made, run `helm upgrade` to switch your platform to the new config:

```shell
helm upgrade <platform-release-name> -f config.yaml --version=<platform-version> astronomer/astronomer -n <your-namespace>
```

Be sure to specify the platform namespace, not an Airflow namespace.

### Infrastructure cost estimates

To ensure reliability with a starting set of Airflow Deployments, these estimates apply to our general recommendation for an Astronomer Software installation in a US East region.

#### AWS

| Component         | Item                                                       | Hourly Cost (Annual Upfront Pricing)|
| ----------------- | ---------------------------------------------------------- | ------------------------------------|
| Compute           | 6 m5.xlarge or 3 m5.2xlarge (24 vCPU 96 GiB)               | $0.68                               |
| EKS control plane | $0.20/hr x 24hr x 365                                      | $0.20                               |
| Database          | db.t2.medium Postgres, Multi-AZ at $0.29/hr x 24hr x 365   | $0.05                               |
| Total             |                                                            | $0.93                               |

#### GCP

| Component | Item                                                           | Hourly Cost (Annual Upfront Pricing)|
| --------- | -------------------------------------------------------------- | ------------------------------------|
| Compute   | 6 n2-standard-8 at $0.311/hr                                   | $0.31                               |
| Database  | Cloud SQL for PostgresSQL with 2 cores and 14.4GB at $0.29/hr  | $0.29                               |
| Total     |                                                                | $0.60                               |

For more information, reference the [GCP Pricing Calculator](https://cloud.google.com/products/calculator/#id=f899c077-6b8b-4ccd-8f8c-974e04cbe872).

#### Azure

| Component | Item                                              | Hourly Cost (Annual Upfront Pricing) |
| --------- | ------------------------------------------------- | ------------------------------------ |
| Compute   | 3 x D8s v3 (8 vCPU(s), 32 GiB)                    | $0.95                               |
| Database  | 1 x Gen 5 (2 vCore), 25 GB Storage, LRS redundancy| $0.18                               |
| Total     |                                                   | $1.13                               |

For more information, reference the [Azure Price Calculator](https://azure.microsoft.com/en-us/pricing/calculator/?service=kubernetes-service).

## Configuring Deployment resources

Most of the key components that you will need to run Airflow can be controlled via the sliders in our UI. However, you may find that there are some discrepancies between the number in the UI and what exists in Kubernetes at any given moment. Below is a summary the less-visible resources that get provisioned with each Airflow deployment you create on Astronomer. All of these resources will exist within the namespace created for your Airflow deployment.

> Note: These are resources that are provisioned in addition to the scheduler, webserver, and worker resources that you've set in your Software UI. If you're running the Kubernetes executor or Kubernetes Pod Operator, resources will be created dynamically, but will not exceed the resource quota you've dictated by your `Extra Capacity` slider.

| Component                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | AU   | CPU/Memory   |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------------ |
| Resource Quotas                                | The resource quota on the namespace will be double the AU (cpu/mem) provisioned for that namespace. Note that this has little to do with what actually gets consumed, but it's necessary because, in certain cases, restarting Airflow requires two webservers and schedulers to exist simultaneously for a brief second while the new environment gets spun up. Without the 2x quota cap, the restart of these services would fail. Additionally, note that any amount added by the `extra capacity` slider will increase this quota by that same amount. | N/A  | N/A          |
| PgBouncer                                      | All Airflow deployments ship with a PgBouncer pod to handle pooling connections to the metadata database.                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 2 AU | 200cpu/768mb |
| StatsD                                         | All Airflow deployments ship with a StatsD pod to handle metrics exports.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 2 AU | 200cpu/768mb |
| Redis                                          | All Airflow deployments **running the celery executor** ship with a Redis pod as a backend queueing system for the workers.                                                                                                                                                                                                                                                                                                                                                                                                                                | 2 AU | 200cpu/768mb |
| Flower                                         | All Airflow deployments **running the celery executor** ship with a Flower pod as a frontend interface for monitoring celery workers.                                                                                                                                                                                                                                                                                                                                                                                                                      | 2 AU | 200cpu/768mb |
| PgBouncer Metrics Exporter Sidecar             | This component reads data from the PgBouncer internal stats database and exposes them to Prometheus. This data powers the database related graphs on our UI and Grafana.                                                                                                                                                                                                                                                                                                                                                                                   | 1 AU | 100cpu/384mb |
| scheduler Log Trimmer Sidecar (`scheduler-gc`) | The scheduler emits logs that are not useful to send to Elasticsearch. Those files are written locally in the pod, so we deploy a trimmer to ensure that the pod does not overflow its ephemeral storage limits.                                                                                                                                                                                                                                                                                                                                           | 1 AU | 100cpu/384mb |

Note that, if the platform is deployed with Elasticsearch disabled, the workers are deployed as StatefulSets to store the logs. This means that we also need to deploy an additional log-trimming sidecar on each pod to prevent the pod from overflowing its ephemeral storage limits.
