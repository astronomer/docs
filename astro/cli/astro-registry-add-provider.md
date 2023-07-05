---
sidebar_label: "astro registry add provider"
title: "astro registry add provider"
id: astro-registry-add-provider
description: Reference documentation for astro registry add provider.
hide_table_of_contents: true
---

Download a provider package from the [Astronomer Registry](https://registry.astronomer.io/) to the `requirements.txt` file of your Astro project. 

## Usage 

```sh
astro registry add provider
```

When you run the command, the CLI prompts you for a provider to download. To retrieve the provider name, open the provider in the Astronomer registry and copy the URL between `providers/` and `/versions`. For example, in the URL `https://registry.astronomer.io/providers/apache-airflow-providers-airbyte/versions/3.3.1`, copy `apache-airflow-providers-airbyte`. 

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--version`   | The version of the provider to download.                                                                                                      | Any valid version.   |

## Examples

```sh
# Download version 1.2.0 of a provider
astro registry add provider --version 1.2.0
```

## Related commands

- [astro registry add dag](cli/astro-registry-add-dag.md)
- [astro dev start](cli/astro-dev-start.md)
