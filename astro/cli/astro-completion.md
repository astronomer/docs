---
sidebar_label: "astro completion"
title: "astro completion"
id: astro-completion
description: Reference documentation for astro completion.
---

## Description

Generate completion scripts for Astro CLI commands. You can modify the generated scripts and add them to the appropriate directory to customize your command line autocompletion behavior.

For example, you could set automation such that typing `astro lo` autocompletes to `astro login` if you press **TAB** on your keyboard and `astro login` or `astro logout` if you press **TAB** again.

This command is helpful for users interacting with the CLI on a regular basis.

## Usage

```sh
astro completion <shell>
```

## Options

| Option  | Description                                          | Possible Values                   |
| ------- | ---------------------------------------------------- | --------------------------------- |
| `<shell>` | The type of shell to generate completion scripts for | `bash`,`fish`, `powershell`,`zsh` |

## Example

To generate a shell completion script for zsh, for example, you can run:

```sh
$ astro completion zsh > /usr/local/share/zsh/site-functions/_astro
# Completion script saved in your local directory
```

Then, to enable autocompletion, ensure that the following lines are present in your `~/.zshrc` file:

```sh
autoload -U compinit
compinit -i
```
