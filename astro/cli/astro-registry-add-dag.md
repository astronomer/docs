---
sidebar_label: "astro registry add dag"
title: "astro registry add dag"
id: astro-registry-add-dag
description: Reference documentation for astro registry add dag.
hide_table_of_contents: true
---

Download a DAG from the [Astronomer Registry](https://registry.astronomer.io/) to your Astro project. 

## Usage 

```sh
astro registry add dag
```

When you run the command, the CLI prompts you for a DAG ID to download. To retrieve the DAG name, open the DAG in the Astronomer registry and copy the URL between `dags/` and `/versions`. For example, in the URL `https://registry.astronomer.io/dags/upload_files_to_s3/versions/1.0.0`, copy `upload_files_to_s3`.

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--version`   | The version of the DAG to download.                                                                                                      | Any valid version.   |
| `--add-providers` | Attempt to add the required providers for the DAG to `requirements.txt`. | None. |

## Examples

```sh
# Download version 1.2.0 of a DAG
astro registry add dag --version 1.2.0
```

## Related commands

- [astro registry add provider](cli/astro-registry-add-provider.md)
- [astro dev start](cli/astro-dev-start.md)
