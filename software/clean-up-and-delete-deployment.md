---
sidebar_label: 'Clean up and delete Deployments'
title: 'Clean up and delete Astronomer Software Deployments'
id: clean-up-and-delete-deployment
description: Configure your Airflow Deployment's resources on Astronomer Software.
---

This document explains how to manage the deletion and cleanup of Deployments on your Astronomer Software cluster.

## Delete a Deployment

You can delete an Airflow Deployment using the **Delete Deployment** button at the bottom of the Deployment's **Settings** tab.

When you delete a Deployment, you delete your Airflow webserver, scheduler, metadata database, and deploy history, and you lose any configurations set in the Airflow UI.

By default, Astro performs a _soft delete_ when you delete a Deployment. After you delete a Deployment, your Astronomer database, the corresponding `Deployment` record receives a `deletedAt` value and continues to persist until permanently deleted through a _hard delete_. A hard delete includes both the Deployment's metadata database and the Deployment entry in your Astronomer database. 14 days after your Deployment's soft delete, Astronomer automatically runs a hard delete cronjob that deletes any values that remained after your soft delete.

:::tip

Astronomer recommends regularly doing a database audit to confirm that you hard delete databases.

:::

### Configure Deployment hard delete jobs

Astronomer runs a cronjob to hard delete the deleted Deployment's metadata database and Deployment entry in your Astronomer database at midnight on a specified day. You can enable whether this cronjob runs or not, how many days after your soft delete to run the cronjob, and what time of day to run the cronjob by editing `astronomer.houston.cleanupDeployments` in your Astronomer Helm chart.

The following is an example of how you might configure the cronjob in your Helm chart:

```yaml
# Cleanup deployments that have been soft-deleted
  # This clean up runs as a CronJob
  cleanupDeployments:
    # Enable the clean up CronJob
    enabled: true

    # Default time for the CronJob to run https://crontab.guru/#0_0_*_*_*
    schedule: "0 0 * * *"

    # Number of days after the Deployment deletion to run the CronJob
    olderThan: 14
```

### Manually hard delete a Deployment

To reuse a custom release name given to an existing Deployment after a soft delete, but before Astronomer automatically cleans up any persisting Deployment records, you need to hard delete both the Deployment's metadata database and the Deployment's entry in your Astronomer database.

1. Enable hard delete as an option at the platform level. To enable this feature, set `astronomer.houston.config.deployments.hardDeleteDeployment: true` in your `config.yaml` file and push the changes to your platform as described in [Apply a config change](apply-platform-config.md).

2. Hard delete a Deployment with the Software UI or Astro CLI.
  - **Software UI:** Go to the Deployment's **Settings** tab and select **Delete Deployment**. Then, select the **Hard Delete?** checkbox before confirming **Delete Deployment**.

    ![Hard delete checkbox](/img/software/hard-delete.png)

  - **Astro CLI:** Run `astro deployment delete --hard`.

This action permanently deletes all data associated with a Deployment, including the database and underlying Kubernetes resources.

## Clean Deployment task metadata

You can run a cronjob to automatically archive task and DAG metadata from your Deployment. This job runs [`airflow db clean`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#clean) for all of your Deployments and exports the results for each Deployment as a file to your external storage service. To run this job for a Deployment, you must install the Astronomer-maintained `airflow-dbcleanup-plugin` on the Deployment.

1. For each of your Deployments, add the following line to the `requirements.txt` file of your Deployment's Astro project. Replace `<latest-version>` with the latest available version in the [`airflow-dbcleanup-plugin` GitHub repository](https://github.com/astronomer/airflow-dbcleanup-plugin/releases).

    ```text
    https://github.com/astronomer/airflow-dbcleanup-plugin/releases/download/<latest-version>/astronomer_dbcleanup_plugin-<latest-version>-py3-none-any.whl
    ```

2. Configure an Airflow connection to your external storage service in JSON or URI format so that it can be stored as an environment variable. You must use a service account to authenticate to your service. See [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#storing-connections-in-environment-variables) to learn how to configure your connection.
3. Store the connection environment variable as a Kubernetes Secret on your Astronomer cluster. See [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret).
4. Add the following configuration to your `values.yaml` file and change the default values as needed.

    ```yaml
    houston:
      cleanupAirflowDb:
        # Enable cleanup CronJob
        enabled: false

        # Default run is at 5:23 every morning https://crontab.guru/#23_5_*_*_*
        schedule: "23 5 * * *"

        # Cleanup deployments older than this many days
        olderThan: 365

        # Output path of archived data csv export
        outputPath: "/tmp"

        # Delete archived tables
        purgeArchive: true

        # Print out the deployments that should be cleaned up and skip actual cleanup
        dryRun: false

        # Name of file storage provider, supported providers - aws/azure/gcp/local
        provider: local

        # Name of the provider bucket name / local file path
        bucketName: "/tmp"

        # The name of the Kubernetes Secret containing your Airflow connection
        providerEnvSecretName: "<your-secret-name>"

        # Run cleanup on specific table or list of tables in a comma separated format
        tables: ""
    ```

5. Push the configuration change. See [Apply a config change](apply-platform-config.md).
