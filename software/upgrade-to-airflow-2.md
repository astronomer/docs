---
title: "Upgrade to Airflow 2"
sidebar_label: "Upgrade to Airflow 2"
id: upgrade-to-airflow-2
description: "Prepare for and upgrade to Airflow 2.0+ on Astronomer."
---

This guide explains how to upgrade an Astronomer Software Deployment from Airflow 1.10.15 to 2.3.

As a follow up to Airflow 2.0, Airflow 2.3 was released in May 2022 with new features like dynamic task mapping and a Grid view in the Airflow UI. Given the significance of this release, Astronomer is providing full support for Airflow 2.3 until October 2023.

Astronomer strongly recommends upgrading any Astronomer Software Deployments currently running Airflow 1.10.15 to Airflow 2.3.

## The benefits of Airflow 2.0+

Airflow 2.0 was built to be fast, reliable, and infinitely scalable. Among the hundreds of new features both large and small, Airflow 2.0 includes:

- [Refactored Airflow Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html#running-more-than-one-scheduler) for enhanced performance and high-availability.
- [Full REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) that enables more opportunities for automation.
- [Smart Sensors](https://airflow.apache.org/docs/apache-airflow/stable/smart-sensor.html) that execute as single, long-running tasks.
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#taskflow-api) for a simpler way to pass information between tasks.
- [Independent Providers](https://github.com/apache/airflow/tree/master/airflow/providers) for improved usability and a more agile release cadence.
- Simplified KubernetesExecutor for ultimate flexibility in configuration.
- [UI/UX Improvements](https://github.com/apache/airflow/pull/11195) including a new Airflow UI and auto-refresh button in the **Graph** view.

Airflow 2.3 subsequently introduced several powerful features, the most notable of which is [dynamic task mapping](https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html). For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) and the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).

## Prerequisites

This setup requires:

- The latest version of the [Astro CLI](configure-cli.md).
- An Astro project running Airflow 1.10.15. If your Astro project uses Airflow 1.10.14 or earlier, upgrade to 1.10.15 using the [standard upgrade process](manage-airflow-versions.md) before following these steps.

## Step 1: Run the Airflow upgrade check script

Most Airflow 1.10.15 DAGs will work in Airflow 2.0, though not all. The Airflow 2.0 upgrade check script can check for compatibility issues in your DAG code.

To run the Airflow 2.0 upgrade check script, open your Astro project and run the following command:

```shell
astro dev upgrade-check
```

This command installs the latest version of the `apache-airflow-upgrade-check` package at runtime and outputs results from the corresponding Airflow CLI command.

In the upgrade check output, you can ignore the `Fernet is enabled by default` and `Check versions of PostgreSQL, MySQL, and SQLite to ease upgrade to Airflow 2.0` tests. All of these details are handled by Astronomer. You can also ignore the and `Users must set a kubernetes.pod_template_file value` test even if you are running the Kubernetes executor.

For more information on upgrade check functionality, see [Upgrade Check Script](https://airflow.apache.org/docs/apache-airflow/2.1.3/upgrade-check.html) in Apache Airflow documentation.

## Step 2: Prepare Airflow 2.0 DAGs

The next step is to review the results from Airflow's upgrade check script and make all necessary changes to your import statements, DAGs, and configurations.

### a. Import operators from backport providers

All Airflow 2.0 operators and extras are backwards compatible with both Airflow 1.10.14 and Airflow 1.10.15. To use these providers:

1. Add all necessary providers in your `requirements.txt` file
2. Modify your import statements
3. Add any extras if needed

For more information, see [1.10.15 Backport Providers](https://airflow.apache.org/docs/apache-airflow/1.10.15/backport-providers.html) in Apache Airflow documentation, or see the collection of [Backport Providers in PyPi](https://pypi.org/search/?q=apache-airflow-backport-providers&o=).

### b. Modify Airflow DAGs

Depending on your DAGs, you might need to modify your code to be 2.0-compatible. This can include:

- Changes to undefined variable handling in templates.
- Changes to the KubernetesPodOperator.
- Changing the default value for `dag_run_conf_overrides_params`.

For more compatibility considerations, see [Step 5: Upgrade Airflow DAGs](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/upgrading-to-2.html#step-5-upgrade-airflow-dags) in Apache Airflow documentation.

## Step 3: Upgrade to Airflow 2.3

If your DAGs and configurations pass the upgrade check script above, you're ready to officially upgrade to Airflow 2.3.0. The upgrade process itself is the same as any other on Astronomer.

To upgrade to Airflow 2.3.0,

1. Initialize the Airflow upgrade process via the Astronomer UI or CLI.
2. Depending on what distribution of Airflow you want to use, add one of the following lines to your project's `Dockerfile`:

    ```dockerfile
    FROM quay.io/astronomer/astro-runtime:5.0.4
    ```

    ```dockerfile
    FROM quay.io/astronomer/ap-airflow:2.3.0-onbuild
    ```

3. Modify all backport providers and replace them with fully supported [provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html). For example, if you were using the [Mongo backport provider](https://pypi.org/project/apache-airflow-backport-providers-mongo/), replace `apache-airflow-backport-providers-mongo` with `apache-airflow-providers-mongo` in your `requirements.txt` file. For more information, see [Airflow documentation on provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html).
4. Restart your local environment and open the Airflow UI to confirm that your upgrade was successful.
5. [Deploy your project](deploy-cli.md) to Astronomer.

### Upgrade considerations

Apache Airflow 2.3 includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 2.3, consider the following:

- Upgrading to Airflow 2.3 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment. During the upgrade, scheduled tasks will continue to execute but new tasks will not be scheduled.
- Once you upgrade successfully to Airflow 2.3, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer Support](https://support.astronomer.io). If requested, Astronomer can drop incompatible tables from your metadata database.
