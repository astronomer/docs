---
sidebar_label: 'Logging'
title: 'Kibana Logging on Astronomer Enterprise'
id: kibana-logging
description: Use Kibana to monitor platform-wide Airflow logs from Astronomer Enterprise.
---

All Airflow logs from your Astronomer logs will flow to Elasticsearch and can be visualized on Kibana. Like Grafana, this view is only available to system admins.

## Setup

To setup logging in Kibana, navigate to `kibana.BASEDOMAIN`

![Index Pattern](https://assets2.astronomer.io/main/docs/ee/index_pattern.png)


Navigate to `Management` and create an index pattern for `fluentd.*`
Elasticsearch uses [index patterns](https://www.elastic.co/guide/en/kibana/current/index-patterns.html) to organize how you explore data. Setting `fluentd.*` as the index means that Kibana will display all logs from all deployments (Astronomer uses `fluentd` to ship logs from pods to ElasticSearch).

Set `@timestamp` as the  `Time Filter` on the next screen.

## Discover

Once the index pattern has been confirmed, the `Discover` tab will show logs as they come in.

![Add fields](https://assets2.astronomer.io/main/docs/ee/add_fields.png)

From this view, you can add filters to see logs as they come in from all Airflow deployments. You can also add fields to filter by:


## Dashboards

Custom dashboards can be created in the `Dashboard` view.
