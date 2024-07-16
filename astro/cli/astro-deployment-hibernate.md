---
sidebar_label: "astro deployment hibernate"
title: "astro deployment hibernate"
id: astro-deployment-hibernate
description: Hibernate a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

[Hibernate an Astro development Deployment](deployment-resources.md#hibernate-a-development-deployment) for a set amount of time. Overrides any existing hibernation schedule and sets the Deployment to hibernate for a specific duration or until a specific date.

## Usage

```sh
astro deployment hibernate [one of --until/ --for/ --remove-override]
```

## Options

| Option                   | Description                                                           | Possible Values                                      |
| ------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------- |
| `-n`,`--deployment-name` | The name of the development Deployment to hibernate.                  | Any valid Deployment name                            |
| `-u, --until`            | Specify the hibernation period using an end date and time.            | Any future date in the format `YYYY-MM-DDT00:00:00Z` |
| `-d, --for`              | Specify the hibernation period using a duration.                      | Any amount of time in the format `XhYm`            |
| `-r, --remove-override`  | Remove any existing override and resume regular hibernation schedule. | None                                                 |
| `-f, --force`            | The CLI will not prompt to confirm before hibernating the Deployment. | None                                                 |

## Related commands

- [`astro deployment wake-up`](astro-deployment-wake-up.md)