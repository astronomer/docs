---
sidebar_label: "astro dev upgrade-test"
title: "astro dev upgrade-test"
id: astro-dev-upgrade-test
description: Test your Astro project before upgrading to a new Astro Runtime version.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Test your local Astro project against a new version of Astro Runtime to prepare for an upgrade. Specifically, this command will run the following tests:

- Identify major and minor version changes of the Python packages in your upgrade version.
- Identify DAG import errors that will appear after you upgrade.

See [Test before upgrading your Astro project](cli/test-your-astro-project-locally.md#test-before-upgrading-your-astro-project) for more detailed information about usage and test results.

## Usage

```bash
astro dev upgrade-test
```

By default, the command runs all three available tests on your project against the latest version of Astro Runtime.

## Options

| Option                       | Description                                                                                                                                                                                                                             | Possible Values                                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `-a`, `--airflow-version`    | The equivalent of Airflow you want to upgrade to. The default is the latest available version. Note that the Astro CLI will still test against an Astro Runtime image based on the Airflow version you specify.                         | Any valid [Airflow version](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html). |
| `-d`, `--dag-test`           | Only run DAG tests. These tests check whether your DAGs will generate import errors after you upgrade.                                                                                                                                  | None                                                                                                   |
| `-i`, `--deployment-id`      | Specify a Deployment ID to test with an image from an Astro Deployment instead of the image listed in your Astro project Dockerfile.                                                                                                    | Any valid Deployment ID.                                                                               |
| `-n`, `--image-name`         | A custom image with an upgraded image tag to test against. The CLI creates a new Dockerfile in your project named `upgrade-test-<old version>--<new version>/Dockerfile` that includes your upgraded image, then tests against that Dockerfile. | A valid image URL                                                                                                   |
| `-v`, `--runtime-version`    | The version of Astro Runtime you want to upgrade to. The default is the latest available version.                                                                                                                                       | Any valid [Astro runtime version](https://docs.astronomer.io/astro/runtime-release-notes).             |
| `--use-astronomer-certified` | Test against an Astronomer Certified distribution of Airflow. Must be used with `--airflow-version`.                                                                                                                                    | None                                                                                                   |
| `--version-test`             | Only run version tests. These tests show you how the versions of your dependencies will change after you upgrade.                                                                                                                       | None                                                                                                   |

## Examples

- Run all tests before upgrading to the latest version of Astro Runtime:

    ```bash
    astro dev upgrade-test
    ```

- Test an Astro project file against a the Astro Runtime distribution of a Airflow 2.6.3:

    ```bash
    astro dev upgrade-test --airflow-version 2.6.3
    ```

- Test only dependency version changes against the Astro Runtime distribution for Airflow 2.6.3:

    ```bash
    astro dev upgrade-test --airflow-version 2.6.3 --provider-check
    ```

- Test a custom image for an upgrade to a custom versioned distribution of Astro Runtime:

    ```bash
    astro dev upgrade-test --image-name quay.io/example-organization/new-example-organization-image:1.0.7
    ```

    If you were upgrading from `quay.io/example-organization/new-example-organization-image:1.0.5`, for example, the Astro CLI creates a new Dockerfile located in `upgrade-test-1.0.5--1.0.7/Dockerfile` that contains the image you specified and tests against it.

## Related Commands

- [`astro dev pytest`](cli/astro-dev-pytest.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
