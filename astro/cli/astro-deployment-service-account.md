---
sidebar_label: "astro deployment service-account"
title: "astro deployment service-account"
id: astro-deployment-service-account
description: Manage service accounts (Software only)
hide_table_of_contents: true
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Manage Deployment-level service accounts, which you can use to configure a CI/CD pipeline or otherwise interact with the Astronomer Houston API.

## Usage

This command includes three subcommands: `create`, `delete`, and `list`

```sh
# Creates a Deployment-level service account
astro deployment service-account create --deployment-id=<your-deployment-id> --label=<your-service-account-label> 

# Deletes a Deployment-level service account
astro deployment service-account delete <your-service-account-label> 

# Shows the name, ID, and API key for each service account in a specific Deployment.
astro deployment service-account list
```

## Options

| Option              | Description                                                                              | Possible Values                       |
| ------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| `--category`                 | The category for the new service account as displayed in the Software UI    |  Any string. The default value is `default`. |
| `--deployment-id` (Required for `create` and `delete`) | The Deployment you're creating a service account for             | Any Deployment ID                                                             |
| `--label` (Required for `create`)         |The name or label for the new service account       | Any string                                                                           |
| `--role`                     |  The User Role for the new service account | Can be either `viewer`, `editor`, or `admin`. The default is `viewer`.                |


