---
title: 'Astronomer Software system components'
sidebar_label: 'System components'
id: system-components
description: Learn about the various tools and services that make up Astronomer Software.
---

Astronomer Software utilizes a variety of tools to run Airflow securely and reliably in your private cloud. This guide contains names and descriptions of all system components required to run Astronomer Software.

## Platform components

Astronomer Software brings together best-of-class components into a complete "Managed Airflow on Kubernetes" system:

* [Astro CLI](https://github.com/astronomer/astro-cli) - Command line tool for pushing deployments from your local machine to your workspaces running on Kubernetes. The CLI also provides the ability to launch a local stack using docker for local development and testing of DAGs, hooks, and operators.
* Software UI (React) - A modern web based interface to create manage workspaces and deployments. Through the UI you can scale up or down your resources per deployment, invite new users and monitor Airflow logs
* Houston (GraphQL API) - The core GraphQL API layer to interact with your astronomer workspaces and deployments. Use GraphQL queries directly, or integrate with your CI/CD platform to automate Airflow deployments.
* [Docker Registry](https://docs.docker.com/registry/) - Each Airflow deployment on your cluster will have it’s own set of required libraries and environment settings. Every time you create/update a deployment, a new docker image is built and pushed to a private registry created for your Astronomer platform. Kubernetes will pull from this registry when creating new pods.
* [Telescope](https://github.com/astronomer/telescope) - Command line tool for generating additional metrics from your Airflow environments. It connects directly to Airflow and generates snapshots of your usage and configurations at various points in time. Astronomer uses this information to troubleshoot your environments.
* Commander - the provisioning component of the Astronomer Platform. It is responsible for interacting with the underlying infrastructure layer. gRPC service to communicate between our API and Kubernetes
* [Prometheus](https://prometheus.io/) - A monitoring platform used to collect metrics from StatsD. Prometheus collects Airflow metrics and pushes them to Granfana for visualization. Email alerts can also be setup to help quickly identify issues.
* [Grafana](https://grafana.com/) - A web dashboard to help visualize and monitor Airflow metrics flowing in from Prometheus. Astronomer has pre-built plenty of dashboards to monitor your cluster or you can create your own custom dashboards to meet your needs.
* [Alert Manager](https://prometheus.io/docs/alerting/alertmanager/) - Email alerts from Prometheus metrics. Enter emails for anyone you want to be alerted in the Software UI. These alerts can help notify you of issues on your cluster such as the Airflow scheduler running slowly.
* [NGINX](https://www.nginx.com/) - NGINX is used as an ingress controller to enforce authentication and direct traffic to the various services such as Airflow webserver, Grafana, Kibana etc. NGINX is also used to serve Airflow logs back up to the Airflow web UI from ElasticSearch.
* [FluentD](https://www.fluentd.org/) - FluentD is a data collector that is used to collect and push the Airflow log data into ElasticSearch.
* [Elasticsearch](https://github.com/elastic/elasticsearch) - A powerful search engine used to centralize and index logs from Airflow deployments.
* [Kibana](https://github.com/elastic/kibana) - A web dashboard to help visualize all of your Airflow logs powered by ElasticSearch. Create your own dashboards to centralize your logs across all of your deployments.
* [Prisma ORM](https://www.prisma.io/) - An interface between the HoustonGraphQL API and your Postgres database. This handles read/writes to the database as well as migrations for upgrades.
* [Astronomer Helm](https://github.com/astronomer/astronomer) - Helm charts for the Astronomer Platform
* [Docker images](https://quay.io/astronomer/) - Docker images for deploying and running Astronomer on DockerHub.

## Airflow components

When you create an Airflow deployment in Astronomer, the following components are installed:

* [Scheduler](https://airflow.apache.org/scheduler.html) - Determines dependencies and decides when DAGs should run and when tasks are ready to be scheduled.
* [Webserver](https://airflow.apache.org/ui.html) - Airflow’s web UI used to view DAGs, Connections, variables, logs etc.
* [pgBouncer](https://pgbouncer.github.io/) - Provides connection pooling for Postgres. This helps prevent the Airflow database from being overwhelmed by too many connections.
* [StatsD](https://github.com/statsd/statsd) - Provides DAG and task level metrics from Airflow. Astronomer collects these metrics and pushes to a centralized view in Grafana
* Celery components:
  * [Worker](https://docs.celeryproject.org/en/latest/userguide/workers.html) - A service running to process Airflow tasks, which can be scaled up to increase the throughput.
  * [Flower](https://flower.readthedocs.io/en/latest/) - Web UI for Celery distributed task queue. Used to monitor your Airflow worker services
  * [Redis](https://redis.io/) - In memory data store used as the backend by the Celery task queue

## Customer-supplied components

To run Astronomer in your environment, you just need to bring a Kubernetes cluster and a Postgres database:

* [Kubernetes](https://kubernetes.io/) - You bring your own Kubernetes environment (EKS, GKE, AKS, other). Coordinates communication between the services, and provides fault tolerance on failures.
* [PostgreSQL](https://www.postgresql.org/) - database used as the backend for the Houston service as well as each Airflow deployment.
