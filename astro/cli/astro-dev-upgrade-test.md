---
sidebar_label: "astro dev upgrade-test"
title: "astro dev upgrade-test"
id: astro-dev-upgrade-test
description: Reference documentation for astro dev upgrade-test.
hide_table_of_contents: true
---

Test your local Airflow environment against a new version of Airflow to prepare for an upgrade. This command can be used to test an upgrade to a specific Airflow, Astro Runtime, or Astronomer Certified version. Specifically, this command will test the following between your current Airflow version and your desired Airflow version:

- Identify dependency conflicts for the Python packages
- Identify major and minor version changes of the Python packages 
- Identify DAGs along with the import errors that will not import correctly during an upgrade

Though you cannot use this command directly with your Astro Deployment, you can build your Deployment's Astro project locally to check for the viability of your upgrade.

## Usage

By default, this command will perform all three tests on your local Airflow environment.

```bash
astro dev upgrade-test
```

## Options

| Option              | Description                                                                                                                                                                               | Possible Values                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `--airflow-version` | An Airflow version to check your DAGs and `requirements.txt` against. By default, the latest version of Airflow is chosen. If you are on the latest version, the command will do nothing. | Any valid [Airflow version](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html). |
| `--runtime-version` | An Astro runtime version to check your DAGs and `requirements.txt` against.                                                                                                               | Any valid [Astro runtime version](https://docs.astronomer.io/astro/runtime-release-notes).             |
| `--conflict-test`   | Check for dependency conflict between your `requirements.txt` and your new Airflow version                                                                                                | N/A                                                                                                    |
| `--dag-test`        | Check for DAGs import errors against your new Airflow version                                                                                                                             | N/A                                                                                                    |
| `--provider-check`  | Check for major depedency changes                                                                                                                                                         | N/A                                                                                                    |

## Examples

To test your DAGs and `requirements.txt` against the latest version of Airflow:

```bash
astro dev upgrade-test
```

To test your DAGs and `requirements.txt` against a specific version of Airflow:

```bash
astro dev upgrade-test --airflow-version 2.6.3
```

To check for major dependency change from the current Airflow version to a specific version of Airflow:

```bash
astro dev upgrade-test --airflow-version 2.6.3 --provider-check 
```

## Related Commands

- [`astro dev pytest`](cli/astro-dev-pytest.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
