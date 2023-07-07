---
sidebar_label: "astro registry dag add"
title: "astro registry dag add"
id: astro-registry-dag-add
description: Reference documentation for astro registry dag add.
hide_table_of_contents: true
---

Download a DAG from the [Astronomer Registry](https://registry.astronomer.io/) to your Astro project. 

## Usage 

```sh
astro registry dag add
```

When you run the command, the CLI prompts you for a DAG ID to download. To retrieve the DAG name, open the DAG in the Astronomer registry and copy the URL between `dags/` and `/versions`. For example, in the URL `https://registry.astronomer.io/dags/upload_files_to_s3/versions/1.0.0`, copy `upload_files_to_s3`.

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `<dag-id>`   | The DAG ID to download.                                                                                                      | Any valid DAG ID. Must be the first option in the command.  |
| `--version`   | The version of the DAG to download.                                                                                                      | Any valid version.   |
| `--add-providers` | Attempt to add the required providers for the DAG to `requirements.txt`. | None. |

## Examples

```sh
# Download version 1.0.0 of a DAG called 'upload_files_to_s3'
astro registry dag add upload_files_to_s3 --version 1.0.0
```

## Related commands

- [astro registry provider add](cli/astro-registry-provider-add.md)
- [astro dev start](cli/astro-dev-start.md)
