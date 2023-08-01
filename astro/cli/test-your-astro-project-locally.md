---
sidebar_label: 'Test your Astro project locally'
title: 'Test and troubleshoot your Astro project locally'
id: test-your-astro-project-locally
---

One of the Astro CLI's main features is the ability to run Astro projects in a local Airflow environment. It additionally includes a few commands that you can use to test and debug DAGs both inside and outside of a locally running environment. Use the following document to learn more about how you can test locally with the Astro CLI before deploying your code changes to a production environment.

## Test before upgrading your Astro project

You can use [`astro dev upgrade-test`](astro-dev-upgrade-test.md) to test your local Astro project against a new version of Astro Runtime to prepare for an upgrade. By default, the command runs three tests that create reports that can help you determine whether your upgrade will be successful before you start it:

- **Conflict test**: Checks for conflicts between your current dependencies and the dependencies in the new Astro Runtime version.
- **Dependency change test**: Shows what packages have been added, removed, or updated in the new Astro Runtime version.
- **DAG test**: Checks your DAGs for import errors with the new Astro Runtime version.

To run these tests, open your Astro project and run:

```sh
astro dev upgrade-test
```

The results of your tests appear in a new folder called `upgrade-test-<current-version>--<new-version>`. Use the test results to fix any dependency conflicts or broken DAGs before you upgrade. Refer to the Airflow and Provider package release notes to assist in upgrading your DAGs. After you resolve all conflicts and DAG import errors, you can [upgrade Astro Runtime](upgrade-runtime.md) and deploy your project to an Astro Deployment.

Use the following sections to learn more about the contents of each test report. For more information about the command's settings, see the [CLI reference guide](cli/astro-dev-upgrade-test.md).

:::tip

If you're testing a local project before deploying to a Deployment on Astro Hosted or Hybrid, you test more accurately by adding  `--deployment-id` flag and specifying your Deployment ID. The Astro CLI uses the image currently running in your Deployment to test against the upgraded version. USe this flag to test a Deployment upgrade with local DAGs and dependencies.

:::

### Conflict test

The conflict test checks for conflicts between the dependencies listed in your `requirements.txt` file and the dependencies of the new Astro Runtime version. The test finds conflicts by creating a list of all the dependencies of the new Airflow version, adding your requirements to this list, and running a [`pip compile`](https://stackoverflow.com/questions/66751657/what-does-pip-compile-do-what-is-its-use-how-do-i-maintain-the-contents-of-my). 

The CLI will produce logs for any dependency conflicts as it finds them. You can also find the final result of the test in `./upgrade-test-<current-version>--<new-version>/conflict-test-result.txt`. 

To run only the conflict test, run `astro dev upgrade-test --conflict-test`.

### Dependency change test

This dependency change test produces a report of pip packages will change after you upgrade. The report shows all Airflow providers and packages that have been removed, added, or updated. You can find the report in `<your-astro-project/upgrade-test-<current-version>--<new-version>/dependency_compare.txt`. 

When you read the results of this test, pay close attention to Airflow providers that will have a major upgrade. Visit the changelog for these providers (for example, the [HTTP provider changelog](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/changelog.html) to see if the major upgrade will affect your environment. You should also pay attention to anything listed under `Unknown Updates`. These are updates that Astro CLI could not categorize, which can include major upgrades that might cause DAGs to break.

To run only the version test, run `astro dev upgrade-test --version-test`.

### DAG Test

The DAG test produces a report of DAGs that have import errors after you upgrade. For each DAG with an import error, the report shows the DAG name and the first error encountered by the import test. You can find the report in `<your-astro-project/upgrade-test-<current-version>--<new-version>/dag-test-report.html`. 

Use the results of this test alongside the dependency change test to fix errors in your DAGs caused by the upgrade. You can also use this report to estimate the time you need to complete the upgrade.

To run only the DAG test, run `astro dev upgrade-test --dag-test`

### Test Results Overview

The tests result in a folder that contains the results of the tests. The folder created by the tests will be called `upgrade-test-<old-version>--<new-version>` and will be in your Astro project folder. The version shown in the name is not the Airflow Version. They are either the Runtime or Certified version. The following files will be in the test result folder if all the tests run successfully:

- `conflict-test-results.txt` - This file is the pip compile result from the conflict test.
- `pip_freeze_<old-version>` - This file results from running pip freeze in the old(not upgraded) environment. Versions are either Runtime or Certified versions
- `pip_freeze_<new-version>` - This file results from running pip freeze in the upgraded environment. Versions are either Runtime or Certified versions.
- `dependency_compare.txt` - This file contains the result of the dependency version test. This file contains a list of pip packages that were added, removed, or changed after the upgrade.
- `Dockerfile` - Upgraded `Dockerfile` used in the dependency version and DAG test.
- `dag-test-results.html` - the HTML file containing the results of the DAG test. DAGs that have import errors after the upgrade will be shown here along with the first error encountered.

Every time you rerun the test for the same upgrade all the files in the test results folder will be changed. If you’d like to keep results for a particular test run make sure to change the folder name.
