---
title: "Upgrade to Airflow 2"
sidebar_label: "Upgrade to Airflow 2"
id: upgrade-to-airflow-2
description: "Prepare for and upgrade to Airflow 2 on Astronomer."
---

This guide explains how to upgrade an Astronomer Software Deployment from Airflow 1.10.15 to 2.3.

As a follow up to Airflow 2, Airflow 2.3 was released in May 2022 with new features like dynamic task mapping and a Grid view in the Airflow UI. Given the significance of this release, Astronomer is providing full support for Airflow 2.3 until October 2023.

Astronomer strongly recommends upgrading any Astronomer Software Deployments currently running Airflow 1.10.15 to Airflow 2.3.

## The benefits of Airflow 2

Airflow 2 was built to be fast, reliable, and infinitely scalable. Among the hundreds of new features both large and small, Airflow 2 includes:

- [Refactored Airflow Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html#running-more-than-one-scheduler) for enhanced performance and high-availability.
- [Full REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) that enables more opportunities for automation.
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html) for a simpler way to pass information between tasks.
- [Independent Providers](https://github.com/apache/airflow/tree/master/airflow/providers) for improved usability and a more agile release cadence.
- Simplified KubernetesExecutor for ultimate flexibility in configuration.
- [UI/UX Improvements](https://github.com/apache/airflow/pull/11195) including a new Airflow UI and auto-refresh button in the **Graph** view.

Airflow 2.3 subsequently introduced several powerful features, the most notable of which is [dynamic task mapping](https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html). For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) and the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).

## Prerequisites

This setup requires:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- An Astro project running Airflow 1.10.15. If your Astro project uses Airflow 1.10.14 or earlier, upgrade to 1.10.15 using the [standard upgrade process](manage-airflow-versions.md).

## Step 1: Run the Airflow upgrade check script

Not all Airflow 1.10.15 DAGs work in Airflow 2,. The Airflow 2 upgrade check script can check for compatibility issues in your DAG code.

To run the Airflow 2 upgrade check script and install the latest version of the `apache-airflow-upgrade-check` package at runtime, open your Astro project and run the following command:

```shell
astro dev upgrade-check
```

This command outputs the results of tests which check the compatibility of your DAGs with Airflow 2.

In the upgrade check output, you can ignore the following entries:

- `Fernet is enabled by default`
- `Check versions of PostgreSQL, MySQL, and SQLite to ease upgrade to Airflow 2`
- `Users must set a kubernetes.pod_template_file value`

For more information about upgrade check functionality, see [Upgrade Check Script](https://airflow.apache.org/docs/apache-airflow/2.1.3/upgrade-check.html) in Apache Airflow documentation.

## Step 2: Prepare Airflow 2 DAGs

Review the results from the Airflow upgrade check script and then update your import statements, DAGs, and configurations if necessary.

### a. Import operators from backport providers

All Airflow 2 providers supported a backported package version for Airflow 1.10.15. You can use backported provider packages to test your DAGs with Airflow 2's functionality in a 1.10.15 environment.

1. Add all necessary backported providers to the `requirements.txt` file of the Astro project.
2. Modify the import statements of your DAGs to reference the backported provider packages.
3. Run your DAGs to test their compatibility with Airflow 2 providers.

For more information, see [1.10.15 Backport Providers](https://airflow.apache.org/docs/apache-airflow/1.10.15/backport-providers.html) in Apache Airflow documentation, or see the collection of [Backport Providers in PyPi](https://pypi.org/search/?q=apache-airflow-backport-providers&o=).

### b. Modify Airflow DAGs

Depending on your DAGs, you might need to make the following changes to make sure your code is compatible with Airflow 2:

- Changes to undefined variable handling in templates.
- Changes to the KubernetesPodOperator.
- Changing the default value for `dag_run_conf_overrides_params`.

For other compatibility considerations, see [Step 5: Upgrade Airflow DAGs](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/upgrading-to-2.html#step-5-upgrade-airflow-dags) in Apache Airflow documentation.

## Step 3: Upgrade to Airflow 2.3

If the upgrade check script didn't identify any issues with your existing DAGs and configurations, you're ready to upgrade to Airflow 2.3.0.

To upgrade to Airflow 2.3.0,

1. Initialize the Airflow upgrade process via the Astronomer UI or CLI.
2. Depending on what distribution of Airflow you want to use, add one of the following lines to your project's `Dockerfile`:

    ```docker
    FROM quay.io/astronomer/astro-runtime:5.0.4
    ```

    ```docker
    FROM quay.io/astronomer/ap-airflow:2.3.0-onbuild
    ```

3. Modify all backport providers and replace them with fully supported [provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html). For example, if you were using the [Mongo backport provider](https://pypi.org/project/apache-airflow-backport-providers-mongo/), replace `apache-airflow-backport-providers-mongo` with `apache-airflow-providers-mongo` in your `requirements.txt` file. For more information, see [Airflow documentation on provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html).
4. Restart your local environment and open the Airflow UI to confirm that your upgrade was successful.
5. [Deploy your project](deploy-cli.md) to Astronomer.

### Upgrade considerations

Airflow 2.3 includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 2.3, consider the following:

- Upgrading to Airflow 2.3 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment. During the upgrade, scheduled tasks will continue to execute but new tasks will not be scheduled.
- Once you upgrade successfully to Airflow 2.3, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, contact [Astronomer Support](https://support.astronomer.io). If necessary, Astronomer can remove incompatible tables from your metadata database.
