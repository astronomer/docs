---
sidebar_label: "astro dev upgrade-test"
title: "astro dev upgrade-test"
id: astro-dev-upgrade-test
description: Reference documentation for astro dev upgrade-test.
hide_table_of_contents: true
---

Test your local Astro project against a new version of Astro Runtime to prepare for an upgrade. Specifically, this command will run the following tests:

- Identify major and minor version changes of the Python packages in your upgrade version.
- Identify DAG import errors that will appear after you upgrade.

:::tip Using with Astronomer Software

If you are authenticated to Astronomer Software, you can test an upgrade using an Astronomer Certified Image. For this, you must add the flag `--use-astronomer-certified` along with the `--airflow-version` you would like to upgrade to.

:::

## Usage

```bash
astro dev upgrade-test
```

By default, the command runs all three available tests on your project against the latest version of Astro Runtime.

## Options

| Option                    | Description                                                                                                                                                                                                     | Possible Values                                                                                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `-a`, `--airflow-version` | The equivalent of Airflow you want to upgrade to. The default is the latest available version. Note that the Astro CLI will still test against an Astro Runtime image based on the Airflow version you specify. | Any valid [Airflow version](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html). |
| `-d`, `--dag-test`              | Only run DAG tests. These tests check whether your DAGs will generate import errors after you upgrade.                                                                                                          | None                                                                                                   |
| `-i`, `--deployment-id`   | Specify a Deployment ID to test with an image from an Astro Deployment instead of the image listed in your Astro project Dockerfile.                                                                            | Any valid Deployment ID.                                                                               |
| `-n`, `--image-name`      | Name of a custom upgraded image. Updates the FROM line in your Dockerfile to pull this image for the upgrade.                                                                                                        | None                                                                                                   |
| `-v`, `--runtime-version` | The version of Astro Runtime you want to upgrade to. The default is the latest available version.                                                                                                               | Any valid [Astro runtime version](https://docs.astronomer.io/astro/runtime-release-notes).             |
|  `--use-astronomer-certified` | Test against an Astronomer Certified distribution of Airflow. Must be used with `--airflow-version`. | None |
| `--version-test`          | Only run version tests. These tests show you how the versions of your dependencies will change after you upgrade.                                                                                               | None                                                                                                   |

## Examples

Run all tests before upgrading to Astro Runtime 8:

```bash
astro dev upgrade-test
```

Test an Astro project file against a the Astro Runtime distribution of a Airflow 2.6.3:

```bash
astro dev upgrade-test --airflow-version 2.6.3
```

Test only dependency version changes against the Astro Runtime distribution for Airflow 2.6.3:

```bash
astro dev upgrade-test --airflow-version 2.6.3 --provider-check
```

## Related Commands

- [`astro dev pytest`](cli/astro-dev-pytest.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
