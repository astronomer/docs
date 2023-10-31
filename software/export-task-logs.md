---
sidebar_label: 'Configure task log collection'
title: 'Configure task log collection and exporting to ElasticSearch'
id: export-task-logs
description: Configure how Astronomer exports task logs to your ElasticSearch instance.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Airflow task logs are stored in a logging backend to ensure you can access them after your Pods terminate. By default, Astronomer uses [Fluentd](https://www.fluentd.org/) to collect task logs and export them to an ElasticSearch instance.

You can configure how Astronomer collects Deployment task logs and exports them to ElasticSearch. The following are the supported methods for exporting task logs to ElasticSearch:

- Using a Fluentd Daemonset pod on each Kubernetes node in your cluster.
- Using container sidecars for Deployment components.

## Export task logs using a Fluentd DaemonSet

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
    ```

3. Push the configuration change. See [Apply a config change](apply-platform-config.md).

:::info

To revert to the default behavior and export task logs using a Fluentd Daemonset, remove this configuration from your `config.yaml` file and reapply it.

:::

#### Customize Vector logging sidecars

You can customize the default Astronomer Vector logging sidecar to have different transformations and sinks based on your team's requirements.

1. Add the following line to your `config.yaml` file:

    ```yaml {5}
    global:
      loggingSidecar:
        enabled: true
        name: sidecar-log-consumer
        customConfig: true
    ```

2. Push the configuration change. See [Apply a config change](apply-platform-config.md).

3. Create a custom [vector configuration `yaml` file](https://vector.dev/docs/reference/configuration/) to change how and where sidecars forward your logs. The following examples are template configurations for each commonly used sink. For the complete default logging sidecar configmap, see the [Astronomer GitHub](https://github.com/astronomer/airflow-chart/blob/master/templates/logging-sidecar-configmap.yaml).

  <Tabs
      defaultValue="elasticsearch"
      groupId= "customize-vector-logging-sidecars"
      values={[
          {label: 'Elasticsearch', value: 'elasticsearch'},
          {label: 'Honeycomb', value: 'honeycomb'},
          {label: 'Datadog', value: 'datadog'},
      ]}>
  <TabItem value="elasticsearch">

    ```yaml 
    log_schema:
      timestamp_key : "@timestamp"
    data_dir: "${SIDECAR_LOGS}"
    sources:
      airflow_log_files:
        type: file
        include:
          - "${SIDECAR_LOGS}/*.log"
        read_from: beginning
    transforms:
      transform_syslog:
        type: add_fields
        inputs:
          - airflow_log_files
        fields:
          component: "${COMPONENT:--}"
          workspace: "${WORKSPACE:--}"
          release: "${RELEASE:--}"
    
      transform_task_log:
        type: remap
        inputs:
          - transform_syslog
        source: |-
          # Parse Syslog input. The "!" means that the script should abort on error.
          . = parse_json!(.message)
          .@timestamp = parse_timestamp(.timestamp, "%Y-%m-%dT%H:%M:%S%Z") ?? now()
          .@date_nano = parse_timestamp(.timestamp, "%Y-%m-%dT%H:%M:%S%Z") ?? now()
          .check_log_id = exists(.log_id)
          if .check_log_id != true {
          .log_id = join!([.dag_id, .task_id, .execution_date, .try_number], "_")
          }
          .offset = to_int(now()) * 1000000000 + to_unix_timestamp(now()) * 1000000
    
      transform_remove_fields:
        type: remove_fields
        inputs:
          - transform_task_log
        fields:
          - host
          - file
    
    sinks:
      out:
        type: elasticsearch
        inputs:
          - transform_remove_fields
        mode: bulk
        compression: none
        endpoint: "http://example-host:<example-port>"
        auth:
          strategy: "basic"
          user: "example-user"
          password : "example-pass"
        bulk:
          index: "vector.${RELEASE:--}.%Y.%m.%d"
          action: create
    ```

  </TabItem>
  <TabItem value="datadog">

    ```yaml 
    log_schema:
      timestamp_key : "@timestamp"
    data_dir: "${SIDECAR_LOGS}"
    sources:
      generate_syslog:
        type: file
        include:
          - "${SIDECAR_LOGS}/*.log"
        read_from: beginning
    transforms:
      transform_syslog:
        type: add_fields
        inputs:
          - generate_syslog
        fields:
          component: "${COMPONENT:--}"
          workspace: "${WORKSPACE:--}"
          release: "${RELEASE:--}"
      transform_task_log:
        type: remap
        inputs:
          - transform_syslog
        source: |-
          # Parse Syslog input. The "!" means that the script should abort on error.
          . = parse_json!(.message)
          .@timestamp = parse_timestamp(.timestamp, "%Y-%m-%dT%H:%M:%S%Z") ?? now()
          .check_log_id = exists(.log_id)
          if .check_log_id != true {
          .log_id = join!([.dag_id, .task_id, .execution_date, .try_number], "_")
          }
          .offset = to_int(now()) * 1000000000 + to_unix_timestamp(now()) * 1000000
    sinks:
      my_sink_id:
        type: datadog_logs
        inputs:
          - transform_task_log
        site: us1.datadoghq.com
        default_api_key: <your-api-key>
        encoding:
          codec: json
    ```

  </TabItem>
  <TabItem value="honeycomb">

    ```yaml
    log_schema:
      timestamp_key : "@timestamp"
    data_dir: "${SIDECAR_LOGS}"
    sources:
      generate_syslog:
        type: file
        include:
          - "${SIDECAR_LOGS}/*.log"
        read_from: beginning
    transforms:
      transform_syslog:
        type: add_fields
        inputs:
          - generate_syslog
        fields:
          component: "${COMPONENT:--}"
          workspace: "${WORKSPACE:--}"
          release: "${RELEASE:--}"
    sinks:
      my_sink_id:
        type: honeycomb
        inputs:
          - transform_syslog
        api_key: <your-api-key>
        dataset: my-honeycomb-dataset
    
    ```

  </TabItem>

  </Tabs>

4. Run the following command to add the configuration file to your cluster as a Kubernetes secret:

    ```sh
    kubectl create secret generic sidecar-config --from-file=vector-config.yaml=vector-config.yaml
    ```

5. Run the following command to annotate the secret so that it's automatically applied to all new Deployments:

    ```sh
    kubectl annotate secret secret-name astronomer.io/commander-sync="platform-release=astronomer"
    ```

6. Run the following command to sync existing Deployments with the new configuration:

    ```sh
    kubectl create job --from=cronjob/astronomer-config-syncer sync-secrets -n astronomer
    ```

## Use an external Elasticsearch instance for Airflow task log management

Add Airflow task logs from your Astronomer Deployment to an existing Elasticsearch instance on [Elastic Cloud](https://www.elastic.co/cloud/) to centralize log management and analysis. Centralized log management allows you to quickly identify, troubleshoot, and resolve task failure issues. Although these examples use Elastic Cloud, you can also use AWS Managed OpenSearch Service or any other elastic service (managed or hosted). With an external Elasticsearch instance configured for Astronomer Software, you can see the logs in your Elasticsearch instance and browse the logs from the Software UI.

### Create an Elastic Deployment and endpoint

1. In your browser, go to `https://cloud.elastic.co/` and create a new Elastic Cloud deployment. See [Create a deployment](https://www.elastic.co/guide/en/cloud/current/ec-create-deployment.html#ec-create-deployment).
2. Copy and save your Elastic Cloud deployment credentials when the **Save the deployment credentials** screen appears.
3. On the Elastic dashboard, click the **Gear** icon for your Deployment.
  ![Elastic Gear icon location](/img/software/elasticsearch-gear-icon.png)
4. Click **Copy endpoint** next to **Elasticsearch**.

    ![Elastic Copy Endpoint location](/img/software/elasticsearch-copy-endpoint.png)

5. Optional. Test the Elastic Cloud deployment endpoint:
    - Open a new browser window, paste the endpoint you copied in step 4 in the **Address** bar, and then press **Enter**.
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

### Save your Elastic Cloud deployment credentials

After you've created an Elastic deployment and endpoint, you have two options to store your Elastic deployment credentials. You can store the credentials in your Astronomer Software helm values, or for greater security, as a secret in your Astronomer Software Kubernetes cluster. For additional information about adding an Astronomer Software configuration change, see [Apply a config change](apply-platform-config.md).

<Tabs
    defaultValue="configyaml"
    groupId= "save-your-elastic-cloud-deployment-credentials"
    values={[
        {label: 'config.yaml', value: 'configyaml'},
        {label: 'Kubernetes secret', value: 'kubernetessecret'},
    ]}>
<TabItem value="configyaml">

1. Run the following command to base64 encode your Elastic Cloud deployment credentials:

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
     host: "<host-URL>"
     port: "9243"
     # encoded credentials from above step 1
     secret: "<encoded credentials>"    
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
<TabItem value="kubernetessecret">

1. Run the following command to create a secret for your Elastic Cloud Deployment credentials in the Kubernetes cluster:

 ```bash
 kubectl create secret generic elasticcreds --from-literal elastic=<username>:<password> --namespace=<your-platform-namespace>
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
     host: "<host-URL>"
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

### View Airflow task logs in Elastic

1. On the Elastic dashboard in the **Elastichsearch Service** area, click the Deployment name.
  ![ElasticDeployment name location](/img/software/elasticsearch-deployment-name.png)
2. Click **Menu** > **Discover**. The **Create index pattern** screen appears.

    ![Discover menu location](/img/software/elasticsearch-discover.png)

3. Enter `fluentd.*` in the **Name** field, enter `@timestamp` in the **Timestamp field**, and then click **Create index pattern**.
4. Click **Menu** > **Dashboard** to view all of the Airflow task logs for your Deployment on Astronomer.
