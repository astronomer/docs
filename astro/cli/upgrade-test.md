---
sidebar_label: 'Run an Airflow Upgrade Test with the CLI'
title: 'Test an Upgrade of your Airflow Enviroment'
id: upgrade-test
---

<head>
  <meta name="description" content="How to use the Astro CLI command 'astro dev upgrade-test' to see if your Airflow environemnt is ready to be upgraded to a newer version of Airflow." />
</head>

## Overview

You can use the `[astro dev upgrade-test](astro-dev-upgrade-test.md)` command to test your local environment against a new version of Airflow to prepare for an upgrade. You can test an upgrade to a specific Airflow, Astronomer Runtime, or Astronomer Certified version. The command will run three tests that create reports that can help you during the upgrade process:

1. Conflict Test: The first test will tell you if there is a conflict between the dependencies of the new Airflow version and your requirements.
2. Dependency Change Test: The second test tells you what packages have been added, removed, or have had a major, minor, or patch update during the upgrade.
3. DAG Test: The last test will test your DAGs for import errors in the upgraded environment. This test will produce a list of all the DAGs with an import error and the error message for the first error encountered.

All three tests will run in the order above by default. To run all three tests for the latest version of Airflow(Runtime) run `astro dev upgrade-test` in an [Astro Project](https://docs.astronomer.io/astro/cli/get-started-cli#step-1-create-an-astro-project).

## Conflict Test

The following section will discuss the conflict test in detail. To run only the conflict test, run `astro dev upgrade-test --conflict-test` in an [Astro Project](https://docs.astronomer.io/astro/cli/get-started-cli#step-1-create-an-astro-project)[.](https://www.notion.so/Weekly-Astro-CLI-Standup-fe53aed8509a4ad7ab39a0cf622a25eb?pvs=21)

This test looks for conflicts between your requirements and the dependencies of the new version of Airflow. Pip package conflicts can result in build or [DAG import errors](https://docs.astronomer.io/learn/debugging-dags) that cause your upgrade to be unsuccessful. The test finds conflicts by creating a list of all the dependencies of the new Airflow version, adding your requirements to this list, and running a `[pip compile](https://stackoverflow.com/questions/66751657/what-does-pip-compile-do-what-is-its-use-how-do-i-maintain-the-contents-of-my)`. If the command identifies a conflict it will stop and display an error. Look through the logs to find information about the conflict.

Here is an example of logs you may see if there is a conflict:

![Screenshot 2023-06-22 at 3.46.34 PM.png](Upgrade%20Test%20Command%20Documentation%2097ca7ba2fa3641e1ac721658f44ab8a2/Screenshot_2023-06-22_at_3.46.34_PM.png)

In this example, the requirement `protobuf==4.23.3` is conflicting with some of the dependencies of the new Airflow version. The best way to fix this conflict is to remove `protobuf==4.23.3` and re-run the command. You can find the result of the pip compile at `./upgrade-test-<new-version>--<old-version>/conflict-test-result.txt`. You will find the best candidate for `protobuf` in this result.

## Dependency Change Test

The following section will discuss the version test in detail. To run only the version test, run `astro dev upgrade-test --version-test` in an [Astro Project](https://docs.astronomer.io/astro/cli/get-started-cli#step-1-create-an-astro-project).

This test will produce a list of pip packages that have changed during the upgrade. You can find the change in the Airflow version at the top of the file. The CLI categorizes other Airflow providers and packages that have been removed, added, or updated(major, minor, or patch). Airflow Providers Major Updates are most likely to cause DAGs to fail. Visit the changelog (HTTP provider [example](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/changelog.html)) for a Provider Package to see how it changed during a major update. Also, pay special attention to the category Unknown Updates. These are updates that Astro CLI could not categorize. These could be major updates that are causing DAGs to break.

You can find the output of this test at `./upgrade-test-<new-version>--<old-version>/dependency_compare.txt`.

## DAG Test

The following section will discuss the DAG test in detail. To run only the DAG test, run `astro dev upgrade-test --dag-test` in an [Astro Project](https://docs.astronomer.io/astro/cli/get-started-cli#step-1-create-an-astro-project).
This test will produce a report that lists DAGs that have import errors after the upgrade. The DAG name and the first error encountered by the import test will be listed. You can use this information and `dependency_compare.txt` to fix errors in your DAGs caused by the upgrade. You can also utilize this list of failing DAGs to plan the time needed for an upgrade.
You can find the output of this test at `./upgrade-test-<new-version>--<old-version>/dag-test-report.html`. Any browser can open this HTML file.

## Test Results Overview

The tests result in a folder that contains the results of the tests. The folder created by the tests will be called `upgrade-test-<old-version>--<new-version>` and will be in your Astro project folder. The version shown in the name is not the Airflow Version. They are either the Runtime or Certified version. The following files will be in the test result folder if all the tests run successfully:

- `conflict-test-results.txt` - This file is the pip compile result from the conflict test.
- `pip_freeze_<old-version>` - This file results from running pip freeze in the old(not upgraded) environment. Versions are either Runtime or Certified versions
- `pip_freeze_<new-version>` - This file results from running pip freeze in the upgraded environment. Versions are either Runtime or Certified versions.
- `dependency_compare.txt` - This file contains the result of the dependency version test. This file contains a list of pip packages that were added, removed, or changed after the upgrade.
- `Dockerfile` - Upgraded `Dockerfile` used in the dependency version and DAG test.
- `dag-test-results.html` - the HTML file containing the results of the DAG test. DAGs that have import errors after the upgrade will be shown here along with the first error encountered.

Every time you rerun the test for the same upgrade all the files in the test results folder will be changed. If you’d like to keep results for a particular test run make sure to change the folder name.

## Airflow Version VS Runtime Version

You can supply an [Astronomer Runtime](https://docs.astronomer.io/astro/runtime-image-architecture) version (`--runtime-version`) or an Airflow version(`--airflow-version`) when testing an upgrade. In both cases, the CLI uses the [Astronomer Runtime image](https://docs.astronomer.io/astro/runtime-image-architecture) to test the upgrade. The CLI translates the Airflow version to a corresponding Runtime version for you.
If you have authenticated to Astronomer Software, you can test an upgrade using an Astronomer Certified Image. You need to supply the command the flag `--use-astronomer-certified` along with the `--airflow-version` you would like to upgrade to.

## Use Airflow Image from an Astro Deployment for Tests

When upgrading a Deployment on Astro Hosted or Hybrid, you can gather information for more accurate tests by using the  `--deployment-id` flag, If you supply a Deployment Id, the CLI will pull down the image currently running in that Deployment. The CLI will use that image to get the current Airflow(Runtime) version running in your Deployment. It will also compare the dependencies in that image with your upgraded environment for the version test.

The DAGs and requirements tested in the new environment for the DAG test will always come from your local project files.

## Test an Upgrade with a Custom Image

By default, the CLI will create an updated version of your `Dockerfile` by replacing the Runtime image with the desired version. If you are pulling from a custom image in the `FROM` line in your `Dockerfile`, you can provide the image name of the desired version of Airflow with the `--custom-image` flag. The CLI will replace everything shown below in `<image-name>`.

```json
FROM <image-name>
```

## What’s Next?

Use the test results to fix any dependency conflicts or broken DAGs resulting from the upgrade. Refer to the Airflow and Provider package release notes to assist in upgrading your DAGs. In the `dependency_compare.txt` file, you can find the specific Airflow version change and the corresponding changes for each provider package.
Once you resolve all conflicts and DAG import errors, you can deploy your DAGs and upgraded environment to your Astronomer Deployment.