---
sidebar_label: "astro dev upgrade-test"
title: "astro dev upgrade-test"
id: astro-dev-upgrade-test
description: Reference documentation for astro dev upgrade-test.
hide_table_of_contents: true
---

Test your local Airflow environment against a new version of Airflow to prepare for an upgrade. This command can be used to test your environment before you upgrade to a specific Airflow, Astro Runtime, or Astronomer Certified version. Specifically, this command will run the following tests:

- Identify dependency conflicts for Python packages in your upgrade version.
- Identify major and minor version changes of the Python packages in your upgrade version.
- Identify DAG import errors that will appear after you upgrade.

This command only works with local Airflow environment. Therefore, this command is useful to test an upgrade locally before pushing the upgrade to a Deployment on Astro. 

## Usage

```bash
astro dev upgrade-test
```

By default, the command runs all three available tests on your project against the latest version of Astro Runtime.
## Options

| Option              | Description                                                                                                                                                                               | Possible Values                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `--airflow-version` | The equivalent of Airflow you want to upgrade to. The default is the latest available version. Note that the Astro CLI will still test against an Astro Runtime image based on the Airflow version you specify. | Any valid [Airflow version](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html). |
| `--runtime-version` | The version of Astro Runtime you want to upgrade to. The default is the latest available version.                                                                                                               | Any valid [Astro runtime version](https://docs.astronomer.io/astro/runtime-release-notes).             |
| `--conflict-test`   | Only run conflict tests. These tests check whether you will have dependency conflicts after you upgrade.                                                                                                | N/A                                                                                                    |
| `--dag-test`        | Only run DAG tests. These tests check whether your DAGs will generate import errors after you upgrade.                                                                                                                            | None                                                                                                  |
| `--deployment-id`        | Specify a Deployment ID to test with an image from an Astro Deployment instead of the image listed in your Astro project Dockerfile.                                                                                                                            | Any valid Deployment ID.                                                                                                  |
| `--version-check`  | Only run version tests. These tests show you how your dependency versions will change after you upgrade.                                                                                                                                                         | None                                                                                                    |

## Examples

To test your DAGs and `requirements.txt` against the latest version of Astro Runtime:

```bash
astro dev upgrade-test
```

To test your DAGs and `requirements.txt` against a version of Astro Runtime based on a specific Airflow version:

```bash
astro dev upgrade-test --airflow-version 2.6.3
```

To check for a major dependency change from the current Airflow version to a specific version of Airflow:

```bash
astro dev upgrade-test --airflow-version 2.6.3 --provider-check 
```

## Related Commands

- [`astro dev pytest`](cli/astro-dev-pytest.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
