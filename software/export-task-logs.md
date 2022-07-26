---
sidebar_label: 'Export task logs'
title: 'Export task logs to ElasticSearch'
id: export-task-logs
description: Configure how Astronomer exports task logs to your ElasticSearch instance.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow task logs are stored in a logging backend to ensure you can access them after your Pods terminate. By default, Astronomer uses [Fluentd](https://www.fluentd.org/) to collect task logs and export them to an ElasticSearch instance.

You can configure how Astronomer collects Deployment task logs and exports them to ElasticSearch. The following are the supported methods for exporting task logs to ElasticSearch:

- Using a Fluentd Daemonset pod on each Kubernetes node in your cluster.
- Using container sidecars for Deployment components.

## Export task logs Using a Fluentd DaemonSet

By default, Astronomer Software uses a Fluentd DaemonSet to aggregate task logs. The is the workflow for the default implementation:

- Deployments write task logs to stdout.
- Kubernetes takes the output from stdout and writes it to the Deployment’s node.
- A Fluentd pod reads logs from the node and forwards them to ElasticSearch.

This implementation is recommended for organizations that:

- Run longer tasks using Celery executor.
- Run Astronomer Software in a dedicated cluster.
- Run privileged containers in a cluster with a ClusterRole.

This approach is not suited for organizations that run many small tasks using the Kubernetes executor. Because task logs exist only for the lifetime of the pod, your pods running small tasks might complete before Fluentd can collect their task logs.

## Export logs using container sidecars

You can use a logging sidecar container to collect and export logs. In this implementation:

- Each container running an Airflow component for a Deployment receives its own [Vector](https://vector.dev/) sidecar.
- Task logs are written to a shared directory.
- The Vector sidecar reads logs from the shared directory and writes them to ElasticSearch.

This implementation is recommended for organizations that:

- Run Astronomer Software in a multi-tenant cluster, where security is a concern.
- Use the KubernetesExecutor to run many short-lived tasks, which requires improved reliability.

:::caution

With this implementation, the Vector sidecars each utilize 100m cpu and 384Mi memory. More compute and memory resources are used for exporting logs with sidecars than when using a Fluentd Daemonset.

:::

### Configure logging sidecars

1. Retrieve your `config.yaml` file. See [Apply a config change](apply-platform-config.md).
2. Add the following entry to your `config.yaml` file:

    ```yaml
    global:
      fluentdEnabled: false
      loggingSidecar:
        enabled: true
        name: sidecar-log-consumer
        # needed to prevent zombie deployment worker pods when using KubernetesExecutor
        terminationEndpoint: http://localhost:8000/quitquitquit
    ```
3. Push the configuration change. See [Apply a config change](apply-platform-config.md).


:::info

To revert to the default behavior and export task logs using a Fluentd Daemonset, remove this configuration from your `config.yaml` file.

:::

## Forward Deployment task logs to Elasticsearch

Add your Astronomer Deployment task logs to an existing Elasticsearch instance to centralize log management and analysis. Centralized log management allows you to quickly identify and troubleshoot issues and resolve issues quickly.

### Create an Elastic Deployment and endpoint

1. In your browser, go to `https://cloud.elastic.co/` and create a new Elastic deployment. See [Create a deployment](https://www.elastic.co/guide/en/cloud/current/ec-create-deployment.html#ec-create-deployment).
2. Copy and save your deployment credentials when the **Save the deployment credentials** screen appears.
3. On the Elastic dashboard, click the **Gear** icon for your Deployment.
  ![Elastic Gear icon location](/img/docs/elasticsearch-gear-icon.png)
4. Click **Copy endpoint** next to **Elasticsearch**.

    ![Elastic Copy Endpoint location](/img/docs/elasticsearch-copy-endpoint.png)

5. Optional. Test the Elasticsearch Deployment endpoint:
    - Open a new browser window, paste the endpoint you copied in step 4 in the **Address** bar, and then click **Enter**.
    - Enter the username and password you copied in step 2 and click **Sign in**. Output similar to the following appears:
    ```text
        name	"instance-0000000000"
        cluster_name	"<cluster-name>"
        cluster_uuid	"<cluster-uuid>"
        version	
        number	"8.3.2"
        build_type	"docker"
        build_hash	"8b0b1f23fbebecc3c88e4464319dea8989f374fd"
        build_date	"2022-07-06T15:15:15.901688194Z"
        build_snapshot	false
        lucene_version	"9.2.0"
        minimum_wire_compatibility_version	"7.17.0"
        minimum_index_compatibility_version	"7.0.0"
        tagline	"You Know, for Search"
    ```
6. Run the following command to download the Astronomer Helm chart: 

    ```bash
    helm pull astronomer/astronomer
  ```
7. Run the following command to show the Astronomer Helm chart:

  ```bash
    helm show chart astronomer/astronomer
  ``` 

### Save your Elasticsearch deployment credentials

After you've created an Elastic deployment and endpoint, you have two options to save your Elastic deployment credentials. You can update your Software `config.yaml` file, or you can create a secret in your Software Kubernetes cluster.

<Tabs
    defaultValue="config.yaml"
    values={[
        {label: 'config.yaml', value: 'config.yaml'},
        {label: 'Kubernetes cluster', value: 'kubernetes cluster'},
    ]}>
<TabItem value="config.yaml">

1. Run the following command to base64 encode your Elasticsearch Deployment credentials:

    ```bash
    echo -n "<username>:<password>" | base64
    ```
2. Add the following entry to your `config.yaml` file:

  ```yaml
      global:
        fluentdEnabled: true
        customLogging:
          enabled: true
          scheme: https
            # host endpoint copied from elasticsearch console with https
            # and port number removed.
            host: “<host-URL>”
            port: "9243"
            # secret encoded from above step
            secret: "<secret>"
  ```
3. Add the following entry to your `config.yaml` file to disable internal logging:

  ```yaml
      tags:
        logging: false
  ```
4. Run the following command to upgrade the Astronomer Software release version in the `config.yaml` file:

  ```bash
    helm upgrade -f config.yaml --version=0.27 --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
 
  ```

</TabItem>
<TabItem value="kubernetes cluster">

1. Run the following command to create a secret for your Elasticsearch Deployment credentials in the Kubernetes cluster:

  ```bash
    kubectl create secret generic elasticcreds --from-literal elastic=elastic:samplepassword --namespace=<your-platform-namespace>
  ```
2. Add the following entry to your `config.yaml` file:

  ```yaml
      global:
        fluentdEnabled: true
        customLogging:
          enabled: true
          scheme: https
            # host endpoint copied from elasticsearch console with https
            # and port number removed.
            host: “<host-URL>”
            port: "9243"
            # kubernetes secret containing credentials
            secretName: elasticcreds
  ```
3. Add the following entry to your `config.yaml` file to disable internal logging:

  ```yaml
      tags:
        logging: false
  ```
4. Run the following command to upgrade the Astronomer Software release version in the `config.yaml` file:

  ```bash
    helm upgrade -f config.yaml --version=0.27 --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
 
  ```
  
</TabItem>
</Tabs>

### View the Deployment task logs in Elastic

1. On the Elastic dashboard in the **Elastichsearch Service** area, click the Deployment name.
  ![ElasticDeployment name location](/img/docs/elasticsearch-deployment-name.png)
2. Click **Menu** > **Discover**. The **Create index pattern** screen appears.

    ![Discover menu location](/img/docs/elasticsearch-discover.png)

3. Enter `fluentd.*` in the **Name** field, enter `@timestamp` in the **Timestamp field**, and then click **Create index pattern**.
4. Click **Menu** > **Dashboard** to view the Deployment task logs.