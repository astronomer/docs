---
title: "Astronomer Enterprise Overview"
navTitle: "Overview"
description: "Architecture, installation guides, customization, and platform overview for Astronomer Enterprise."
note: "Consider updating https://github.com/astronomer/astronomer when you update this doc"
---

Astronomer makes it easy to run, monitor, and scale [Apache Airflow](https://github.com/apache/airflow) deployments in our cloud or yours. Source code is made available for the benefit of customers.

If you'd like to see the platform in action, [start a free trial on our SaaS service, Astronomer Cloud](https://www.astronomer.io/get-astronomer/) and run through our [getting started guide](https://www.astronomer.io/docs/enterprise/stable/get-started/quickstart/). This is a good first step, even if you're ultimately interested in running Astronomer Enterprise in your own Kubernetes cluster.

## Architecture

![Astronomer Enterprise Overview](https://assets2.astronomer.io/main/enterpriseArchitecture.svg)

## Installation Guides

We have created guides for installing Astronomer on a number of Kubernetes environments:

* [Amazon Web Services EKS](https://www.astronomer.io/docs/enterprise/stable/install/aws/install-aws-standard/)
* [Google Cloud Platform GKE](https://www.astronomer.io/docs/enterprise/stable/install/gcp/install-gcp-standard/)
* [Microsoft Azure AKS](https://www.astronomer.io/docs/enterprise/stable/install/azure/install-azure-standard/)
* [Openshift Kubernetes](https://www.astronomer.io/docs/enterprise/)
* [Digital Ocean Kubernetes](https://www.astronomer.io/docs/enterprise/)
* ["General" Kubernetes](https://www.astronomer.io/docs/enterprise/)

## Customizing Your Installation

Because the platform uses Helm throughout, it's very easy to customize your Astronomer installation. Below are some guides for most common customizations:

* [Integrating Auth Systems](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/integrate-auth-system/)
* [Configuring Resources with Helm](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/manage-platform-users/)
* [Configuring a Registry Back End](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/registry-backend/)
* [Built-in Alerts](https://www.astronomer.io/docs/enterprise/stable/monitor/platform-alerts/)

## Administration

There are many tools at your disposal for administrating Astronomer:

* [The Houston API Playground](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/houston-api/)
* [Metrics](https://www.astronomer.io/docs/enterprise/stable/monitor/grafana-metrics/)
* [Using Kibana](https://www.astronomer.io/docs/enterprise/stable/monitor/kibana-logging/)
* [Using kubectl](https://www.astronomer.io/docs/enterprise/stable/troubleshoot/kubectl/)
* [Pulling Postgres Credentials](https://www.astronomer.io/docs/enterprise/stable/customize-airflow/access-airflow-database/)
* [Upgrade to a Patch Version of Astronomer Enterprise](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/upgrade-astronomer-patch/)
* [Migrating An Airflow Deployment to Astronomer](https://www.astronomer.io/docs/enterprise/)

## License

Usage of Astronomer requires an [Astronomer Platform Enterprise Edition license](https://github.com/astronomer/astronomer/blob/master/LICENSE).

## Platform Components

Astronomer Enterprise brings together best-of-class components into a complete "Managed Airflow on Kubernetes" system:

* [Astro CLI](https://github.com/astronomer/astro-cli) - Command line tool for pushing deployments from your local machine to your workspaces running on Kubernetes. The CLI also provides the ability to launch a local stack via docker for local development and testing of DAGs, hooks and operators.
* Orbit (React UI) - A modern web based interface to create manage workspaces and deployments. Through the UI you can scale up or down your resources per deployment, invite new users and monitor Airflow logs
* Houston (GraphQL API) - The core GraphQL API layer to interact with your astronomer workspaces and deployments. Use GraphQL queries directly, or integrate with your CI/CD platform to automate Airflow deployments.
* [Docker Registry](https://docs.docker.com/registry/) - Each Airflow deployment on your cluster will have it???s own set of required libraries and environment settings. Every time you create/update a deployment, a new docker image is built and pushed to a private registry created for your Astronomer platform. Kubernetes will pull from this registry when creating new pods.
* Commander - the provisioning component of the Astronomer Platform. It is responsible for interacting with the underlying infrastructure layer. gRPC service to communicate between our API and Kubernetes
* [Prometheus](https://prometheus.io/) - A monitoring platform used to collect metrics from StatsD. Prometheus collects Airflow metrics and pushes them to Granfana for visualization. Email alerts can also be setup to help quickly identify issues.
* [Grafana](https://grafana.com/) - A web dashboard to help visualize and monitor Airflow metrics flowing in from Prometheus. Astronomer has pre-built plenty of dashboards to monitor your cluster or you can create your own custom dashboards to meet your needs.
* [Alert Manager](https://prometheus.io/docs/alerting/alertmanager/) - Email alerts from Prometheus metrics. Enter emails for anyone you want to be alerted in the Orbit UI. These alerts can help notify you of issues on your cluster such as the Airflow Scheduler running slowly.
* [NGINX](https://www.nginx.com/) - NGINX is used as an ingress controller to enforce authentication and direct traffic to the various services such as Airflow webserver, Grafana, Kibana etc. NGINX is also used to serve Airflow logs back up to the Airflow web UI from ElasticSearch.
* [FluentD](https://www.fluentd.org/) - FluentD is a data collector that is used to collect and push the Airflow log data into ElasticSearch.
* [Elasticsearch](https://github.com/elastic/elasticsearch) - A powerful search engine used to centralize and index logs from Airflow deployments.
* [Kibana](https://github.com/elastic/kibana) - A web dashboard to help visualize all of your Airflow logs powered by ElasticSearch. Create your own dashboards to centralize your logs across all of your deployments.
* [Prisma ORM](https://www.prisma.io/) - An interface between the HoustonGraphQL API and your Postgres database. This handles read/writes to the database as well as migrations for upgrades.
* [Astronomer Helm](https://github.com/astronomer/astronomer) - Helm charts for the Astronomer Platform
* [Docker images](https://quay.io/astronomer/) - Docker images for deploying and running Astronomer on DockerHub.

## Airflow Components

When you create an Airflow deployment in Astronomer, the following components are installed:

* [Scheduler](https://airflow.apache.org/scheduler.html) - Determines dependencies and decides when DAGs should run and when tasks are ready to be scheduled.
* [Webserver](https://airflow.apache.org/ui.html) - Airflow???s web UI used to view DAGs, Connections, variables, logs etc.
* [pgBouncer](https://pgbouncer.github.io/) - Provides connection pooling for Postgres. This helps prevent the Airflow database from being overwhelmed by too many connections.
* [StatsD](https://github.com/statsd/statsd) - Provides DAG and task level metrics from Airflow. Astronomer collects these metrics and pushes to a centralized view in Grafana
* Celery components:
  * [Worker](https://docs.celeryproject.org/en/latest/userguide/workers.html) - A service running to process Airflow tasks, which can be scaled up to increase the throughput.
  * [Flower](https://flower.readthedocs.io/en/latest/) - Web UI for Celery distributed task queue. Used to monitor your Airflow worker services
  * [Redis](https://redis.io/) - In memory data store used as the backend by the Celery task queue

## Customer-Supplied Resources

To run Astronomer in your environment, you just need to bring a Kubernetes cluster and a Postgres database:

* [Kubernetes](https://kubernetes.io/) - You bring your own Kubernetes environment (EKS, GKE, AKS, other). Coordinates communication between the services, and provides fault tolerance on failures.
* [PostgreSQL](https://www.postgresql.org/) - database used as the backend for the Houston service as well as each Airflow deployment.
