---
sidebar_label: 'Test your Astro project locally'
title: 'Test and troubleshoot your Astro project locally'
id: test-your-astro-project-locally
description: Check the upgrade readiness of your Astro project`
---

One of the Astro CLI's main features is the ability to run Astro projects in a local Airflow environment. It additionally includes commands that you can use to test and debug DAGs both inside and outside of a locally running Airflow environment. Use the following document to learn more about how you can test locally with the Astro CLI before deploying your code changes to a production environment.

## Test before upgrading your Astro project

You can use [`astro dev upgrade-test`](astro-dev-upgrade-test.md) to test your local Astro project against a new version of Astro Runtime to prepare for an upgrade. By default, the command runs the following tests in order to create reports that can help you determine whether your upgrade will be successful:

- **Dependency test**: Identify the packages that have been added, removed, or changed in the upgrade version.
- **DAG test**: Identify Python DAG `import` errors in the upgrade version.

To run these tests, open your Astro project and run:

```sh
astro dev upgrade-test
```

If the tests are successful, the Astro CLI creates a folder in your Astro project called `upgrade-test-<your-current-version>--<your-upgrade-version>`. The folder will contain the following reports:

- `pip_freeze_<current-version>`: The output of the `pip freeze` with your current version.
- `pip_freeze_<upgrade-version>`: The output of the `pip freeze` with your upgrade version.
- `dependency_compare.txt`: The result of the dependency test.
- `Dockerfile`: The updated file used in the upgrade test.
- `dag-test-results.html`: The results of the DAG test.

Use the test results to fix any major package changes or broken DAGs before you upgrade. Refer to the Airflow and Provider package release notes to assist in upgrading your DAGs. After you resolve all conflicts and DAG import errors, you can [upgrade Astro Runtime](upgrade-runtime.md) and [deploy your project](https://docs.astronomer.io/astro/deploy-dags) to an Astro Deployment.

:::info

When you rerun the test for the same project and upgrade version, all the files in the test results folder will be updated. To keep results for a particular test, change the folder name before rerunning the command.

:::

:::tip

If you're testing a local project before deploying to Astro, you can test more accurately by adding  `--deployment-id` flag and specifying your Deployment ID. The Astro CLI uses the image currently running in your Deployment to test against the upgrade version. Note that this flag will use your local DAGs and dependencies against your Astro Deployment's image with the upgrade version of runtime specified. 

:::

Read the following sections to learn more about the contents of each test report. For more information about the command's settings, see the [CLI reference guide](cli/astro-dev-upgrade-test.md).

### Dependency test

To prepare for an upgrade, it's helpful to identify all Python packages which will modified as a result of the upgrade. You can do this using the dependency test. When you run the test, the Astro CLI generates a report called `dependency_compare.txt` in `upgrade-test-<current-version>--<upgrade-version>`. The report shows all Airflow providers and packages that have been removed, added, or updated. 

When you read the results of this test, pay close attention to the `Major Updates` section. Major updates to Python packages are more likely to cause your DAGs to fail. Visit the changelog for any providers listed in this section (for example, the [HTTP provider changelog](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/changelog.html)) to see if the major upgrade will affect your environment. You should also pay attention to anything listed under `Unknown Updates`. These are updates that Astro CLI could not categorize, which can include major upgrades that might cause DAGs to break.

To run only the DAG test against the latest version of Astro Runtime, run the following command in your Astro Project: 

```bash
astro dev upgrade-test --version-test
```

### DAG test

When you upgrade, any Python packages that changed can generate import errors and cause your DAGs to break. These import errors are visible in the UI after you upgrade, but you can address them before upgrading by running the DAG test.

This test uses the [`astro dev parse`](./astro-dev-parse.md) command against the upgrade version and produces a report called `dag-test-report.html` in `upgrade-test-<current-version>--<upgrade-version>`. This HTML report lists the DAGs that will have import errors, along with the first error encountered if you complete an upgrade. You can use this report along with the dependency test report to fix errors in your DAGs before your upgrade.

To run only the DAG test against the latest version of Astro Runtime, run the following command in your Astro Project: 

```bash
astro dev upgrade-test --dag-test
```

## See also

- [Debug DAGs](https://docs.astronomer.io/learn/debugging-dags.md)
- [`astro dev pytest`](./astro-dev-pytest.md)
