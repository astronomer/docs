---
title: 'Alerting in Astronomer Software'
sidebar_label: 'Software alerts'
id: platform-alerts
---

You can use two built-in alerting solutions for monitoring the health of Astronomer:

- Deployment-level alerts, which notify you when the health of an Airflow Deployment is low or if any of Airflow's underlying components are underperforming, including the Airflow scheduler.
- Platform-level alerts, which notify you when a component of your Software installation is unhealthy, such as Elasticsearch, Astronomer's Houston API, or your Docker Registry.

These alerts fire based on metrics collected by Prometheus. If the conditions of an alert are met, [Prometheus Alertmanager](https://prometheus.io/docs/alerting/alertmanager) handles the process of sending the alert to the appropriate communication channel.

Astronomer offers built-in Deployment and platform alerts, as well as the ability to create custom alerts in Helm using [PromQL query language](https://prometheus.io/docs/prometheus/latest/querying/basics/). This guide provides all of the information you need to configure Prometheus Alertmanager, subscribe to built-in alerts, and create custom alerts.

In addition to configuring platform and Deployment-level alerts, you can also set email alerts that trigger on DAG and task-based events. For more information on configuring Airflow alerts, read [Airflow alerts](airflow-alerts.md).

## Anatomy of an alert

Platform and Deployment alerts are defined in YAML and use [PromQL queries](https://prometheus.io/docs/prometheus/latest/querying/basics/) for alerting conditions. Each `alert` YAML object contains the following key-value pairs:

* `expr`: The logic that determines when the alert will fire, written in PromQL.
* `for`: The length of time that the `expr` logic has to be true for the alert to fire. This can be defined in minutes or hours (e.g. `5m` or `2h`).
* `labels.tier`: The level of your platform that the alert should operate at. Deployment alerts have a tier of `airflow`, while platform alerts have a tier of `platform`.
* `labels.severity`: The severity of the alert. Can be `info`, `warning`, `high`, or `critical`.
* `annotations.summary`: The text for the alert that's sent by Alertmanager.
* `annotations.description`: A human-readable description of what the alert does.

By default, Astronomer checks for all alerts defined in [the Prometheus configmap](https://github.com/astronomer/astronomer/blob/master/charts/prometheus/templates/prometheus-alerts-configmap.yaml).

## Subscribe to alerts

Astronomer uses [Prometheus Alertmanager](https://prometheus.io/docs/alerting/configuration/) to manage alerts. This includes silencing, inhibiting, aggregating, and sending out notifications using methods such as email, on-call notification systems, and chat platforms.

You can configure [Alertmanager](https://prometheus.io/docs/alerting/configuration/) to send built-in Astronomer alerts to email, HipChat, PagerDuty, Pushover, Slack, OpsGenie, and more by defining alert receivers in the [Alertmanager Helm chart](https://github.com/astronomer/astronomer/blob/master/charts/alertmanager/values.yaml) and modifying the [Alertmanager `email-config` parameter](https://prometheus.io/docs/alerting/latest/configuration/#email_config).

### Create alert receivers

Alertmanager uses [receivers](https://prometheus.io/docs/alerting/latest/configuration/#receiver) to integrate with different messaging platforms. To begin sending notifications for alerts, you first need to define `receivers` in YAML using the [Alertmanager Helm chart](https://github.com/astronomer/astronomer/blob/master/charts/alertmanager/values.yaml).

This Helm chart contains groups for each possible alert type based on `labels.tier` and `labels.severity`. Each receiver must be defined within at least one alert type in order to reveive notifications.

For example, adding the following receiver to `receivers.platformCritical` would cause platform alerts with `critical` severity to appear in a specified Slack channel:

```yaml
alertmanager:
  receivers:
    # Configs for platform alerts
    platform: 
      email_configs:
        - smarthost: smtp.sendgrid.net:587
          from: <your-astronomer-alert-email@company.com>
          to: <your-email@company.com>
          auth_username: apikey
          auth_password: SG.myapikey1234567891234abcdef_bKY
          send_resolved: true
    platformCritical:
      slack_configs:
        - api_url: https://hooks.slack.com/services/abc12345/abcXYZ/xyz67890
          channel: '#<your-slack-channel-name>'
          text: |-
            {{ range .Alerts }}{{ .Annotations.description }}
            {{ end }}
          title: '{{ .CommonAnnotations.summary }}'
```

By default, the Alertmanager Helm chart includes alert objects for platform, critical platform, and Deployment alerts. To configure a receiver for a non-default alert type, such as Deployment alerts with high severity, add that receiver to the `customRoutes` list with the appropriate `match_re` and receiver configuration values. For example:

```yaml
alertmanager:
  customRoutes:
  - name: deployment-high-receiver
    match_re:
      tier: airflow
      severity: high
```

Note that if you have a `platform`, `platformCritical`, or `airflow` receiver defined in the prior section, you do not need a `customRoute` to route to them. They will automatically be routed to by the `tier` label.

For more information on building and configuring receivers, refer to [Prometheus documentation](https://prometheus.io/docs/alerting/configuration/).

### Push alert receivers to Astronomer

To add a new receiver to Astronomer, add your receiver configuration to your `config.yaml` file and push the changes to your installation as described in [Apply a config change](apply-platform-config.md). The receivers you add must be specified in the same order and format as they appear in the Alertmanager Helm chart. Once you push the alerts to Astronomer, they are automatically added to the [Alertmanager ConfigMap](https://github.com/astronomer/astronomer/blob/master/charts/alertmanager/templates/alertmanager-configmap.yaml).

## Create custom alerts

In addition to subscribing to Astronomer's built-in alerts, you can also create custom alerts and push them to Astronomer.

Platform and Deployment alerts are defined in YAML and pushed to Astronomer with the Prometheus Helm chart. For example, the following alert will fire if more than 2 Airflow schedulers across the platform are not heartbeating for more than 5 minutes:

```yaml
prometheus:
  additionalAlerts:
    # Additional rules for the 'platform' alert group
    # Provide as a block string in yaml list form
    platform: |
      - alert: ExamplePlatformAlert
        # If greater than 10% task failure
        expr: count(rate(airflow_scheduler_heartbeat{}[1m]) <= 0) > 2
        for: 5m
        labels:
          tier: platform
          severity: critical  
        annotations:
          summary: {{ printf "%q" "{{value}} airflow schedulers are not heartbeating." }}
          description: If more than 2 Airflow schedulers are not heartbeating for more than 5 minutes, this alert fires.
```

To push custom alerts to Astronomer, add them to the `AdditionalAlerts` section of your `config.yaml` file and push the file with Helm as described in [Apply a config change](apply-platform-config.md).

Once you've pushed the alert to Astronomer, make sure that you've configured receiver to subscribe to the alert. For more information, read [Subscribe to Alerts](platform-alerts.md#subscribe-to-alerts).

## Reference: Deployment alerts

The following table lists some of the most common Deployment alerts that you might receive from Astronomer.

For a complete list of built-in Airflow alerts, see the [Prometheus configmap](https://github.com/astronomer/astronomer/blob/master/charts/prometheus/templates/prometheus-alerts-configmap.yaml).

| Alert                                     | Description                                                                                                                        | Follow-Up                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AirflowDeploymentUnhealthy`              | Your Airflow Deployment is unhealthy or not completely available.                                                                  | Contact [Astronomer support](https://support.astronomer.io).                                                                                                                                                                                                                                                                                                                                                                                               |
| `AirflowEphemeralStorageLimit`            | Your Airflow Deployment has been using more than 5GB of its ephemeral storage for over 10 minutes.                                 | Make sure to continually remove unused temporary data in your Airflow tasks.                                                                                                                                                                                                                                                                                                                                                                                    |
| `AirflowPodQuota`                         | Your Airflow Deployment has been using over 95% of its pod quota for over 10 minutes.                                              | Either increase your Deployment's Extra Capacity in the Software UI or update your DAGs to use less resources. If you have not already done so, upgrade to [Airflow 2.0](https://www.astronomer.io/blog/introducing-airflow-2-0) for improved resource management.                                                                                                                                                                                            |
| `AirflowSchedulerUnhealthy`               | The Airflow scheduler has not emitted a heartbeat for over 1 minute.                                                               | Contact [Astronomer support](https://support.astronomer.io).                                                                                                                                                                                                                                                                                                                                                                                               |
| `AirflowTasksPendingIncreasing`           | Your Airflow Deployment created tasks faster than it was clearing them for over 30 minutes.                                        | Ensure that your tasks are running and completing correctly. If your tasks are running as expected, [raise concurrency and parallelism in Airflow](https://docs.astronomer.io/learn/airflow-scaling-workers), then consider increasing one of the following resources to handle the increase in performance: <ul><li>Kubernetes: Extra Capacity</li><li>Celery: worker Count or worker Resources</li></ul><ul><li>Local Executor: scheduler Resources</li></ul> |
| `ContainerMemoryNearTheLimitInDeployment` | A container in your Airflow Deployment is near its memory quota; it's been using over 95% of its memory quota for over 60 minutes. | Either increase your Deployment's allocated resources in the Software UI or update your DAGs to use less memory. If you have not already done so, upgrade to [Airflow 2.0](https://www.astronomer.io/blog/introducing-airflow-2-0) for improved resource management.                                                                                                                                                                                          |
