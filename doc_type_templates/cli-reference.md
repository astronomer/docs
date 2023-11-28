---
sidebar_label: "cli ref title"
title: "cli ref title"
id: cli-ref-title
description: Short cli description.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

<!-- All CLI ref must include the `sidebar_custom_props` line in the header to ensure generated sidebar info renders correctly.-->
<!-- See cli/astro-workspace-user-list.md for a command reference example that includes both software and astro commands, outputs, usage examples, and input options -->

- Intro summary naming and defining the category, command, or feature

## Usage

- A code example of the command syntax

```bash
astro command syntax
```

## Options

- Include a table of all required and optional parameters
- This table includes columns for Option, Description, and Possible Values

| Option   | Description                       | Possible Values  |
| -------- | --------------------------------- | ---------------- |
| `option` | Description of option parameters. | Possible values. |

## Output (optional)

- If the command returns a list of output, define the columns of that output
- List the output column titles in the first column, "Output"
- List the output definitions in the second column, "description"
- list the output data type in the final column "data type"
- See `astro workspace team list` for an example

| Output   | Description | Data Type |
| -------- | ----------- | --------- |
| `output` | Dexription  | Data type |

## Examples (Optional)

- A code example that uses the command syntax
- should not contain stand-in values such as <dag-id>

```bash

astro command things

```

## Related commands

- include links to associated commands,
  - for example, astro workspace switch and astro workplace list
